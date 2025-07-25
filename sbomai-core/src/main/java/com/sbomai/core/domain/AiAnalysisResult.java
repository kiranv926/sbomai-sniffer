package com.sbomai.core.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Domain entity representing AI analysis results for an SBOM document.
 */
@Entity
@Table(name = "ai_analysis_results")
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class AiAnalysisResult {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "risk_score")
    private Double riskScore;

    @Column(name = "risk_level")
    @Enumerated(EnumType.STRING)
    private RiskLevel riskLevel;

    @Column(name = "analysis_summary", columnDefinition = "TEXT")
    private String analysisSummary;

    @Column(name = "key_findings", columnDefinition = "TEXT")
    private String keyFindings;

    @Column(name = "recommendations", columnDefinition = "TEXT")
    private String recommendations;

    @Column(name = "model_used")
    private String modelUsed;

    @Column(name = "model_version")
    private String modelVersion;

    @Column(name = "analysis_duration_ms")
    private Long analysisDurationMs;

    @Column(name = "confidence_score")
    private Double confidenceScore;

    @Column(name = "analysis_date")
    private LocalDateTime analysisDate;

    @Column(name = "status")
    @Enumerated(EnumType.STRING)
    private AnalysisStatus status;

    @Column(name = "error_message")
    private String errorMessage;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "sbom_document_id")
    private SbomDocument sbomDocument;

    @Column(name = "created_date")
    private LocalDateTime createdDate;

    // Constructors
    public AiAnalysisResult() {
        this.createdDate = LocalDateTime.now();
        this.analysisDate = LocalDateTime.now();
        this.status = AnalysisStatus.PENDING;
    }

    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public Double getRiskScore() { return riskScore; }
    public void setRiskScore(Double riskScore) { this.riskScore = riskScore; }

    public RiskLevel getRiskLevel() { return riskLevel; }
    public void setRiskLevel(RiskLevel riskLevel) { this.riskLevel = riskLevel; }

    public String getAnalysisSummary() { return analysisSummary; }
    public void setAnalysisSummary(String analysisSummary) { this.analysisSummary = analysisSummary; }

    public String getKeyFindings() { return keyFindings; }
    public void setKeyFindings(String keyFindings) { this.keyFindings = keyFindings; }

    public String getRecommendations() { return recommendations; }
    public void setRecommendations(String recommendations) { this.recommendations = recommendations; }

    public String getModelUsed() { return modelUsed; }
    public void setModelUsed(String modelUsed) { this.modelUsed = modelUsed; }

    public String getModelVersion() { return modelVersion; }
    public void setModelVersion(String modelVersion) { this.modelVersion = modelVersion; }

    public Long getAnalysisDurationMs() { return analysisDurationMs; }
    public void setAnalysisDurationMs(Long analysisDurationMs) { this.analysisDurationMs = analysisDurationMs; }

    public Double getConfidenceScore() { return confidenceScore; }
    public void setConfidenceScore(Double confidenceScore) { this.confidenceScore = confidenceScore; }

    public LocalDateTime getAnalysisDate() { return analysisDate; }
    public void setAnalysisDate(LocalDateTime analysisDate) { this.analysisDate = analysisDate; }

    public AnalysisStatus getStatus() { return status; }
    public void setStatus(AnalysisStatus status) { this.status = status; }

    public String getErrorMessage() { return errorMessage; }
    public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }

    public SbomDocument getSbomDocument() { return sbomDocument; }
    public void setSbomDocument(SbomDocument sbomDocument) { this.sbomDocument = sbomDocument; }

    public LocalDateTime getCreatedDate() { return createdDate; }
    public void setCreatedDate(LocalDateTime createdDate) { this.createdDate = createdDate; }

    // Business methods
    public boolean isHighRisk() {
        return RiskLevel.HIGH.equals(riskLevel) || RiskLevel.CRITICAL.equals(riskLevel);
    }

    public boolean isConfident() {
        return confidenceScore != null && confidenceScore >= 0.8;
    }

    @Override
    public String toString() {
        return "AiAnalysisResult{" +
                "id=" + id +
                ", riskScore=" + riskScore +
                ", riskLevel=" + riskLevel +
                ", status=" + status +
                ", analysisDate=" + analysisDate +
                '}';
    }
} 