package com.sbomai.cli.commands;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import picocli.CommandLine;

import java.util.concurrent.Callable;

/**
 * CLI command for managing configuration settings.
 */
@Component
@CommandLine.Command(
    name = "config",
    description = "View and manage CLI configuration settings",
    mixinStandardHelpOptions = true
)
public class ConfigCommand implements Callable<Integer> {

    @Value("${sbomai.cli.default.remote-url:http://localhost:8080}")
    private String defaultRemoteUrl;

    @Value("${sbomai.cli.default.output-format:TEXT}")
    private String defaultOutputFormat;

    @Value("${sbomai.cli.default.timeout:300000}")
    private String defaultTimeout;

    @Value("${sbomai.cli.remote.connection-timeout:30000}")
    private String connectionTimeout;

    @Value("${sbomai.cli.remote.read-timeout:300000}")
    private String readTimeout;

    @Value("${sbomai.cli.remote.max-retries:3}")
    private String maxRetries;

    @CommandLine.Option(
        names = {"-s", "--set"},
        description = "Set a configuration value (format: key=value)"
    )
    private String setConfig;

    @CommandLine.Option(
        names = {"-g", "--get"},
        description = "Get a specific configuration value"
    )
    private String getConfig;

    @CommandLine.Option(
        names = {"-r", "--reset"},
        description = "Reset configuration to defaults"
    )
    private boolean resetConfig;

    @Override
    public Integer call() throws Exception {
        try {
            if (setConfig != null) {
                return setConfiguration(setConfig);
            } else if (getConfig != null) {
                return getConfiguration(getConfig);
            } else if (resetConfig) {
                return resetConfiguration();
            } else {
                return showConfiguration();
            }
        } catch (Exception e) {
            System.err.println("❌ Configuration error: " + e.getMessage());
            return 1;
        }
    }

    private Integer setConfiguration(String config) {
        String[] parts = config.split("=", 2);
        if (parts.length != 2) {
            System.err.println("❌ Invalid configuration format. Use: key=value");
            return 1;
        }

        String key = parts[0].trim();
        String value = parts[1].trim();

        // For now, just show what would be set (in a real implementation, this would persist)
        System.out.println("🔧 Setting configuration:");
        System.out.println("   Key: " + key);
        System.out.println("   Value: " + value);
        System.out.println("⚠️  Note: Configuration persistence not implemented yet");
        
        return 0;
    }

    private Integer getConfiguration(String key) {
        String value = getConfigValue(key);
        if (value != null) {
            System.out.println(value);
            return 0;
        } else {
            System.err.println("❌ Configuration key not found: " + key);
            return 1;
        }
    }

    private Integer resetConfiguration() {
        System.out.println("🔄 Resetting configuration to defaults...");
        System.out.println("⚠️  Note: Configuration reset not implemented yet");
        return 0;
    }

    private Integer showConfiguration() {
        System.out.println("🔧 SBOMAI CLI Configuration:");
        System.out.println("=============================");
        System.out.println();
        
        System.out.println("📡 Remote Settings:");
        System.out.println("   Default URL: " + defaultRemoteUrl);
        System.out.println("   Connection Timeout: " + connectionTimeout + "ms");
        System.out.println("   Read Timeout: " + readTimeout + "ms");
        System.out.println("   Max Retries: " + maxRetries);
        System.out.println();
        
        System.out.println("📋 Default Settings:");
        System.out.println("   Output Format: " + defaultOutputFormat);
        System.out.println("   Timeout: " + defaultTimeout + "ms");
        System.out.println();
        
        System.out.println("💡 Usage:");
        System.out.println("   sbomai config --get remote-url");
        System.out.println("   sbomai config --set remote-url=https://sbomai.company.com");
        System.out.println("   sbomai config --reset");
        
        return 0;
    }

    private String getConfigValue(String key) {
        switch (key.toLowerCase()) {
            case "remote-url":
            case "default.remote-url":
                return defaultRemoteUrl;
            case "output-format":
            case "default.output-format":
                return defaultOutputFormat;
            case "timeout":
            case "default.timeout":
                return defaultTimeout;
            case "connection-timeout":
            case "remote.connection-timeout":
                return connectionTimeout;
            case "read-timeout":
            case "remote.read-timeout":
                return readTimeout;
            case "max-retries":
            case "remote.max-retries":
                return maxRetries;
            default:
                return null;
        }
    }
} 