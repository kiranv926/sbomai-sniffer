package com.sbomai.cli;

import com.sbomai.cli.commands.AnalyzeCommand;
import com.sbomai.cli.commands.HealthCommand;
import com.sbomai.cli.commands.VersionCommand;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import picocli.CommandLine;

/**
 * Main CLI application for SBOMAI.
 * 
 * This application provides a command-line interface for SBOM analysis,
 * supporting both local analysis and remote API integration.
 */
@SpringBootApplication
public class SbomaiCliApplication {

    public static void main(String[] args) {
        SpringApplication.run(SbomaiCliApplication.class, args);
    }

    @Bean
    public CommandLineRunner commandLineRunner(CommandLine.IFactory factory) {
        return args -> {
            CommandLine commandLine = new CommandLine(new SbomaiCliCommand(), factory);
            commandLine.addSubcommand("analyze", new AnalyzeCommand());
            commandLine.addSubcommand("health", new HealthCommand());
            commandLine.addSubcommand("version", new VersionCommand());
            
            int exitCode = commandLine.execute(args);
            System.exit(exitCode);
        };
    }
} 