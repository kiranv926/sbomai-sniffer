package com.sbomai.cli.services;

import com.sbomai.cli.commands.AnalysisRequest;
import com.sbomai.cli.commands.AnalysisResult;
import com.sbomai.core.services.HealthStatus;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;

/**
 * Service for communicating with remote SBOMAI core services.
 */
@Service
public class RemoteApiService {

    private static final Logger logger = LoggerFactory.getLogger(RemoteApiService.class);

    private final WebClient webClient;

    public RemoteApiService() {
        this.webClient = WebClient.builder()
            .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(50 * 1024 * 1024)) // 50MB
            .build();
    }

    /**
     * Analyzes an SBOM file using remote services.
     * 
     * @param request The analysis request
     * @return Analysis result
     */
    public AnalysisResult analyzeSbom(AnalysisRequest request) {
        try {
            String apiUrl = request.getRemoteUrl() + "/api/v1/sbom/analyze";
            
            // Prepare multipart form data
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", new FileSystemResource(request.getSbomFile()));
            body.add("format", request.getFormat());

            // Make API call
            var response = webClient.post()
                .uri(apiUrl)
                .contentType(MediaType.MULTIPART_FORM_DATA)
                .bodyValue(body)
                .retrieve()
                .bodyToMono(com.sbomai.core.services.AnalysisResult.class)
                .block();

            if (response != null) {
                // Convert to CLI result
                AnalysisResult result = new AnalysisResult();
                result.setSuccessful(response.getAnalysisStatus() == com.sbomai.core.domain.AnalysisStatus.COMPLETED);
                result.setSbomDocument(response.getSbomDocument());
                result.setVulnerabilityReport(response.getVulnerabilityReport());
                result.setAiAnalysisResult(response.getAiAnalysisResult());
                result.setPolicyViolations(response.getPolicyViolations());
                result.setErrorMessage(response.getErrorMessage());
                return result;
            } else {
                throw new RuntimeException("No response received from remote service");
            }

        } catch (WebClientResponseException e) {
            logger.error("Remote API call failed with status: {}", e.getStatusCode(), e);
            AnalysisResult result = new AnalysisResult();
            result.setSuccessful(false);
            result.setErrorMessage("Remote API call failed: " + e.getStatusCode() + " - " + e.getResponseBodyAsString());
            return result;
        } catch (Exception e) {
            logger.error("Remote API call failed", e);
            AnalysisResult result = new AnalysisResult();
            result.setSuccessful(false);
            result.setErrorMessage("Remote API call failed: " + e.getMessage());
            return result;
        }
    }

    /**
     * Checks the health of remote services.
     * 
     * @param remoteUrl The remote service URL
     * @return true if remote services are healthy
     */
    public boolean checkHealth(String remoteUrl) {
        try {
            String healthUrl = remoteUrl + "/api/v1/sbom/health";
            
            var response = webClient.get()
                .uri(healthUrl)
                .retrieve()
                .bodyToMono(HealthStatus.class)
                .block();

            return response != null && response.isFullyOperational();

        } catch (WebClientResponseException e) {
            logger.error("Health check failed with status: {}", e.getStatusCode(), e);
            return false;
        } catch (Exception e) {
            logger.error("Health check failed", e);
            return false;
        }
    }
} 