package com.sbomai.core.services;

import com.sbomai.core.domain.*;
import com.sbomai.core.ports.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.InputStream;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;

/**
 * Main orchestrator service that coordinates SBOM analysis operations.
 * 
 * This service provides a unified interface for parsing, scanning, analyzing,
 * and enforcing policies on SBOM documents.
 */
@Service
public class SbomAnalysisOrchestrator {

    private static final Logger logger = LoggerFactory.getLogger(SbomAnalysisOrchestrator.class);

    private final SbomParser sbomParser;
    private final VulnerabilityScanner vulnerabilityScanner;
    private final AiAnalyzer aiAnalyzer;
    private final PolicyEnforcer policyEnforcer;
    private final Executor analysisExecutor;

    @Autowired
    public SbomAnalysisOrchestrator(
            SbomParser sbomParser,
            VulnerabilityScanner vulnerabilityScanner,
            AiAnalyzer aiAnalyzer,
            PolicyEnforcer policyEnforcer,
            Executor analysisExecutor) {
        this.sbomParser = sbomParser;
        this.vulnerabilityScanner = vulnerabilityScanner;
        this.aiAnalyzer = aiAnalyzer;
        this.policyEnforcer = policyEnforcer;
        this.analysisExecutor = analysisExecutor;
    }

    /**
     * Performs a complete analysis of an SBOM document.
     * 
     * @param inputStream The input stream containing the SBOM data
     * @param format The expected format of the SBOM
     * @return CompletableFuture containing the analysis result
     */
    public CompletableFuture<AnalysisResult> analyzeSbom(InputStream inputStream, SbomFormat format) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                logger.info("Starting complete SBOM analysis for format: {}", format);
                
                // Step 1: Parse the SBOM
                SbomDocument sbomDocument = parseSbom(inputStream, format);
                
                // Step 2: Perform parallel analysis
                CompletableFuture<VulnerabilityReport> vulnerabilityFuture = 
                    vulnerabilityScanner.scan(sbomDocument);
                
                CompletableFuture<AiAnalysisResult> aiAnalysisFuture = 
                    aiAnalyzer.analyze(sbomDocument);
                
                CompletableFuture<List<PolicyViolation>> policyFuture = 
                    CompletableFuture.supplyAsync(() -> {
                        try {
                            return policyEnforcer.enforcePolicies(sbomDocument);
                        } catch (PolicyEnforcementException e) {
                            logger.error("Policy enforcement failed", e);
                            throw new RuntimeException(e);
                        }
                    }, analysisExecutor);

                // Step 3: Wait for all analysis to complete
                CompletableFuture<Void> allAnalysis = CompletableFuture.allOf(
                    vulnerabilityFuture, aiAnalysisFuture, policyFuture
                );

                allAnalysis.join();

                // Step 4: Build the complete analysis result
                AnalysisResult result = new AnalysisResult();
                result.setSbomDocument(sbomDocument);
                result.setVulnerabilityReport(vulnerabilityFuture.get());
                result.setAiAnalysisResult(aiAnalysisFuture.get());
                result.setPolicyViolations(policyFuture.get());
                result.setAnalysisStatus(AnalysisStatus.COMPLETED);

                logger.info("SBOM analysis completed successfully for document: {}", 
                    sbomDocument.getDocumentName());
                
