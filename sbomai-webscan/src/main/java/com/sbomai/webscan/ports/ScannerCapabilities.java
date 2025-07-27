package com.sbomai.webscan.ports;

import java.util.Arrays;
import java.util.List;

/**
 * Information about scanner capabilities and supported features.
 */
public class ScannerCapabilities {
    private final String scannerName;
    private final String version;
    private final List<String> supportedFeatures;
    private final List<String> supportedFormats;
    private final int maxConcurrentScans;
    private final long maxScanTimeout;
    private final boolean supportsCustomHeaders;
    private final boolean supportsAuthentication;
    private final boolean supportsProxy;

    public ScannerCapabilities(String scannerName, String version, List<String> supportedFeatures,
                              List<String> supportedFormats, int maxConcurrentScans, long maxScanTimeout,
                              boolean supportsCustomHeaders, boolean supportsAuthentication, boolean supportsProxy) {
        this.scannerName = scannerName;
        this.version = version;
        this.supportedFeatures = supportedFeatures;
        this.supportedFormats = supportedFormats;
        this.maxConcurrentScans = maxConcurrentScans;
        this.maxScanTimeout = maxScanTimeout;
        this.supportsCustomHeaders = supportsCustomHeaders;
        this.supportsAuthentication = supportsAuthentication;
        this.supportsProxy = supportsProxy;
    }

    public String getScannerName() { return scannerName; }
    public String getVersion() { return version; }
    public List<String> getSupportedFeatures() { return supportedFeatures; }
    public List<String> getSupportedFormats() { return supportedFormats; }
    public int getMaxConcurrentScans() { return maxConcurrentScans; }
    public long getMaxScanTimeout() { return maxScanTimeout; }
    public boolean isSupportsCustomHeaders() { return supportsCustomHeaders; }
    public boolean isSupportsAuthentication() { return supportsAuthentication; }
    public boolean isSupportsProxy() { return supportsProxy; }

    public static ScannerCapabilities defaultCapabilities() {
        return new ScannerCapabilities(
            "SBOMAI Web Scanner",
            "1.0.0",
            Arrays.asList(
                "JavaScript Library Detection",
                "Security Header Analysis",
                "Metadata Detection",
                "Vulnerability Scanning",
                "SSL/TLS Analysis",
                "Content Security Policy Analysis"
            ),
            Arrays.asList("HTML", "JavaScript", "CSS", "JSON", "XML"),
            10,
            300000, // 5 minutes
            true,
            true,
            true
        );
    }

    @Override
    public String toString() {
        return "ScannerCapabilities{" +
                "scannerName='" + scannerName + '\'' +
                ", version='" + version + '\'' +
                ", supportedFeatures=" + supportedFeatures +
                ", maxConcurrentScans=" + maxConcurrentScans +
                '}';
    }
} 