package com.sbomai.cli.services;

import com.sbomai.cli.commands.AnalysisRequest;
import com.sbomai.cli.commands.AnalysisResult;
import com.sbomai.core.domain.SbomFormat;
import com.sbomai.core.services.SbomAnalysisOrchestrator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.concurrent.ExecutionException;

/**
 * Service for handling CLI analysis requests.
 */
@Service
public class CliAnalysisService {

    private static final Logger logger = LoggerFactory.getLogger(CliAnalysisService.class);

    private final SbomAnalysisOrchestrator orchestrator;
    private final RemoteApiService remoteApiService;

    @Autowired
    public CliAnalysisService(SbomAnalysisOrchestrator orchestrator, RemoteApiService remoteApiService) {
        this.orchestrator = orchestrator;
        this.remoteApiService = remoteApiService;
    }

    /**
     * Analyzes an SBOM file using either local or remote services.
     * 
     * @param request The analysis request
     * @return Analysis result
     */
    public AnalysisResult analyzeSbom(AnalysisRequest request) {
        try {
            if (request.isUseRemote()) {
                return analyzeSbomRemote(request);
            } else {
                return analyzeSbomLocal(request);
            }
        } catch (Exception e) {
            logger.error("Analysis failed", e);
            AnalysisResult result = new AnalysisResult();
            result.setSuccessful(false);
            result.setErrorMessage(e.getMessage());
            return result;
        }
    }

    /**
     * Performs local SBOM analysis.
     * 
     * @param request The analysis request
     * @return Analysis result
     */
    private AnalysisResult analyzeSbomLocal(AnalysisRequest request) throws IOException, InterruptedException, ExecutionException {
        logger.info("Performing local SBOM analysis for file: {}", request.getSbomFile().getName());

        // Determine SBOM format
        SbomFormat format = determineSbomFormat(request.getFormat(), request.getSbomFile());

        // Perform analysis using local orchestrator
        try (FileInputStream fis = new FileInputStream(request.getSbomFile())) {
            var future = orchestrator.analyzeSbom(fis, format);
            var coreResult = future.get(); // Wait for completion

            // Convert to CLI result
            AnalysisResult result = new AnalysisResult();
            result.setSuccessful(coreResult.getAnalysisStatus() == com.sbomai.core.domain.AnalysisStatus.COMPLETED);
            result.setSbomDocument(coreResult.getSbomDocument());
            result.setVulnerabilityReport(coreResult.getVulnerabilityReport());
            result.setAiAnalysisResult(coreResult.getAiAnalysisResult());
            result.setPolicyViolations(coreResult.getPolicyViolations());
            result.setErrorMessage(coreResult.getErrorMessage());

            return result;
        }
    }

    /**
     * Performs remote SBOM analysis.
     * 
     * @param request The analysis request
     * @return Analysis result
     */
    private AnalysisResult analyzeSbomRemote(AnalysisRequest request) throws IOException {
        logger.info("Performing remote SBOM analysis for file: {}", request.getSbomFile().getName());

        // Use remote API service
        return remoteApiService.analyzeSbom(request);
    }

    /**
     * Determines the SBOM format from the request or file extension.
     * 
     * @param format The requested format
     * @param file The SBOM file
     * @return The determined SBOM format
     */
    private SbomFormat determineSbomFormat(String format, java.io.File file) {
        if (!"AUTO".equals(format)) {
            return SbomFormat.fromCode(format);
        }

        // Auto-detect based on file extension
        String fileName = file.getName().toLowerCase();
        if (fileName.endsWith(".spdx") || fileName.endsWith(".spdx.json")) {
            return SbomFormat.SPDX;
        } else if (fileName.endsWith(".cyclonedx") || fileName.endsWith(".cdx") || fileName.endsWith(".cyclonedx.json")) {
            return SbomFormat.CYCLONEDX;
        } else if (fileName.endsWith(".swid") || fileName.endsWith(".swid.xml")) {
            return SbomFormat.SWID;
        } else {
            // Default to SPDX if we can't determine
            logger.warn("Could not auto-detect SBOM format, defaulting to SPDX");
            return SbomFormat.SPDX;
        }
    }
} 