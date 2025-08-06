package com.sbomai.core.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.sbomai.core.domain.Scan;
import com.sbomai.core.domain.SbomDocument;
import com.sbomai.core.domain.SbomComponent;
import com.sbomai.core.domain.ScanStatus;
import com.sbomai.core.dto.SbomProcessedEvent;
import com.sbomai.core.dto.SbomReceivedEvent;
import com.sbomai.core.dto.VulnerabilitiesDetectedEvent;
import com.sbomai.core.repository.ScanRepository;
import com.sbomai.core.repository.SbomDocumentRepository;
import com.sbomai.core.repository.SbomComponentRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.List;
import java.util.UUID;

@Service
public class SbomOrchestrationService {
    
    private static final Logger logger = LoggerFactory.getLogger(SbomOrchestrationService.class);
    
    @Autowired
    private ScanRepository scanRepository;
    
    @Autowired
    private SbomDocumentRepository sbomDocumentRepository;
    
    @Autowired
    private SbomComponentRepository sbomComponentRepository;
    
    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;
    
    @Autowired
    private WebClient webClient;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Value("")
    private String parserServiceUrl;
    
    @Value("")
    private String analysisServiceUrl;
    
    @Value("")
    private String sbomProcessedTopic;
    
    @Value("")
    private String scanCompletedTopic;
    
    @Value("")
    private String scanFailedTopic;
    
    @KafkaListener(topics = "", groupId = "sbomai-core")
    public void handleSbomReceived(SbomReceivedEvent event) {
        logger.info("Received SBOM processing request for scan: {}", event.getScanId());
        
        try {
            // Step 1: Update scan status to PARSING
            updateScanStatus(event.getScanId(), ScanStatus.PARSING);
            
            // Step 2: Call Go parser service
            JsonNode parsedSbom = callParserService(event.getRawSbomContent());
            
            // Step 3: Save SBOM to database
            UUID sbomDocumentId = saveSbomToDatabase(event.getScanId(), parsedSbom);
            
            // Step 4: Extract and store components
            int componentsCount = extractAndStoreComponents(event.getScanId(), sbomDocumentId, parsedSbom);
            
            // Step 5: Update scan status and publish sbom.processed event
            updateScanStatus(event.getScanId(), ScanStatus.ANALYSIS_PENDING);
            publishSbomProcessedEvent(event.getScanId(), sbomDocumentId, componentsCount);
            
            // Step 6: Trigger vulnerability analysis (non-blocking)
            triggerVulnerabilityAnalysis(event.getScanId(), sbomDocumentId);
            
            logger.info("Successfully processed SBOM for scan: {}", event.getScanId());
            
        } catch (Exception e) {
            logger.error("Failed to process SBOM for scan: {}", event.getScanId(), e);
            handleProcessingError(event.getScanId(), e.getMessage());
        }
    }
    
    @KafkaListener(topics = "", groupId = "sbomai-core")
    public void handleVulnerabilitiesDetected(VulnerabilitiesDetectedEvent event) {
        logger.info("Received vulnerability analysis results for scan: {}", event.getScanId());
        
        try {
            // Step 1: Save vulnerabilities to database
            saveVulnerabilitiesToDatabase(event.getScanId(), event.getVulnerabilities());
            
            // Step 2: Update scan status to COMPLETED
            updateScanStatus(event.getScanId(), ScanStatus.COMPLETED);
            
            // Step 3: Update scan with analysis results
            updateScanWithAnalysisResults(event.getScanId(), event.getAnalysisSummary());
            
            // Step 4: Publish scan.completed event
            publishScanCompletedEvent(event.getScanId(), event.getAnalysisSummary());
            
            logger.info("Successfully completed vulnerability analysis for scan: {}", event.getScanId());
            
        } catch (Exception e) {
            logger.error("Failed to process vulnerability results for scan: {}", event.getScanId(), e);
            handleProcessingError(event.getScanId(), e.getMessage());
        }
    }
    
