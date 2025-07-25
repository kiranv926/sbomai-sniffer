package com.sbomai.core.services;

import com.sbomai.core.domain.*;
import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDateTime;
import java.util.List;

/**
 * Complete analysis result combining all SBOM analysis outputs.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AnalysisResult {
    private SbomDocument sbomDocument;
    private VulnerabilityReport vulnerabilityReport;
    private AiAnalysisResult aiAnalysisResult;
    private List<PolicyViolation> policyViolations;
    private AnalysisStatus analysisStatus;
    private String errorMessage;
    private LocalDateTime analysisDate;
    private Long analysisDurationMs;

    public AnalysisResult() {
        this.analysisDate = LocalDateTime.now();
    }

    // Getters and Setters
    public SbomDocument getSbomDocument() { return sbomDocument; }
    public void setSbomDocument(SbomDocument sbomDocument) { this.sbomDocument = sbomDocument; }

    public VulnerabilityReport getVulnerabilityReport() { return vulnerabilityReport; }
    public void setVulnerabilityReport(VulnerabilityReport vulnerabilityReport) { this.vulnerabilityReport = vulnerabilityReport; }

    public AiAnalysisResult getAiAnalysisResult() { return aiAnalysisResult; }
    public void setAiAnalysisResult(AiAnalysisResult aiAnalysisResult) { this.aiAnalysisResult = aiAnalysisResult; }

    public List<PolicyViolation> getPolicyViolations() { return policyViolations; }
    public void setPolicyViolations(List<PolicyViolation> policyViolations) { this.policyViolations = policyViolations; }

    public AnalysisStatus getAnalysisStatus() { return analysisStatus; }
    public void setAnalysisStatus(AnalysisStatus analysisStatus) { this.analysisStatus = analysisStatus; }

    public String getErrorMessage() { return errorMessage; }
    public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }

    public LocalDateTime getAnalysisDate() { return analysisDate; }
    public void setAnalysisDate(LocalDateTime analysisDate) { this.analysisDate = analysisDate; }

    public Long getAnalysisDurationMs() { return analysisDurationMs; }
    public void setAnalysisDurationMs(Long analysisDurationMs) { this.analysisDurationMs = analysisDurationMs; }

    // Business methods
    public boolean hasVulnerabilities() {
        return vulnerabilityReport != null && vulnerabilityReport.getTotalVulnerabilities() != null && 
               vulnerabilityReport.getTotalVulnerabilities() > 0;
    }

    public boolean hasCriticalVulnerabilities() {
        return vulnerabilityReport != null && vulnerabilityReport.hasCriticalVulnerabilities();
    }

    public boolean hasPolicyViolations() {
        return policyViolations != null && !policyViolations.isEmpty();
    }

    public boolean hasBlockingPolicyViolations() {
        return policyViolations != null && policyViolations.stream().anyMatch(PolicyViolation::isBlockingViolation);
    }

    public boolean isHighRisk() {
        return aiAnalysisResult != null && aiAnalysisResult.isHighRisk();
    }

    @Override
    public String toString() {
        return "AnalysisResult{" +
                "analysisStatus=" + analysisStatus +
                ", hasVulnerabilities=" + hasVulnerabilities() +
                ", hasPolicyViolations=" + hasPolicyViolations() +
                ", isHighRisk=" + isHighRisk() +
                '}';
    }
} 