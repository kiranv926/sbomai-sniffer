package com.sbomai.webscan.ports;

import java.util.HashSet;
import java.util.Set;

/**
 * Configuration options for website scanning.
 */
public class ScanOptions {
    private boolean scanJavaScriptLibraries = true;
    private boolean scanSecurityHeaders = true;
    private boolean scanMetadata = true;
    private boolean scanVulnerabilities = true;
    private int timeoutSeconds = 30;
    private int maxRedirects = 5;
    private String userAgent = "SBOMAI-WebScanner/1.0";
    private Set<String> excludedPaths = new HashSet<>();
    private boolean followRedirects = true;
    private boolean verifySSL = true;
    private int maxDepth = 1;

    public ScanOptions() {}

    // Getters and Setters
    public boolean isScanJavaScriptLibraries() { return scanJavaScriptLibraries; }
    public void setScanJavaScriptLibraries(boolean scanJavaScriptLibraries) { this.scanJavaScriptLibraries = scanJavaScriptLibraries; }

    public boolean isScanSecurityHeaders() { return scanSecurityHeaders; }
    public void setScanSecurityHeaders(boolean scanSecurityHeaders) { this.scanSecurityHeaders = scanSecurityHeaders; }

    public boolean isScanMetadata() { return scanMetadata; }
    public void setScanMetadata(boolean scanMetadata) { this.scanMetadata = scanMetadata; }

    public boolean isScanVulnerabilities() { return scanVulnerabilities; }
    public void setScanVulnerabilities(boolean scanVulnerabilities) { this.scanVulnerabilities = scanVulnerabilities; }

    public int getTimeoutSeconds() { return timeoutSeconds; }
    public void setTimeoutSeconds(int timeoutSeconds) { this.timeoutSeconds = timeoutSeconds; }

    public int getMaxRedirects() { return maxRedirects; }
    public void setMaxRedirects(int maxRedirects) { this.maxRedirects = maxRedirects; }

    public String getUserAgent() { return userAgent; }
    public void setUserAgent(String userAgent) { this.userAgent = userAgent; }

    public Set<String> getExcludedPaths() { return excludedPaths; }
    public void setExcludedPaths(Set<String> excludedPaths) { this.excludedPaths = excludedPaths; }

    public boolean isFollowRedirects() { return followRedirects; }
    public void setFollowRedirects(boolean followRedirects) { this.followRedirects = followRedirects; }

    public boolean isVerifySSL() { return verifySSL; }
    public void setVerifySSL(boolean verifySSL) { this.verifySSL = verifySSL; }

    public int getMaxDepth() { return maxDepth; }
    public void setMaxDepth(int maxDepth) { this.maxDepth = maxDepth; }

    // Builder methods
    public ScanOptions withJavaScriptLibraries(boolean enabled) {
        this.scanJavaScriptLibraries = enabled;
        return this;
    }

    public ScanOptions withSecurityHeaders(boolean enabled) {
        this.scanSecurityHeaders = enabled;
        return this;
    }

    public ScanOptions withMetadata(boolean enabled) {
        this.scanMetadata = enabled;
        return this;
    }

    public ScanOptions withVulnerabilities(boolean enabled) {
        this.scanVulnerabilities = enabled;
        return this;
    }

    public ScanOptions withTimeout(int seconds) {
        this.timeoutSeconds = seconds;
        return this;
    }

    public ScanOptions withUserAgent(String userAgent) {
        this.userAgent = userAgent;
        return this;
    }

    public ScanOptions excludePath(String path) {
        this.excludedPaths.add(path);
        return this;
    }

    public static ScanOptions defaultOptions() {
        return new ScanOptions();
    }

    public static ScanOptions quickScan() {
        return new ScanOptions()
            .withTimeout(15)
            .withMaxDepth(0);
    }

    public static ScanOptions deepScan() {
        return new ScanOptions()
            .withTimeout(60)
            .withMaxDepth(3);
    }
} 