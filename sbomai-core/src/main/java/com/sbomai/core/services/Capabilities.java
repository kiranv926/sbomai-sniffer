package com.sbomai.core.services;

import com.sbomai.core.domain.SbomFormat;
import com.sbomai.core.ports.*;
import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * Capabilities information for all analysis components.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Capabilities {
    private SbomFormat[] supportedSbomFormats;
    private String[] vulnerabilitySources;
    private ScannerInfo scannerInfo;
    private String[] aiModels;
    private AnalyzerInfo analyzerInfo;
    private String[] policyTypes;
    private PolicyConfiguration policyConfiguration;

    public Capabilities() {}

    // Getters and Setters
    public SbomFormat[] getSupportedSbomFormats() { return supportedSbomFormats; }
    public void setSupportedSbomFormats(SbomFormat[] supportedSbomFormats) { this.supportedSbomFormats = supportedSbomFormats; }

    public String[] getVulnerabilitySources() { return vulnerabilitySources; }
    public void setVulnerabilitySources(String[] vulnerabilitySources) { this.vulnerabilitySources = vulnerabilitySources; }

    public ScannerInfo getScannerInfo() { return scannerInfo; }
    public void setScannerInfo(ScannerInfo scannerInfo) { this.scannerInfo = scannerInfo; }

    public String[] getAiModels() { return aiModels; }
    public void setAiModels(String[] aiModels) { this.aiModels = aiModels; }

    public AnalyzerInfo getAnalyzerInfo() { return analyzerInfo; }
    public void setAnalyzerInfo(AnalyzerInfo analyzerInfo) { this.analyzerInfo = analyzerInfo; }

    public String[] getPolicyTypes() { return policyTypes; }
    public void setPolicyTypes(String[] policyTypes) { this.policyTypes = policyTypes; }

    public PolicyConfiguration getPolicyConfiguration() { return policyConfiguration; }
    public void setPolicyConfiguration(PolicyConfiguration policyConfiguration) { this.policyConfiguration = policyConfiguration; }

    @Override
    public String toString() {
        return "Capabilities{" +
                "supportedSbomFormats=" + (supportedSbomFormats != null ? supportedSbomFormats.length : 0) +
                ", vulnerabilitySources=" + (vulnerabilitySources != null ? vulnerabilitySources.length : 0) +
                ", aiModels=" + (aiModels != null ? aiModels.length : 0) +
                ", policyTypes=" + (policyTypes != null ? policyTypes.length : 0) +
                '}';
    }
} 