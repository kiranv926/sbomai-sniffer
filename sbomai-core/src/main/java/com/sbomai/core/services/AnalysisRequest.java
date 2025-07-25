package com.sbomai.core.services;

import com.sbomai.core.ports.AnalysisParameters;
import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * Request object for custom SBOM analysis parameters.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AnalysisRequest {
    private String[] vulnerabilitySources;
    private AnalysisParameters analysisParameters;
    private String[] policyTypes;
    private boolean includeAiAnalysis = true;
    private boolean includeVulnerabilityScan = true;
    private boolean includePolicyEnforcement = true;

    public AnalysisRequest() {}

    // Getters and Setters
    public String[] getVulnerabilitySources() { return vulnerabilitySources; }
    public void setVulnerabilitySources(String[] vulnerabilitySources) { this.vulnerabilitySources = vulnerabilitySources; }

    public AnalysisParameters getAnalysisParameters() { return analysisParameters; }
    public void setAnalysisParameters(AnalysisParameters analysisParameters) { this.analysisParameters = analysisParameters; }

    public String[] getPolicyTypes() { return policyTypes; }
    public void setPolicyTypes(String[] policyTypes) { this.policyTypes = policyTypes; }

    public boolean isIncludeAiAnalysis() { return includeAiAnalysis; }
    public void setIncludeAiAnalysis(boolean includeAiAnalysis) { this.includeAiAnalysis = includeAiAnalysis; }

    public boolean isIncludeVulnerabilityScan() { return includeVulnerabilityScan; }
    public void setIncludeVulnerabilityScan(boolean includeVulnerabilityScan) { this.includeVulnerabilityScan = includeVulnerabilityScan; }

    public boolean isIncludePolicyEnforcement() { return includePolicyEnforcement; }
    public void setIncludePolicyEnforcement(boolean includePolicyEnforcement) { this.includePolicyEnforcement = includePolicyEnforcement; }

    @Override
    public String toString() {
        return "AnalysisRequest{" +
                "includeAiAnalysis=" + includeAiAnalysis +
                ", includeVulnerabilityScan=" + includeVulnerabilityScan +
                ", includePolicyEnforcement=" + includePolicyEnforcement +
                '}';
    }
} 