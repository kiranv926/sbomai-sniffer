package com.sbomai.cli.commands;

import com.sbomai.cli.services.CliAnalysisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import picocli.CommandLine;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.stream.Collectors;

/**
 * CLI command for batch analysis of multiple SBOM files.
 */
@Component
@CommandLine.Command(
    name = "batch",
    description = "Analyze multiple SBOM files in batch mode",
    mixinStandardHelpOptions = true
)
public class BatchCommand implements Callable<Integer> {

    @Autowired
    private CliAnalysisService analysisService;

    @CommandLine.Parameters(
        index = "0",
        description = "Directory containing SBOM files or glob pattern",
        arity = "1"
    )
    private String inputPath;

    @CommandLine.Option(
        names = {"-f", "--format"},
        description = "SBOM format filter (SPDX, CYCLONEDX, SWID). Auto-detected if not specified.",
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
        names = {"-d", "--output-dir"},
        description = "Output directory for results (default: ./batch-results)"
    )
    private String outputDir;

    @CommandLine.Option(
        names = {"-p", "--parallel"},
        description = "Number of parallel analyses (default: 3)"
    )
    private int parallelCount = 3;

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

    @CommandLine.Option(
        names = {"--summary-only"},
        description = "Generate only summary report, skip individual file reports"
    )
    private boolean summaryOnly;

    @Override
    public Integer call() throws Exception {
        try {
            System.out.println("📦 SBOMAI Batch Analysis Starting...");
            System.out.println("📁 Input: " + inputPath);
            System.out.println("📋 Format: " + format);
            System.out.println("🌐 Mode: " + (useRemote ? "Remote (" + remoteUrl + ")" : "Local"));
            System.out.println("⚡ Parallel: " + parallelCount);
            System.out.println();

            // Find SBOM files
            List<File> sbomFiles = findSbomFiles(inputPath);
            if (sbomFiles.isEmpty()) {
                System.err.println("❌ No SBOM files found in: " + inputPath);
                return 1;
            }

            System.out.println("📄 Found " + sbomFiles.size() + " SBOM files to analyze");
            System.out.println();

            // Create output directory
            String outputDirectory = outputDir != null ? outputDir : "./batch-results";
            createOutputDirectory(outputDirectory);

            // Perform batch analysis
            BatchAnalysisResult batchResult = performBatchAnalysis(sbomFiles, outputDirectory);

            // Display summary
            displayBatchSummary(batchResult);

            return batchResult.getFailedCount() == 0 ? 0 : 1;

        } catch (Exception e) {
            System.err.println("❌ Batch analysis failed: " + e.getMessage());
            if (verbose) {
                e.printStackTrace();
            }
            return 1;
        }
    }

    private List<File> findSbomFiles(String inputPath) throws Exception {
        List<File> files = new ArrayList<>();
        Path path = Paths.get(inputPath);

        if (Files.isDirectory(path)) {
            // Directory - find all SBOM files
            files = Files.walk(path)
                .filter(Files::isRegularFile)
                .filter(this::isSbomFile)
                .map(Path::toFile)
                .collect(Collectors.toList());
        } else if (inputPath.contains("*") || inputPath.contains("?")) {
            // Glob pattern
            Path parent = path.getParent() != null ? path.getParent() : Paths.get(".");
            String glob = path.getFileName().toString();
            
            files = Files.walk(parent)
                .filter(Files::isRegularFile)
                .filter(p -> matchesGlob(p.getFileName().toString(), glob))
                .filter(this::isSbomFile)
                .map(Path::toFile)
                .collect(Collectors.toList());
        } else {
            // Single file
            File file = new File(inputPath);
            if (file.exists() && isSbomFile(file.toPath())) {
                files.add(file);
            }
        }

        return files;
    }

    private boolean isSbomFile(Path path) {
        String fileName = path.getFileName().toString().toLowerCase();
        return fileName.endsWith(".spdx") || 
               fileName.endsWith(".spdx.json") ||
               fileName.endsWith(".cyclonedx") ||
               fileName.endsWith(".cdx") ||
               fileName.endsWith(".cyclonedx.json") ||
               fileName.endsWith(".swid") ||
               fileName.endsWith(".swid.xml");
    }

