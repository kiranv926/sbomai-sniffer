package com.sbomai.core.ports;

/**
 * Information about an AI analyzer.
 */
public class AnalyzerInfo {
    private final String name;
    private final String version;
    private final String[] supportedModels;
    private final boolean isAvailable;
    private final String provider;

    public AnalyzerInfo(String name, String version, String[] supportedModels, boolean isAvailable, String provider) {
        this.name = name;
        this.version = version;
        this.supportedModels = supportedModels;
        this.isAvailable = isAvailable;
        this.provider = provider;
    }

    public String getName() {
        return name;
    }

    public String getVersion() {
        return version;
    }

    public String[] getSupportedModels() {
        return supportedModels;
    }

    public boolean isAvailable() {
        return isAvailable;
    }

    public String getProvider() {
        return provider;
    }

    @Override
    public String toString() {
        return "AnalyzerInfo{" +
                "name='" + name + '\'' +
                ", version='" + version + '\'' +
                ", provider='" + provider + '\'' +
                ", isAvailable=" + isAvailable +
                '}';
    }
} 