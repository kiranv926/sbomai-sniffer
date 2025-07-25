package com.sbomai.cli.commands;

import org.springframework.stereotype.Component;
import picocli.CommandLine;

import java.util.concurrent.Callable;

/**
 * CLI command for displaying version information.
 */
@Component
@CommandLine.Command(
    name = "version",
    description = "Display SBOMAI version information",
    mixinStandardHelpOptions = true
)
public class VersionCommand implements Callable<Integer> {

    @Override
    public Integer call() throws Exception {
        System.out.println("🔍 SBOMAI - AI-Powered SBOM Analysis Tool");
        System.out.println("==========================================");
        System.out.println("Version: 1.0.0-SNAPSHOT");
        System.out.println("Java Version: " + System.getProperty("java.version"));
        System.out.println("OS: " + System.getProperty("os.name") + " " + System.getProperty("os.version"));
        System.out.println();
        System.out.println("Features:");
        System.out.println("  • SBOM Parsing (SPDX, CycloneDX, SWID)");
        System.out.println("  • Vulnerability Scanning (NVD, OSS Index, OSV)");
        System.out.println("  • AI-Powered Risk Analysis");
        System.out.println("  • Policy Enforcement");
        System.out.println("  • Local and Remote Analysis");
        System.out.println();
        System.out.println("For more information, visit: https://github.com/your-org/sbomai-sniffer");
        
        return 0;
    }
} 