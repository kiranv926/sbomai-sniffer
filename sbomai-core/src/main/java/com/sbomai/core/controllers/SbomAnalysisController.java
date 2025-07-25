package com.sbomai.core.controllers;

import com.sbomai.core.domain.SbomFormat;
import com.sbomai.core.services.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.concurrent.CompletableFuture;

/**
 * REST API controller for SBOM analysis operations.
 * 
 * This controller exposes the core SBOM analysis functionality through
 * REST endpoints for external modules to consume.
 */
@RestController
@RequestMapping("/api/v1/sbom")
@CrossOrigin(origins = "*")
public class SbomAnalysisController {

    private static final Logger logger = LoggerFactory.getLogger(SbomAnalysisController.class);

    private final SbomAnalysisOrchestrator orchestrator;

    @Autowired
    public SbomAnalysisController(SbomAnalysisOrchestrator orchestrator) {
        this.orchestrator = orchestrator;
    }

    /**
     * Analyzes an SBOM document with default settings.
     * 
     * @param file The SBOM file to analyze
     * @param format The format of the SBOM (SPDX, CYCLONEDX, etc.)
     * @return CompletableFuture containing the analysis result
     */
    @PostMapping(value = "/analyze", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public CompletableFuture<ResponseEntity<AnalysisResult>> analyzeSbom(
            @RequestParam("file") MultipartFile file,
            @RequestParam("format") String format) {
        
        logger.info("Received SBOM analysis request for file: {} with format: {}", 
            file.getOriginalFilename(), format);
        
        try {
            SbomFormat sbomFormat = SbomFormat.fromCode(format);
            return orchestrator.analyzeSbom(file.getInputStream(), sbomFormat)
                .thenApply(result -> {
                    if (result.getAnalysisStatus() == com.sbomai.core.domain.AnalysisStatus.COMPLETED) {
                        return ResponseEntity.ok(result);
                    } else {
                        return ResponseEntity.badRequest().body(result);
                    }
                });
        } catch (IllegalArgumentException e) {
            logger.error("Invalid SBOM format: {}", format, e);
            AnalysisResult errorResult = new AnalysisResult();
            errorResult.setAnalysisStatus(com.sbomai.core.domain.AnalysisStatus.FAILED);
            errorResult.setErrorMessage("Invalid SBOM format: " + format);
            return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(errorResult));
        } catch (IOException e) {
            logger.error("Failed to read uploaded file", e);
            AnalysisResult errorResult = new AnalysisResult();
            errorResult.setAnalysisStatus(com.sbomai.core.domain.AnalysisStatus.FAILED);
            errorResult.setErrorMessage("Failed to read uploaded file: " + e.getMessage());
            return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(errorResult));
        }
    }

    /**
     * Analyzes an SBOM document with custom parameters.
     * 
     * @param file The SBOM file to analyze
     * @param format The format of the SBOM (SPDX, CYCLONEDX, etc.)
     * @param request Custom analysis parameters
     * @return CompletableFuture containing the analysis result
     */
    @PostMapping(value = "/analyze/custom", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public CompletableFuture<ResponseEntity<AnalysisResult>> analyzeSbomCustom(
            @RequestParam("file") MultipartFile file,
            @RequestParam("format") String format,
            @RequestParam("request") String requestJson) {
        
        logger.info("Received custom SBOM analysis request for file: {} with format: {}", 
            file.getOriginalFilename(), format);
        
        try {
            SbomFormat sbomFormat = SbomFormat.fromCode(format);
            // TODO: Parse requestJson into AnalysisRequest object
            AnalysisRequest request = new AnalysisRequest(); // Placeholder
            
            return orchestrator.analyzeSbom(file.getInputStream(), sbomFormat, request)
                .thenApply(result -> {
                    if (result.getAnalysisStatus() == com.sbomai.core.domain.AnalysisStatus.COMPLETED) {
                        return ResponseEntity.ok(result);
                    } else {
                        return ResponseEntity.badRequest().body(result);
                    }
                });
        } catch (IllegalArgumentException e) {
            logger.error("Invalid SBOM format: {}", format, e);
            AnalysisResult errorResult = new AnalysisResult();
            errorResult.setAnalysisStatus(com.sbomai.core.domain.AnalysisStatus.FAILED);
            errorResult.setErrorMessage("Invalid SBOM format: " + format);
            return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(errorResult));
        } catch (IOException e) {
            logger.error("Failed to read uploaded file", e);
            AnalysisResult errorResult = new AnalysisResult();
            errorResult.setAnalysisStatus(com.sbomai.core.domain.AnalysisStatus.FAILED);
            errorResult.setErrorMessage("Failed to read uploaded file: " + e.getMessage());
            return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(errorResult));
        }
    }

    /**
     * Gets the health status of all analysis components.
     * 
     * @return Health status information
     */
    @GetMapping("/health")
    public ResponseEntity<HealthStatus> getHealthStatus() {
        logger.debug("Received health status request");
        HealthStatus status = orchestrator.getHealthStatus();
        
        if (status.isFullyOperational()) {
            status.setOverallStatus("HEALTHY");
            return ResponseEntity.ok(status);
        } else {
            status.setOverallStatus("DEGRADED");
            return ResponseEntity.status(503).body(status);
        }
    }

    /**
     * Gets the capabilities of all analysis components.
     * 
     * @return Capabilities information
     */
    @GetMapping("/capabilities")
    public ResponseEntity<Capabilities> getCapabilities() {
        logger.debug("Received capabilities request");
        Capabilities capabilities = orchestrator.getCapabilities();
        return ResponseEntity.ok(capabilities);
    }

    /**
     * Analyzes an SBOM document from JSON content.
     * 
     * @param format The format of the SBOM (SPDX, CYCLONEDX, etc.)
     * @param content The SBOM content as JSON string
     * @return CompletableFuture containing the analysis result
     */
    @PostMapping(value = "/analyze/json", consumes = MediaType.APPLICATION_JSON_VALUE)
    public CompletableFuture<ResponseEntity<AnalysisResult>> analyzeSbomJson(
            @RequestParam("format") String format,
            @RequestBody String content) {
        
        logger.info("Received SBOM JSON analysis request with format: {}", format);
        
        try {
            SbomFormat sbomFormat = SbomFormat.fromCode(format);
            // TODO: Implement JSON parsing and analysis
            AnalysisResult result = new AnalysisResult();
            result.setAnalysisStatus(com.sbomai.core.domain.AnalysisStatus.FAILED);
            result.setErrorMessage("JSON analysis not yet implemented");
            return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(result));
        } catch (IllegalArgumentException e) {
            logger.error("Invalid SBOM format: {}", format, e);
            AnalysisResult errorResult = new AnalysisResult();
            errorResult.setAnalysisStatus(com.sbomai.core.domain.AnalysisStatus.FAILED);
            errorResult.setErrorMessage("Invalid SBOM format: " + format);
            return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(errorResult));
        }
    }
} 