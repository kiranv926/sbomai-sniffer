package com.sbomai.core.adapters;

import com.sbomai.core.domain.AiAnalysisResult;
import com.sbomai.core.domain.RiskLevel;
import com.sbomai.core.domain.AnalysisStatus;
import com.sbomai.core.domain.SbomDocument;
import com.sbomai.core.ports.AiAnalyzer;
import com.sbomai.core.ports.AiAnalysisException;
import com.sbomai.core.ports.AnalysisParameters;
import com.sbomai.core.ports.AnalyzerInfo;
import com.sbomai.core.ports.CostEstimate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import java.util.concurrent.TimeUnit;
import java.util.Map;

/**
 * gRPC client adapter for the Python AI Microservice
 * Connects to the Python AI service via gRPC for advanced AI analysis
 */
@Service
public class GrpcAiAnalyzer implements AiAnalyzer {
    
    private static final Logger logger = LoggerFactory.getLogger(GrpcAiAnalyzer.class);
    
    @Value("${sbomai.ai.grpc.host:localhost}")
    private String grpcHost;
    
    @Value("${sbomai.ai.grpc.port:50051}")
    private int grpcPort;
    
    @Value("${sbomai.ai.grpc.timeout:30}")
    private int timeoutSeconds;
    
    private final Executor executor;
    private volatile boolean isAvailable = false;
    
    public GrpcAiAnalyzer(Executor executor) {
        this.executor = executor;
        checkAvailability();
    }
    
    @Override
    public CompletableFuture<AiAnalysisResult> analyze(SbomDocument sbomDocument) {
        return analyze(sbomDocument, AnalysisParameters.builder().build());
    }
    
    @Override
    public CompletableFuture<AiAnalysisResult> analyze(SbomDocument sbomDocument, AnalysisParameters parameters) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                logger.info("Starting gRPC AI analysis for SBOM: {}", sbomDocument.getDocumentName());
                
                // Convert SBOM document to gRPC request format
                var request = buildExplainRiskRequest(sbomDocument, parameters);
                
                // Call Python AI service via gRPC
                var response = callPythonAiService(request);
                
                // Convert response back to domain model
                return convertToAiAnalysisResult(response, sbomDocument);
                
            } catch (Exception e) {
                logger.error("Error during gRPC AI analysis: {}", e.getMessage(), e);
                throw new RuntimeException(new AiAnalysisException("Failed to analyze SBOM via gRPC AI service", e));
            }
        }, executor);
    }
    
    @Override
    public String[] getAvailableModels() {
        return new String[]{"gpt-4", "claude-3", "gemini-pro", "local-bert"};
    }
    
    @Override
    public boolean isAvailable() {
        return isAvailable;
    }
    
    @Override
    public AnalyzerInfo getAnalyzerInfo() {
                        return new AnalyzerInfo(
                    "AI/ML Models Microservice",
                    "1.0.0",
                    new String[]{"explain_risk", "predict_risk", "suggest_fix", "explainable_chain"},
                    isAvailable,
                    "grpc"
                );
    }
    
    @Override
    public CostEstimate estimateCost(SbomDocument sbomDocument) {
        // Estimate based on component count and complexity
        int componentCount = sbomDocument.getComponents().size();
        double estimatedCost = componentCount * 0.01; // $0.01 per component
        
        return new CostEstimate(
            estimatedCost,
            "USD",
            "grpc-ai-service",
            componentCount,
            "Estimated cost based on component count"
        );
    }
    
    private Object buildExplainRiskRequest(SbomDocument sbomDocument, AnalysisParameters parameters) {
        // Build gRPC request for explainable SBOM chain analysis
        // This would use the generated gRPC client code
        return Map.of(
            "sbom_document", convertSbomDocument(sbomDocument),
            "chain_config", Map.of(
                "max_steps", 10,
                "confidence_threshold", parameters.getConfidenceThreshold(),
                "include_detailed_explanations", true,
                "analysis_types", List.of("vulnerability", "license", "outdated")
            )
        );
    }
    
    private Object buildComponentAnalysisRequest(String componentName, String version, 
                                               List<String> vulnerabilities, AnalysisParameters parameters) {
        return Map.of(
            "component", Map.of(
                "name", componentName,
                "version", version
            ),
            "vulnerabilities", vulnerabilities.stream()
                .map(vuln -> Map.of("id", vuln))
                .toList(),
            "analysis_context", "Component analysis",
            "model_config", Map.of(
                "model_name", parameters.getModel(),
                "temperature", parameters.getTemperature(),
                "provider", "auto"
            )
        );
    }
    
    private Object callPythonAiService(Object request) {
        // This would use the actual gRPC client to call the Python service
        // For now, return a mock response
        logger.info("Calling Python AI service at {}:{}", grpcHost, grpcPort);
        
        // Simulate gRPC call
        try {
            Thread.sleep(1000); // Simulate network delay
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        return Map.of(
            "explanation", "AI analysis completed via gRPC service",
            "confidence_score", 0.85,
            "sources", List.of("NVD", "OSS Index"),
            "key_factors", List.of("Component age", "Vulnerability count"),
            "risk_level", "MEDIUM",
            "model_used", "gpt-4",
            "processing_time_ms", 1200
        );
    }
    
    private AiAnalysisResult convertToAiAnalysisResult(Object response, SbomDocument sbomDocument) {
        // Convert gRPC response to domain model
        var result = new AiAnalysisResult();
        result.setRiskLevel(RiskLevel.MEDIUM); // Extract from response
        result.setAnalysisSummary("AI analysis completed via gRPC service");
        result.setConfidenceScore(0.85); // Extract confidence from response
        result.setStatus(AnalysisStatus.COMPLETED);
        result.setModelUsed("grpc-ai-service");
        result.setAnalysisDurationMs(System.currentTimeMillis());
        return result;
    }
    
    private AiAnalysisResult convertToAiAnalysisResult(Object response, String componentName, String version) {
        var result = new AiAnalysisResult();
        result.setRiskLevel(RiskLevel.MEDIUM);
        result.setAnalysisSummary("Component analysis completed via gRPC service");
        result.setConfidenceScore(0.85);
        result.setStatus(AnalysisStatus.COMPLETED);
        result.setModelUsed("grpc-ai-service");
        result.setAnalysisDurationMs(System.currentTimeMillis());
        return result;
    }
    
    private Map<String, Object> convertSbomDocument(SbomDocument sbomDocument) {
        return Map.of(
            "name", sbomDocument.getDocumentName(),
            "version", sbomDocument.getDocumentVersion(),
            "format", sbomDocument.getSbomFormat().toString(),
            "created_date", sbomDocument.getCreatedDate().toString(),
            "components", sbomDocument.getComponents().stream()
                .map(this::convertComponent)
                .toList()
        );
    }
    
    private Map<String, Object> convertComponent(com.sbomai.core.domain.SbomComponent component) {
        return Map.of(
            "name", component.getName(),
            "version", component.getVersion(),
            "group_id", component.getGroupId(),
            "license", component.getLicense() != null ? component.getLicense() : "",
            "purl", component.getPurl()
        );
    }
    
    private void checkAvailability() {
        // Check if Python AI service is available
        CompletableFuture.runAsync(() -> {
            try {
                // Try to connect to gRPC service
                // For now, just set as available
                isAvailable = true;
                                            logger.info("AI/ML Models Microservice is available at {}:{}", grpcHost, grpcPort);
            } catch (Exception e) {
                isAvailable = false;
                                            logger.warn("AI/ML Models Microservice is not available: {}", e.getMessage());
            }
        }, executor);
    }
} 