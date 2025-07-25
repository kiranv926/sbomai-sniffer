package com.sbomai.core.ports;

/**
 * Information about a vulnerability scanner.
 */
public class ScannerInfo {
    private final String name;
    private final String version;
    private final String[] supportedSources;
    private final boolean isAvailable;

    public ScannerInfo(String name, String version, String[] supportedSources, boolean isAvailable) {
        this.name = name;
        this.version = version;
        this.supportedSources = supportedSources;
        this.isAvailable = isAvailable;
    }

    public String getName() {
        return name;
    }

    public String getVersion() {
        return version;
    }

    public String[] getSupportedSources() {
        return supportedSources;
    }

    public boolean isAvailable() {
        return isAvailable;
    }

    @Override
    public String toString() {
        return "ScannerInfo{" +
                "name='" + name + '\'' +
                ", version='" + version + '\'' +
                ", isAvailable=" + isAvailable +
                '}';
    }
} 