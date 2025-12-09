package com.sbomai.core.domain;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "scans")
public class Scan {
    
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    
    @Column(name = "project_name", nullable = false)
    private String projectName;
    
    @Column(name = "source_type", nullable = false)
    private String sourceType; // DOCKER_IMAGE, DIRECTORY, GITHUB_REPO, etc.
    
    @Column(name = "source_path", nullable = false)
    private String sourcePath;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private ScanStatus status;
    
    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @Column(name = "error_message")
    private String errorMessage;
    
    @Column(name = "sbom_document_id")
    private UUID sbomDocumentId;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id")
    private Project project;
    
    @Column(name = "vulnerabilities_found")
    private Integer vulnerabilitiesFound = 0;
    
    @Column(name = "risk_score")
    private Double riskScore = 0.0;
    
    // Constructors
    public Scan() {
        this.createdAt = LocalDateTime.now();
        this.status = ScanStatus.PENDING;
    }
    
    public Scan(String projectName, String sourceType, String sourcePath) {
        this();
        this.projectName = projectName;
        this.sourceType = sourceType;
        this.sourcePath = sourcePath;
    }
    
    // Getters and Setters
    public UUID getId() {
        return id;
    }
    
    public void setId(UUID id) {
        this.id = id;
    }
    
    public String getProjectName() {
        return projectName;
    }
    
    public void setProjectName(String projectName) {
        this.projectName = projectName;
    }
    
    public String getSourceType() {
        return sourceType;
    }
    
    public void setSourceType(String sourceType) {
        this.sourceType = sourceType;
    }
    
    public String getSourcePath() {
        return sourcePath;
    }
    
    public void setSourcePath(String sourcePath) {
        this.sourcePath = sourcePath;
    }
    
    public ScanStatus getStatus() {
        return status;
    }
    
    public void setStatus(ScanStatus status) {
        this.status = status;
        this.updatedAt = LocalDateTime.now();
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
    
    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
    
    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
    
    public String getErrorMessage() {
        return errorMessage;
    }
    
    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
    
    public UUID getSbomDocumentId() {
        return sbomDocumentId;
    }
    
    public void setSbomDocumentId(UUID sbomDocumentId) {
        this.sbomDocumentId = sbomDocumentId;
    }
    
    public Project getProject() {
        return project;
    }
    
    public void setProject(Project project) {
        this.project = project;
    }
    
    public Integer getVulnerabilitiesFound() {
        return vulnerabilitiesFound;
    }
    
    public void setVulnerabilitiesFound(Integer vulnerabilitiesFound) {
        this.vulnerabilitiesFound = vulnerabilitiesFound;
    }
    
    public Double getRiskScore() {
        return riskScore;
    }
    
    public void setRiskScore(Double riskScore) {
        this.riskScore = riskScore;
    }
} 