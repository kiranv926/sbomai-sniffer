package com.sbomai.cli;

import picocli.CommandLine;

import java.util.concurrent.Callable;

/**
 * Main CLI command for SBOMAI.
 * This serves as the root command that provides help and version information.
 */
@CommandLine.Command(
    name = "sbomai",
    description = "SBOMAI - AI-Powered Software Bill of Materials Analysis Tool",
    mixinStandardHelpOptions = true,
    version = "SBOMAI CLI 1.0.0-SNAPSHOT"
)
public class SbomaiCliCommand implements Callable<Integer> {

    @Override
    public Integer call() {
        // If no subcommand is provided, show help
        System.out.println("🔍 SBOMAI - AI-Powered SBOM Analysis Tool");
        System.out.println("==========================================");
        System.out.println();
        System.out.println("Available commands:");
        System.out.println("  analyze    - Analyze an SBOM file for vulnerabilities, policy violations, and AI insights");
        System.out.println("  batch      - Analyze multiple SBOM files in batch mode");
        System.out.println("  config     - View and manage CLI configuration settings");
        System.out.println("  health     - Check the health status of SBOMAI services");
        System.out.println("  version    - Display version information");
        System.out.println();
        System.out.println("Use 'sbomai <command> --help' for more information about a command.");
        System.out.println();
        System.out.println("Examples:");
        System.out.println("  sbomai analyze package.spdx.json");
        System.out.println("  sbomai batch --directory ./sboms --format JSON");
        System.out.println("  sbomai config --list");
        System.out.println("  sbomai health");
        return 0;
    }
} 