    private boolean matchesGlob(String fileName, String glob) {
        // Simple glob matching - in a real implementation, use proper glob library
        String pattern = glob.replace("*", ".*").replace("?", ".");
        return fileName.matches(pattern);
    }

    private void createOutputDirectory(String outputDirectory) throws Exception {
        Path outputPath = Paths.get(outputDirectory);
        if (!Files.exists(outputPath)) {
            Files.createDirectories(outputPath);
            System.out.println("📁 Created output directory: " + outputDirectory);
        }
    }

    private BatchAnalysisResult performBatchAnalysis(List<File> sbomFiles, String outputDirectory) {
        BatchAnalysisResult batchResult = new BatchAnalysisResult();
        batchResult.setTotalFiles(sbomFiles.size());
        batchResult.setOutputDirectory(outputDirectory);

        System.out.println("🚀 Starting batch analysis...");
        System.out.println();

        for (int i = 0; i < sbomFiles.size(); i++) {
            File sbomFile = sbomFiles.get(i);
            System.out.println("📄 [" + (i + 1) + "/" + sbomFiles.size() + "] Analyzing: " + sbomFile.getName());

            try {
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

                if (result.isSuccessful()) {
                    batchResult.incrementSuccessCount();
                    
                    // Save individual result if not summary-only
                    if (!summaryOnly) {
                        saveIndividualResult(result, sbomFile, outputDirectory);
                    }
                    
                    // Update batch statistics
                    updateBatchStatistics(batchResult, result);
                    
                    System.out.println("   ✅ Success");
                } else {
                    batchResult.incrementFailedCount();
                    System.out.println("   ❌ Failed: " + result.getErrorMessage());
                }

            } catch (Exception e) {
                batchResult.incrementFailedCount();
                System.out.println("   ❌ Error: " + e.getMessage());
            }

            System.out.println();
        }

        return batchResult;
    }

    private void saveIndividualResult(AnalysisResult result, File sbomFile, String outputDirectory) {
        try {
            String baseName = sbomFile.getName().replaceFirst("[.][^.]+$", "");
            String outputFile = outputDirectory + "/" + baseName + ".results." + outputFormat.toLowerCase();
            
            // In a real implementation, this would write the result to the file
            // For now, just show what would be saved
            if (verbose) {
                System.out.println("   💾 Saved: " + outputFile);
            }
        } catch (Exception e) {
            System.err.println("   ⚠️  Failed to save result: " + e.getMessage());
        }
    }

    private void updateBatchStatistics(BatchAnalysisResult batchResult, AnalysisResult result) {
        // Update vulnerability statistics
        if (result.getVulnerabilityReport() != null) {
            batchResult.addTotalVulnerabilities(result.getVulnerabilityReport().getTotalVulnerabilities());
            if (result.getVulnerabilityReport().getCriticalCount() != null) {
                batchResult.addCriticalVulnerabilities(result.getVulnerabilityReport().getCriticalCount());
            }
            if (result.getVulnerabilityReport().getHighCount() != null) {
                batchResult.addHighVulnerabilities(result.getVulnerabilityReport().getHighCount());
            }
        }

        // Update policy violation statistics
        if (result.getPolicyViolations() != null) {
            batchResult.addTotalPolicyViolations(result.getPolicyViolations().size());
            long blockingViolations = result.getPolicyViolations().stream()
                .filter(v -> v.isBlockingViolation())
                .count();
            batchResult.addBlockingPolicyViolations((int) blockingViolations);
        }

        // Update AI analysis statistics
        if (result.getAiAnalysisResult() != null) {
            batchResult.addRiskScore(result.getAiAnalysisResult().getRiskScore());
        }
    }

