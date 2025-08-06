package com.sbomai.core.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import java.util.UUID;

public class VulnerabilitiesDetectedEvent {
    @JsonProperty("scan_id")
    private UUID scanId;
    
    @JsonProperty("vulnerabilities")
    private List<VulnerabilityData> vulnerabilities;
    
    @JsonProperty("analysis_summary")
    private AnalysisSummary analysisSummary;
    
    public VulnerabilitiesDetectedEvent() {}
    
    public VulnerabilitiesDetectedEvent(UUID scanId, List<VulnerabilityData> vulnerabilities, AnalysisSummary analysisSummary) {
        this.scanId = scanId;
        this.vulnerabilities = vulnerabilities;
        this.analysisSummary = analysisSummary;
    }
    
    // Getters and Setters
    public UUID getScanId() { return scanId; }
    public void setScanId(UUID scanId) { this.scanId = scanId; }
    
    public List<VulnerabilityData> getVulnerabilities() { return vulnerabilities; }
    public void setVulnerabilities(List<VulnerabilityData> vulnerabilities) { this.vulnerabilities = vulnerabilities; }
    
    public AnalysisSummary getAnalysisSummary() { return analysisSummary; }
    public void setAnalysisSummary(AnalysisSummary analysisSummary) { this.analysisSummary = analysisSummary; }
    
    public static class VulnerabilityData {
        @JsonProperty("cve_id")
        private String cveId;
        
        @JsonProperty("severity")
        private String severity;
        
        @JsonProperty("cvss_score")
        private Double cvssScore;
        
        @JsonProperty("description")
        private String description;
        
        @JsonProperty("affected_components")
        private List<String> affectedComponents;
        
        // Getters and Setters
        public String getCveId() { return cveId; }
        public void setCveId(String cveId) { this.cveId = cveId; }
        
        public String getSeverity() { return severity; }
        public void setSeverity(String severity) { this.severity = severity; }
        
        public Double getCvssScore() { return cvssScore; }
        public void setCvssScore(Double cvssScore) { this.cvssScore = cvssScore; }
        
        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
        
        public List<String> getAffectedComponents() { return affectedComponents; }
        public void setAffectedComponents(List<String> affectedComponents) { this.affectedComponents = affectedComponents; }
    }
    
    public static class AnalysisSummary {
        @JsonProperty("total_vulnerabilities")
        private Integer totalVulnerabilities;
        
        @JsonProperty("critical_count")
        private Integer criticalCount;
        
        @JsonProperty("high_count")
        private Integer highCount;
        
        @JsonProperty("medium_count")
        private Integer mediumCount;
        
        @JsonProperty("low_count")
        private Integer lowCount;
        
        @JsonProperty("overall_risk_score")
        private Double overallRiskScore;
        
        // Getters and Setters
        public Integer getTotalVulnerabilities() { return totalVulnerabilities; }
        public void setTotalVulnerabilities(Integer totalVulnerabilities) { this.totalVulnerabilities = totalVulnerabilities; }
        
        public Integer getCriticalCount() { return criticalCount; }
        public void setCriticalCount(Integer criticalCount) { this.criticalCount = criticalCount; }
        
        public Integer getHighCount() { return highCount; }
        public void setHighCount(Integer highCount) { this.highCount = highCount; }
        
        public Integer getMediumCount() { return mediumCount; }
        public void setMediumCount(Integer mediumCount) { this.mediumCount = mediumCount; }
        
        public Integer getLowCount() { return lowCount; }
        public void setLowCount(Integer lowCount) { this.lowCount = lowCount; }
        
        public Double getOverallRiskScore() { return overallRiskScore; }
        public void setOverallRiskScore(Double overallRiskScore) { this.overallRiskScore = overallRiskScore; }
    }
}
