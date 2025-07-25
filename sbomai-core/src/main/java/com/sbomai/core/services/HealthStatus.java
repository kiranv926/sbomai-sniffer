package com.sbomai.core.services;

import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * Health status information for all analysis components.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public class HealthStatus {
    private boolean sbomParserAvailable;
    private boolean vulnerabilityScannerAvailable;
    private boolean aiAnalyzerAvailable;
    private boolean policyEnforcerAvailable;
    private String overallStatus;

    public HealthStatus() {}

    // Getters and Setters
    public boolean isSbomParserAvailable() { return sbomParserAvailable; }
    public void setSbomParserAvailable(boolean sbomParserAvailable) { this.sbomParserAvailable = sbomParserAvailable; }

    public boolean isVulnerabilityScannerAvailable() { return vulnerabilityScannerAvailable; }
    public void setVulnerabilityScannerAvailable(boolean vulnerabilityScannerAvailable) { this.vulnerabilityScannerAvailable = vulnerabilityScannerAvailable; }

    public boolean isAiAnalyzerAvailable() { return aiAnalyzerAvailable; }
    public void setAiAnalyzerAvailable(boolean aiAnalyzerAvailable) { this.aiAnalyzerAvailable = aiAnalyzerAvailable; }

    public boolean isPolicyEnforcerAvailable() { return policyEnforcerAvailable; }
    public void setPolicyEnforcerAvailable(boolean policyEnforcerAvailable) { this.policyEnforcerAvailable = policyEnforcerAvailable; }

    public String getOverallStatus() { return overallStatus; }
    public void setOverallStatus(String overallStatus) { this.overallStatus = overallStatus; }

    // Business methods
    public boolean isFullyOperational() {
        return sbomParserAvailable && vulnerabilityScannerAvailable && 
               aiAnalyzerAvailable && policyEnforcerAvailable;
    }

    public int getAvailableComponentsCount() {
        int count = 0;
        if (sbomParserAvailable) count++;
        if (vulnerabilityScannerAvailable) count++;
        if (aiAnalyzerAvailable) count++;
        if (policyEnforcerAvailable) count++;
        return count;
    }

    @Override
    public String toString() {
        return "HealthStatus{" +
                "sbomParserAvailable=" + sbomParserAvailable +
                ", vulnerabilityScannerAvailable=" + vulnerabilityScannerAvailable +
                ", aiAnalyzerAvailable=" + aiAnalyzerAvailable +
                ", policyEnforcerAvailable=" + policyEnforcerAvailable +
                ", overallStatus='" + overallStatus + '\'' +
                '}';
    }
} 