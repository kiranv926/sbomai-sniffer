package com.sbomai.cli;

import picocli.CommandLine;

/**
 * Main CLI command for SBOMAI.
 * 
 * This is the root command that provides help and version information.
 */
@CommandLine.Command(
    name = "sbomai",
    mixinStandardHelpOptions = true,
    version = "SBOMAI CLI 1.0.0",
    description = "AI-powered SBOM analysis tool",
    subcommands = {
        CommandLine.HelpCommand.class
    }
)
public class SbomaiCliCommand implements Runnable {

    @Override
    public void run() {
        // Show help if no subcommand is provided
        CommandLine.usage(this, System.out);
    }
} 