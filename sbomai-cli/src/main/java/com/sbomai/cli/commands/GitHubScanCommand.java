package com.sbomai.cli.commands;

import com.sbomai.cli.services.GitHubScanService;
import com.sbomai.cli.output.OutputFormatter;
import com.sbomai.cli.output.OutputFormat;
import picocli.CommandLine;

import java.nio.file.Path;
import java.util.concurrent.Callable;

/**
 * Command for scanning GitHub repositories with SBOMAI Engine.
 * This command clones repositories, generates SBOMs, and analyzes them using AI.
 */
@CommandLine.Command(
    name = "github-scan",
    description = "Scan GitHub repositories for vulnerabilities using AI-powered analysis",
    mixinStandardHelpOptions = true
)
public class GitHubScanCommand implements Callable<Integer> {

    @CommandLine.Parameters(
        index = "0",
        description = "GitHub repository URL to scan (e.g., https://github.com/user/repo)"
    )
    private String repositoryUrl;

    @CommandLine.Option(
        names = {"-o", "--output"},
        description = "Output format: JSON, TEXT, HTML (default: JSON)"
    )
    private OutputFormat outputFormat = OutputFormat.JSON;

    @CommandLine.Option(
        names = {"-f", "--output-file"},
        description = "Output file path (default: stdout)"
    )
    private Path outputFile;

    @CommandLine.Option(
        names = {"-b", "--branch"},
        description = "Git branch to scan (default: main/master)"
    )
    private String branch;

    @CommandLine.Option(
        names = {"-d", "--depth"},
        description = "Git clone depth (default: 1, use 0 for full history)"
    )
    private int cloneDepth = 1;

    @CommandLine.Option(
        names = {"--no-sbom-generation"},
        description = "Skip SBOM generation, only analyze existing SBOM files"
    )
    private boolean skipSbomGeneration = false;

    @CommandLine.Option(
        names = {"--sbom-generator"},
        description = "SBOM generator to use: CYCLONEDX, SYFT, TRIVY, AUTO (default: AUTO)"
    )
    private String sbomGenerator = "AUTO";

    @CommandLine.Option(
        names = {"--ai-model"},
        description = "AI model to use: LOCAL, OPENAI, ANTHROPIC, GOOGLE (default: LOCAL)"
    )
    private String aiModel = "LOCAL";

    @CommandLine.Option(
        names = {"--include-dev-deps"},
        description = "Include development dependencies in analysis"
    )
    private boolean includeDevDeps = false;

    @CommandLine.Option(
        names = {"--vulnerability-sources"},
        description = "Comma-separated list of vulnerability sources: NVD,GHSA,EXPLOITDB,CISA,MITRE,REDHAT,JFROG (default: all)"
    )
    private String vulnerabilitySources = "NVD,GHSA,EXPLOITDB,CISA,MITRE,REDHAT,JFROG";

    @CommandLine.Option(
        names = {"--risk-threshold"},
        description = "Risk threshold for reporting (0.0-10.0, default: 5.0)"
    )
    private double riskThreshold = 5.0;

    @CommandLine.Option(
        names = {"--timeout"},
        description = "Timeout in seconds for repository operations (default: 300)"
    )
    private int timeout = 300;

    @CommandLine.Option(
        names = {"-v", "--verbose"},
        description = "Enable verbose output"
    )
    private boolean verbose = false;

    @CommandLine.Option(
        names = {"--temp-dir"},
        description = "Temporary directory for cloning repositories"
    )
    private Path tempDir;

    @Override
    public Integer call() {
        try {
            System.out.println("🚀 SBOMAI Engine - GitHub Repository Scanner");
            System.out.println("=" * 50);
            System.out.println("Repository: " + repositoryUrl);
            System.out.println("Branch: " + (branch != null ? branch : "default"));
            System.out.println("AI Model: " + aiModel);
            System.out.println("Output Format: " + outputFormat);
            System.out.println();

            // Validate repository URL
            if (!isValidGitHubUrl(repositoryUrl)) {
                System.err.println("❌ Error: Invalid GitHub repository URL");
                System.err.println("   Expected format: https://github.com/user/repo");
                return 1;
            }

            // Create GitHub scan service
            GitHubScanService scanService = new GitHubScanService();
            
            // Configure scan options
            GitHubScanService.ScanOptions options = GitHubScanService.ScanOptions.builder()
                .repositoryUrl(repositoryUrl)
                .branch(branch)
                .cloneDepth(cloneDepth)
                .skipSbomGeneration(skipSbomGeneration)
                .sbomGenerator(sbomGenerator)
                .aiModel(aiModel)
                .includeDevDeps(includeDevDeps)
                .vulnerabilitySources(vulnerabilitySources.split(","))
                .riskThreshold(riskThreshold)
                .timeout(timeout)
                .verbose(verbose)
                .tempDir(tempDir)
                .build();

            // Execute scan
            GitHubScanService.ScanResult result = scanService.scanRepository(options);

            // Format and output results
            OutputFormatter formatter = new OutputFormatter();
            String formattedOutput = formatter.format(result, outputFormat);

            if (outputFile != null) {
                formatter.writeToFile(formattedOutput, outputFile, outputFormat);
                System.out.println("📄 Report saved to: " + outputFile.toAbsolutePath());
            } else {
                System.out.println("\n" + "=" * 60);
                System.out.println("ANALYSIS REPORT");
                System.out.println("=" * 60);
                System.out.println(formattedOutput);
            }

            // Return appropriate exit code based on risk level
            if (result.getOverallRisk().equals("CRITICAL") || result.getOverallRisk().equals("HIGH")) {
                System.out.println("\n⚠️  High-risk vulnerabilities detected!");
                return 2; // Exit code for high risk
            } else if (result.getOverallRisk().equals("MEDIUM")) {
                System.out.println("\n⚠️  Medium-risk vulnerabilities detected.");
                return 1; // Exit code for medium risk
            } else {
                System.out.println("\n✅ No high-risk vulnerabilities detected.");
                return 0; // Exit code for success
            }

        } catch (Exception e) {
            System.err.println("❌ Error scanning repository: " + e.getMessage());
            if (verbose) {
                e.printStackTrace();
            }
            return 1;
        }
    }

    private boolean isValidGitHubUrl(String url) {
        return url != null && 
               (url.startsWith("https://github.com/") || url.startsWith("http://github.com/")) &&
               url.split("/").length >= 5;
    }
} 