package com.sbomai.cli;

import com.sbomai.cli.commands.AnalyzeCommand;
import com.sbomai.cli.commands.BatchCommand;
import com.sbomai.cli.commands.ConfigCommand;
import com.sbomai.cli.commands.HealthCommand;
import com.sbomai.cli.commands.VersionCommand;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
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
    public CommandLineRunner commandLineRunner(ApplicationContext context) {
        return args -> {
            CommandLine commandLine = new CommandLine(new SbomaiCliCommand());
            
            // Get command beans from Spring context to ensure dependency injection
            commandLine.addSubcommand("analyze", context.getBean(AnalyzeCommand.class));
            commandLine.addSubcommand("batch", context.getBean(BatchCommand.class));
            commandLine.addSubcommand("config", context.getBean(ConfigCommand.class));
            commandLine.addSubcommand("health", context.getBean(HealthCommand.class));
            commandLine.addSubcommand("version", context.getBean(VersionCommand.class));
            
            int exitCode = commandLine.execute(args);
            System.exit(exitCode);
        };
    }
} 