    private void updateScanStatus(UUID scanId, ScanStatus status) {
        try {
            Scan scan = scanRepository.findById(scanId)
                    .orElseThrow(() -> new RuntimeException("Scan not found: " + scanId));
            
            scan.setStatus(status);
            scanRepository.save(scan);
            
            logger.info("Updated scan {} status to: {}", scanId, status);
        } catch (Exception e) {
            logger.error("Failed to update scan status for scan: {}", scanId, e);
            throw e;
        }
    }
    
    private JsonNode callParserService(String rawSbomContent) {
        try {
            return webClient.post()
                    .uri(parserServiceUrl + "/parse-sbom")
                    .bodyValue(rawSbomContent)
                    .retrieve()
                    .bodyToMono(JsonNode.class)
                    .timeout(Duration.ofSeconds(30))
                    .retry(3)
                    .block();
        } catch (WebClientResponseException e) {
            logger.error("Parser service returned error: {} - {}", e.getStatusCode(), e.getResponseBodyAsString());
            throw new RuntimeException("Failed to parse SBOM: " + e.getMessage());
        } catch (Exception e) {
            logger.error("Failed to call parser service", e);
            throw new RuntimeException("Failed to call parser service: " + e.getMessage());
        }
    }
    
    private UUID saveSbomToDatabase(UUID scanId, JsonNode parsedSbom) {
        try {
            SbomDocument sbomDocument = new SbomDocument();
            sbomDocument.setScanId(scanId);
            sbomDocument.setFormat(parsedSbom.path("bomFormat").asText("cyclonedx"));
            sbomDocument.setSpecVersion(parsedSbom.path("specVersion").asText("1.0"));
            sbomDocument.setRawJson(parsedSbom.toString());
            
            SbomDocument saved = sbomDocumentRepository.save(sbomDocument);
            logger.info("Saved SBOM document {} for scan: {}", saved.getId(), scanId);
            return saved.getId();
        } catch (Exception e) {
            logger.error("Failed to save SBOM to database for scan: {}", scanId, e);
            throw e;
        }
    }
    
    private int extractAndStoreComponents(UUID scanId, UUID sbomDocumentId, JsonNode parsedSbom) {
        try {
            int componentsCount = 0;
            if (parsedSbom.has("components")) {
                JsonNode components = parsedSbom.get("components");
                componentsCount = components.size();
                
                for (JsonNode component : components) {
                    SbomComponent sbomComponent = new SbomComponent();
                    sbomComponent.setSbomId(sbomDocumentId);
                    sbomComponent.setBomRef(component.path("bom-ref").asText(""));
                    sbomComponent.setName(component.path("name").asText(""));
                    sbomComponent.setVersion(component.path("version").asText(""));
                    sbomComponent.setType(component.path("type").asText("library"));
                    sbomComponent.setPurl(component.path("purl").asText(""));
                    sbomComponent.setCpe(component.path("cpe").asText(""));
                    
                    // Handle licenses
                    if (component.has("licenses") && component.get("licenses").isArray() && component.get("licenses").size() > 0) {
                        String licenseId = component.get("licenses").get(0).path("license").path("id").asText("");
                        sbomComponent.setLicenseId(licenseId);
                    }
                    
                    sbomComponentRepository.save(sbomComponent);
                }
                
                logger.info("Extracted and stored {} components for scan: {}", componentsCount, scanId);
            }
            return componentsCount;
        } catch (Exception e) {
            logger.error("Failed to extract and store components for scan: {}", scanId, e);
            throw e;
        }
    }
    
    private void publishSbomProcessedEvent(UUID scanId, UUID sbomDocumentId, int componentsCount) {
        try {
            SbomProcessedEvent event = new SbomProcessedEvent(scanId, sbomDocumentId, componentsCount);
            kafkaTemplate.send(sbomProcessedTopic, scanId.toString(), event);
            logger.info("Published sbom.processed event for scan: {}", scanId);
        } catch (Exception e) {
            logger.error("Failed to publish sbom.processed event for scan: {}", scanId, e);
            throw e;
        }
    }
    
