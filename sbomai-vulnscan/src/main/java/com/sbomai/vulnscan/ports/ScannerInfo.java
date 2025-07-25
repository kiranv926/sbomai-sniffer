package com.sbomai.vulnscan.ports;

import com.sbomai.vulnscan.domain.VulnerabilitySource;

import java.util.List;

/**
 * Information about a vulnerability scanner.
 */
public class ScannerInfo {
    
    private final String name;
    private final String version;
    private final String description;
    private final List<VulnerabilitySource> supportedSources;
    private final boolean available;
    private final String lastUpdated;
    
    public ScannerInfo(String name, String version, String description, 
                      List<VulnerabilitySource> supportedSources, boolean available, String lastUpdated) {
        this.name = name;
        this.version = version;
        this.description = description;
        this.supportedSources = supportedSources;
        this.available = available;
        this.lastUpdated = lastUpdated;
    }
    
    public String getName() { return name; }
    public String getVersion() { return version; }
    public String getDescription() { return description; }
    public List<VulnerabilitySource> getSupportedSources() { return supportedSources; }
    public boolean isAvailable() { return available; }
    public String getLastUpdated() { return lastUpdated; }
    
    @Override
    public String toString() {
        return String.format("ScannerInfo{name='%s', version='%s', available=%s, sources=%s}",
                name, version, available, supportedSources);
    }
} 