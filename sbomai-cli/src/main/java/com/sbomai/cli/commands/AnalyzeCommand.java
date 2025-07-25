package com.sbomai.cli.commands;

import com.sbomai.cli.services.CliAnalysisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import picocli.CommandLine;

import java.io.File;
import java.util.concurrent.Callable;

/**
 * CLI command for analyzing SBOM files.
 */
@Component
@CommandLine.Command(
    name = "analyze",
    description = "Analyze an SBOM file for vulnerabilities, policy violations, and AI insights",
    mixinStandardHelpOptions = true
)
public class AnalyzeCommand implements Callable<Integer> {

    @Autowired
    private CliAnalysisService analysisService;

    @CommandLine.Parameters(
        index = "0",
        description = "Path to the SBOM file to analyze",
        arity = "1"
    )
    private File sbomFile;

    @CommandLine.Option(
        names = {"-f", "--format"},
        description = "SBOM format (SPDX, CYCLONEDX, SWID). Auto-detected if not specified.",
        defaultValue = "AUTO"
    )
    private String format;

    @CommandLine.Option(
        names = {"-o", "--output"},
        description = "Output format (JSON, TEXT, HTML). Default: TEXT",
        defaultValue = "TEXT"
    )
    private String outputFormat;

    @CommandLine.Option(
        names = {"-r", "--remote"},
        description = "Use remote SBOMAI core service instead of local analysis"
    )
    private boolean useRemote;

    @CommandLine.Option(
        names = {"-u", "--url"},
        description = "Remote SBOMAI core service URL (default: http://localhost:8080)",
        defaultValue = "http://localhost:8080"
    )
    private String remoteUrl;

    @CommandLine.Option(
        names = {"-v", "--verbose"},
        description = "Enable verbose output"
    )
    private boolean verbose;

    @CommandLine.Option(
        names = {"--no-ai"},
        description = "Skip AI analysis"
    )
    private boolean skipAiAnalysis;

    @CommandLine.Option(
        names = {"--no-vulnerability-scan"},
        description = "Skip vulnerability scanning"
    )
    private boolean skipVulnerabilityScan;

    @CommandLine.Option(
        names = {"--no-policy-check"},
        description = "Skip policy enforcement"
    )
    private boolean skipPolicyCheck;

    @Override
    public Integer call() throws Exception {
        try {
            System.out.println("🔍 SBOMAI Analysis Starting...");
            System.out.println("📁 File: " + sbomFile.getAbsolutePath());
            System.out.println("📋 Format: " + format);
            System.out.println("🌐 Mode: " + (useRemote ? "Remote (" + remoteUrl + ")" : "Local"));
            System.out.println();

            if (!sbomFile.exists()) {
                System.err.println("❌ Error: SBOM file not found: " + sbomFile.getAbsolutePath());
                return 1;
            }

            // Create analysis request
            AnalysisRequest request = new AnalysisRequest();
            request.setSbomFile(sbomFile);
            request.setFormat(format);
            request.setOutputFormat(outputFormat);
            request.setUseRemote(useRemote);
            request.setRemoteUrl(remoteUrl);
            request.setVerbose(verbose);
            request.setSkipAiAnalysis(skipAiAnalysis);
            request.setSkipVulnerabilityScan(skipVulnerabilityScan);
            request.setSkipPolicyCheck(skipPolicyCheck);

            // Perform analysis
            AnalysisResult result = analysisService.analyzeSbom(request);

            // Display results
            displayResults(result);

            return result.isSuccessful() ? 0 : 1;

        } catch (Exception e) {
            System.err.println("❌ Analysis failed: " + e.getMessage());
            if (verbose) {
                e.printStackTrace();
            }
            return 1;
        }
    }

    private void displayResults(AnalysisResult result) {
        System.out.println("📊 Analysis Results:");
        System.out.println("===================");
        
        if (result.getSbomDocument() != null) {
            System.out.println("📄 SBOM Document: " + result.getSbomDocument().getDocumentName());
            System.out.println("📦 Components: " + result.getSbomDocument().getComponents().size());
        }

        if (result.getVulnerabilityReport() != null) {
            System.out.println("🔒 Vulnerabilities: " + result.getVulnerabilityReport().getTotalVulnerabilities());
            if (result.getVulnerabilityReport().getCriticalCount() != null && result.getVulnerabilityReport().getCriticalCount() > 0) {
                System.out.println("⚠️  Critical: " + result.getVulnerabilityReport().getCriticalCount());
            }
            if (result.getVulnerabilityReport().getHighCount() != null && result.getVulnerabilityReport().getHighCount() > 0) {
                System.out.println("🚨 High: " + result.getVulnerabilityReport().getHighCount());
            }
        }

        if (result.getPolicyViolations() != null && !result.getPolicyViolations().isEmpty()) {
            System.out.println("📋 Policy Violations: " + result.getPolicyViolations().size());
            long blockingViolations = result.getPolicyViolations().stream()
                .filter(v -> v.isBlockingViolation())
                .count();
            if (blockingViolations > 0) {
                System.out.println("🚫 Blocking: " + blockingViolations);
            }
        }

        if (result.getAiAnalysisResult() != null) {
            System.out.println("🤖 AI Risk Level: " + result.getAiAnalysisResult().getRiskLevel());
            System.out.println("📈 Risk Score: " + result.getAiAnalysisResult().getRiskScore());
        }

        System.out.println();
        System.out.println("✅ Analysis completed successfully!");
    }
} 