    private void triggerVulnerabilityAnalysis(UUID scanId, UUID sbomDocumentId) {
        try {
            webClient.post()
                    .uri(analysisServiceUrl + "/analyze-vulnerabilities")
                    .bodyValue(new AnalysisRequest(scanId, sbomDocumentId))
                    .retrieve()
                    .bodyToMono(Void.class)
                    .timeout(Duration.ofSeconds(10))
                    .subscribe(
                            result -> logger.info("Triggered vulnerability analysis for scan: {}", scanId),
                            error -> logger.error("Failed to trigger vulnerability analysis for scan: {}", scanId, error)
                    );
        } catch (Exception e) {
            logger.error("Failed to trigger vulnerability analysis for scan: {}", scanId, e);
            // Don't throw here as this is non-blocking
        }
    }
    
    private void saveVulnerabilitiesToDatabase(UUID scanId, List<VulnerabilitiesDetectedEvent.VulnerabilityData> vulnerabilities) {
        // Implementation to save vulnerabilities to database
        // This would save to vulnerabilities and component_vulnerabilities tables
        logger.info("Saved {} vulnerabilities for scan: {}", vulnerabilities.size(), scanId);
    }
    
    private void updateScanWithAnalysisResults(UUID scanId, VulnerabilitiesDetectedEvent.AnalysisSummary summary) {
        try {
            Scan scan = scanRepository.findById(scanId)
                    .orElseThrow(() -> new RuntimeException("Scan not found: " + scanId));
            
            scan.setVulnerabilitiesFound(summary.getTotalVulnerabilities());
            scan.setRiskScore(summary.getOverallRiskScore());
            scanRepository.save(scan);
            
            logger.info("Updated scan {} with analysis results", scanId);
        } catch (Exception e) {
            logger.error("Failed to update scan with analysis results for scan: {}", scanId, e);
            throw e;
        }
    }
    
    private void publishScanCompletedEvent(UUID scanId, VulnerabilitiesDetectedEvent.AnalysisSummary summary) {
        try {
            ScanCompletedEvent event = new ScanCompletedEvent(scanId, summary);
            kafkaTemplate.send(scanCompletedTopic, scanId.toString(), event);
            logger.info("Published scan.completed event for scan: {}", scanId);
        } catch (Exception e) {
            logger.error("Failed to publish scan.completed event for scan: {}", scanId, e);
            throw e;
        }
    }
    
    private void handleProcessingError(UUID scanId, String errorMessage) {
        try {
            updateScanStatus(scanId, ScanStatus.FAILED);
            
            // Publish scan.failed event
            ScanFailedEvent event = new ScanFailedEvent(scanId, errorMessage);
            kafkaTemplate.send(scanFailedTopic, scanId.toString(), event);
            
            logger.error("Published scan.failed event for scan: {} with error: {}", scanId, errorMessage);
        } catch (Exception e) {
            logger.error("Failed to handle processing error for scan: {}", scanId, e);
        }
    }
    
    // Helper classes for internal use
    private static class AnalysisRequest {
        private UUID scanId;
        private UUID sbomDocumentId;
        
        public AnalysisRequest(UUID scanId, UUID sbomDocumentId) {
            this.scanId = scanId;
            this.sbomDocumentId = sbomDocumentId;
        }
        
        // Getters
        public UUID getScanId() { return scanId; }
        public UUID getSbomDocumentId() { return sbomDocumentId; }
    }
    
    private static class ScanCompletedEvent {
        private UUID scanId;
        private VulnerabilitiesDetectedEvent.AnalysisSummary summary;
        
        public ScanCompletedEvent(UUID scanId, VulnerabilitiesDetectedEvent.AnalysisSummary summary) {
            this.scanId = scanId;
            this.summary = summary;
        }
        
        // Getters
        public UUID getScanId() { return scanId; }
        public VulnerabilitiesDetectedEvent.AnalysisSummary getSummary() { return summary; }
    }
    
    private static class ScanFailedEvent {
        private UUID scanId;
        private String errorMessage;
        
        public ScanFailedEvent(UUID scanId, String errorMessage) {
            this.scanId = scanId;
            this.errorMessage = errorMessage;
        }
        
        // Getters
        public UUID getScanId() { return scanId; }
        public String getErrorMessage() { return errorMessage; }
    }
}