                return result;

            } catch (Exception e) {
                logger.error("SBOM analysis failed", e);
                AnalysisResult errorResult = new AnalysisResult();
                errorResult.setAnalysisStatus(AnalysisStatus.FAILED);
                errorResult.setErrorMessage(e.getMessage());
                return errorResult;
            }
        }, analysisExecutor);
    }

    /**
     * Performs a complete analysis of an SBOM document with custom parameters.
     * 
     * @param inputStream The input stream containing the SBOM data
     * @param format The expected format of the SBOM
     * @param analysisRequest Custom analysis parameters
     * @return CompletableFuture containing the analysis result
     */
    public CompletableFuture<AnalysisResult> analyzeSbom(InputStream inputStream, SbomFormat format, AnalysisRequest analysisRequest) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                logger.info("Starting custom SBOM analysis for format: {} with request: {}", format, analysisRequest);
                
                // Step 1: Parse the SBOM
                SbomDocument sbomDocument = parseSbom(inputStream, format);
                
                // Step 2: Perform parallel analysis with custom parameters
                CompletableFuture<VulnerabilityReport> vulnerabilityFuture = 
                    vulnerabilityScanner.scan(sbomDocument, analysisRequest.getVulnerabilitySources());
                
                CompletableFuture<AiAnalysisResult> aiAnalysisFuture = 
                    aiAnalyzer.analyze(sbomDocument, analysisRequest.getAnalysisParameters());
                
                CompletableFuture<List<PolicyViolation>> policyFuture = 
                    CompletableFuture.supplyAsync(() -> {
                        try {
                            return policyEnforcer.enforcePolicies(sbomDocument, analysisRequest.getPolicyTypes());
                        } catch (PolicyEnforcementException e) {
                            logger.error("Policy enforcement failed", e);
                            throw new RuntimeException(e);
                        }
                    }, analysisExecutor);

                // Step 3: Wait for all analysis to complete
                CompletableFuture<Void> allAnalysis = CompletableFuture.allOf(
                    vulnerabilityFuture, aiAnalysisFuture, policyFuture
                );

                allAnalysis.join();

                // Step 4: Build the complete analysis result
                AnalysisResult result = new AnalysisResult();
                result.setSbomDocument(sbomDocument);
                result.setVulnerabilityReport(vulnerabilityFuture.get());
                result.setAiAnalysisResult(aiAnalysisFuture.get());
                result.setPolicyViolations(policyFuture.get());
                result.setAnalysisStatus(AnalysisStatus.COMPLETED);

                logger.info("Custom SBOM analysis completed successfully for document: {}", 
                    sbomDocument.getDocumentName());
                
                return result;

            } catch (Exception e) {
                logger.error("Custom SBOM analysis failed", e);
                AnalysisResult errorResult = new AnalysisResult();
                errorResult.setAnalysisStatus(AnalysisStatus.FAILED);
                errorResult.setErrorMessage(e.getMessage());
                return errorResult;
            }
        }, analysisExecutor);
    }

    /**
     * Parses an SBOM document from an input stream.
     * 
     * @param inputStream The input stream containing the SBOM data
     * @param format The expected format of the SBOM
     * @return The parsed SBOM document
     * @throws RuntimeException if parsing fails
     */
    private SbomDocument parseSbom(InputStream inputStream, SbomFormat format) {
        try {
            return sbomParser.parse(inputStream, format)
                .orElseThrow(() -> new RuntimeException("Failed to parse SBOM document"));
        } catch (SbomParsingException e) {
            logger.error("SBOM parsing failed", e);
            throw new RuntimeException("Failed to parse SBOM document", e);
        }
    }

    /**
     * Gets the health status of all analysis components.
     * 
     * @return Health status information
     */
    public HealthStatus getHealthStatus() {
        HealthStatus status = new HealthStatus();
        status.setSbomParserAvailable(sbomParser != null);
        status.setVulnerabilityScannerAvailable(vulnerabilityScanner != null && vulnerabilityScanner.isAvailable());
        status.setAiAnalyzerAvailable(aiAnalyzer != null && aiAnalyzer.isAvailable());
        status.setPolicyEnforcerAvailable(policyEnforcer != null && policyEnforcer.isAvailable());
        return status;
    }

    /**
     * Gets the capabilities of all analysis components.
     * 
     * @return Capabilities information
     */
    public Capabilities getCapabilities() {
        Capabilities capabilities = new Capabilities();
        
        if (sbomParser != null) {
            capabilities.setSupportedSbomFormats(sbomParser.getSupportedFormats());
        }
        
        if (vulnerabilityScanner != null) {
            capabilities.setVulnerabilitySources(vulnerabilityScanner.getAvailableSources());
            capabilities.setScannerInfo(vulnerabilityScanner.getScannerInfo());
        }
        
        if (aiAnalyzer != null) {
            capabilities.setAiModels(aiAnalyzer.getAvailableModels());
            capabilities.setAnalyzerInfo(aiAnalyzer.getAnalyzerInfo());
        }
        
        if (policyEnforcer != null) {
            capabilities.setPolicyTypes(policyEnforcer.getAvailablePolicyTypes());
            capabilities.setPolicyConfiguration(policyEnforcer.getPolicyConfiguration());
        }
        
        return capabilities;
    }
} 