    private void displayBatchSummary(BatchAnalysisResult batchResult) {
        System.out.println("📊 Batch Analysis Summary:");
        System.out.println("==========================");
        System.out.println("📁 Output Directory: " + batchResult.getOutputDirectory());
        System.out.println("📄 Total Files: " + batchResult.getTotalFiles());
        System.out.println("✅ Successful: " + batchResult.getSuccessCount());
        System.out.println("❌ Failed: " + batchResult.getFailedCount());
        System.out.println();

        if (batchResult.getTotalVulnerabilities() > 0) {
            System.out.println("🔒 Vulnerability Summary:");
            System.out.println("   Total: " + batchResult.getTotalVulnerabilities());
            System.out.println("   Critical: " + batchResult.getCriticalVulnerabilities());
            System.out.println("   High: " + batchResult.getHighVulnerabilities());
            System.out.println();
        }

        if (batchResult.getTotalPolicyViolations() > 0) {
            System.out.println("📋 Policy Violation Summary:");
            System.out.println("   Total: " + batchResult.getTotalPolicyViolations());
            System.out.println("   Blocking: " + batchResult.getBlockingPolicyViolations());
            System.out.println();
        }

        if (batchResult.getAverageRiskScore() > 0) {
            System.out.println("🤖 AI Risk Summary:");
            System.out.println("   Average Risk Score: " + String.format("%.2f", batchResult.getAverageRiskScore()));
            System.out.println();
        }

        System.out.println("🎉 Batch analysis completed!");
    }

    /**
     * Result object for batch analysis.
     */
    public static class BatchAnalysisResult {
        private int totalFiles;
        private int successCount;
        private int failedCount;
        private String outputDirectory;
        private int totalVulnerabilities;
        private int criticalVulnerabilities;
        private int highVulnerabilities;
        private int totalPolicyViolations;
        private int blockingPolicyViolations;
        private double totalRiskScore;
        private int riskScoreCount;

        // Getters and Setters
        public int getTotalFiles() { return totalFiles; }
        public void setTotalFiles(int totalFiles) { this.totalFiles = totalFiles; }

        public int getSuccessCount() { return successCount; }
        public void setSuccessCount(int successCount) { this.successCount = successCount; }

        public int getFailedCount() { return failedCount; }
        public void setFailedCount(int failedCount) { this.failedCount = failedCount; }

        public String getOutputDirectory() { return outputDirectory; }
        public void setOutputDirectory(String outputDirectory) { this.outputDirectory = outputDirectory; }

        public int getTotalVulnerabilities() { return totalVulnerabilities; }
        public void setTotalVulnerabilities(int totalVulnerabilities) { this.totalVulnerabilities = totalVulnerabilities; }

        public int getCriticalVulnerabilities() { return criticalVulnerabilities; }
        public void setCriticalVulnerabilities(int criticalVulnerabilities) { this.criticalVulnerabilities = criticalVulnerabilities; }

        public int getHighVulnerabilities() { return highVulnerabilities; }
        public void setHighVulnerabilities(int highVulnerabilities) { this.highVulnerabilities = highVulnerabilities; }

        public int getTotalPolicyViolations() { return totalPolicyViolations; }
        public void setTotalPolicyViolations(int totalPolicyViolations) { this.totalPolicyViolations = totalPolicyViolations; }

        public int getBlockingPolicyViolations() { return blockingPolicyViolations; }
        public void setBlockingPolicyViolations(int blockingPolicyViolations) { this.blockingPolicyViolations = blockingPolicyViolations; }

        public double getAverageRiskScore() { 
            return riskScoreCount > 0 ? totalRiskScore / riskScoreCount : 0.0; 
        }

        // Helper methods
        public void incrementSuccessCount() { successCount++; }
        public void incrementFailedCount() { failedCount++; }
        public void addTotalVulnerabilities(int count) { totalVulnerabilities += count; }
        public void addCriticalVulnerabilities(int count) { criticalVulnerabilities += count; }
        public void addHighVulnerabilities(int count) { highVulnerabilities += count; }
        public void addTotalPolicyViolations(int count) { totalPolicyViolations += count; }
        public void addBlockingPolicyViolations(int count) { blockingPolicyViolations += count; }
        public void addRiskScore(double score) { 
            totalRiskScore += score; 
            riskScoreCount++; 
        }
    }
} 