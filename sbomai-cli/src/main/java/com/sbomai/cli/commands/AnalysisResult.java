package com.sbomai.cli.commands;

import com.sbomai.core.domain.*;

/**
 * Result object for CLI SBOM analysis.
 */
public class AnalysisResult {
    private SbomDocument sbomDocument;
    private VulnerabilityReport vulnerabilityReport;
    private AiAnalysisResult aiAnalysisResult;
    private java.util.List<PolicyViolation> policyViolations;
    private boolean successful;
    private String errorMessage;

    // Getters and Setters
    public SbomDocument getSbomDocument() { return sbomDocument; }
    public void setSbomDocument(SbomDocument sbomDocument) { this.sbomDocument = sbomDocument; }

    public VulnerabilityReport getVulnerabilityReport() { return vulnerabilityReport; }
    public void setVulnerabilityReport(VulnerabilityReport vulnerabilityReport) { this.vulnerabilityReport = vulnerabilityReport; }

    public AiAnalysisResult getAiAnalysisResult() { return aiAnalysisResult; }
    public void setAiAnalysisResult(AiAnalysisResult aiAnalysisResult) { this.aiAnalysisResult = aiAnalysisResult; }

    public java.util.List<PolicyViolation> getPolicyViolations() { return policyViolations; }
    public void setPolicyViolations(java.util.List<PolicyViolation> policyViolations) { this.policyViolations = policyViolations; }

    public boolean isSuccessful() { return successful; }
    public void setSuccessful(boolean successful) { this.successful = successful; }

    public String getErrorMessage() { return errorMessage; }
    public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }
} 