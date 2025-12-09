package com.sbomai.core.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class AIAnalysisDto {
    
    private UUID id;
    
    private UUID sbomDocumentId;
    
    private String analysisType; // VULNERABILITY, RISK, COMPLIANCE, TREND
    
    private String status; // PENDING, IN_PROGRESS, COMPLETED, FAILED, PARTIAL
    
    private String modelUsed;
    
    private String modelVersion;
    
    private Double riskScore;
    
    private String riskLevel; // CRITICAL, HIGH, MEDIUM, LOW, NONE
    
    private Double confidenceScore;
    
    private String analysisSummary;
    
    private List<String> keyFindings;
    
    private List<String> recommendations;
    
    private String errorMessage;
    
    private Long analysisDurationMs;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime analysisDate;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime createdDate;
    
    // Constructors
    public AIAnalysisDto() {}
    
    public AIAnalysisDto(UUID id, UUID sbomDocumentId, String analysisType, String status, 
                        String modelUsed, Double riskScore, String riskLevel) {
        this.id = id;
        this.sbomDocumentId = sbomDocumentId;
        this.analysisType = analysisType;
        this.status = status;
        this.modelUsed = modelUsed;
        this.riskScore = riskScore;
        this.riskLevel = riskLevel;
    }
    
    // Getters and Setters
    public UUID getId() {
        return id;
    }
    
    public void setId(UUID id) {
        this.id = id;
    }
    
    public UUID getSbomDocumentId() {
        return sbomDocumentId;
    }
    
    public void setSbomDocumentId(UUID sbomDocumentId) {
        this.sbomDocumentId = sbomDocumentId;
    }
    
    public String getAnalysisType() {
        return analysisType;
    }
    
    public void setAnalysisType(String analysisType) {
        this.analysisType = analysisType;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public String getModelUsed() {
        return modelUsed;
    }
    
    public void setModelUsed(String modelUsed) {
        this.modelUsed = modelUsed;
    }
    
    public String getModelVersion() {
        return modelVersion;
    }
    
    public void setModelVersion(String modelVersion) {
        this.modelVersion = modelVersion;
    }
    
    public Double getRiskScore() {
        return riskScore;
    }
    
    public void setRiskScore(Double riskScore) {
        this.riskScore = riskScore;
    }
    
    public String getRiskLevel() {
        return riskLevel;
    }
    
    public void setRiskLevel(String riskLevel) {
        this.riskLevel = riskLevel;
    }
    
    public Double getConfidenceScore() {
        return confidenceScore;
    }
    
    public void setConfidenceScore(Double confidenceScore) {
        this.confidenceScore = confidenceScore;
    }
    
    public String getAnalysisSummary() {
        return analysisSummary;
    }
    
    public void setAnalysisSummary(String analysisSummary) {
        this.analysisSummary = analysisSummary;
    }
    
    public List<String> getKeyFindings() {
        return keyFindings;
    }
    
    public void setKeyFindings(List<String> keyFindings) {
        this.keyFindings = keyFindings;
    }
    
    public List<String> getRecommendations() {
        return recommendations;
    }
    
    public void setRecommendations(List<String> recommendations) {
        this.recommendations = recommendations;
    }
    
    public String getErrorMessage() {
        return errorMessage;
    }
    
    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
    
    public Long getAnalysisDurationMs() {
        return analysisDurationMs;
    }
    
    public void setAnalysisDurationMs(Long analysisDurationMs) {
        this.analysisDurationMs = analysisDurationMs;
    }
    
    public LocalDateTime getAnalysisDate() {
        return analysisDate;
    }
    
    public void setAnalysisDate(LocalDateTime analysisDate) {
        this.analysisDate = analysisDate;
    }
    
    public LocalDateTime getCreatedDate() {
        return createdDate;
    }
    
    public void setCreatedDate(LocalDateTime createdDate) {
        this.createdDate = createdDate;
    }
} 