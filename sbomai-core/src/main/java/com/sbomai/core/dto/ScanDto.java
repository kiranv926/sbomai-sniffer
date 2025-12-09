package com.sbomai.core.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDateTime;
import java.util.UUID;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class ScanDto {
    
    private UUID id;
    
    @NotBlank(message = "Project name is required")
    private String projectName;
    
    private UUID projectId;
    
    @NotBlank(message = "Source path is required")
    private String sourcePath;
    
    @NotBlank(message = "Source type is required")
    private String sourceType; // FILE, DIRECTORY, REPOSITORY, URL
    
    @NotNull(message = "Status is required")
    private String status; // PENDING, PARSING, ANALYSIS_PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
    
    private String scanType; // SBOM, VULNERABILITY, POLICY, COMPREHENSIVE
    
    private String errorMessage;
    
    private UUID sbomDocumentId;
    
    private Double riskScore;
    
    private Integer vulnerabilitiesFound;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime createdAt;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime updatedAt;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime startedAt;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime completedAt;
    
    private Long scanDurationMs;
    
    private String scannerVersion;
    
    private String scanConfiguration;
    
    private String scanResults;
    
    // Additional fields for UI
    private String projectDescription;
    
    private String scanTypeDisplay;
    
    private String statusDisplay;
    
    private String durationDisplay;
    
    // Constructors
    public ScanDto() {}
    
    public ScanDto(UUID id, String projectName, String sourcePath, String sourceType, String status) {
        this.id = id;
        this.projectName = projectName;
        this.sourcePath = sourcePath;
        this.sourceType = sourceType;
        this.status = status;
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
    
    public UUID getProjectId() {
        return projectId;
    }
    
    public void setProjectId(UUID projectId) {
        this.projectId = projectId;
    }
    
    public String getSourcePath() {
        return sourcePath;
    }
    
    public void setSourcePath(String sourcePath) {
        this.sourcePath = sourcePath;
    }
    
    public String getSourceType() {
        return sourceType;
    }
    
    public void setSourceType(String sourceType) {
        this.sourceType = sourceType;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public String getScanType() {
        return scanType;
    }
    
    public void setScanType(String scanType) {
        this.scanType = scanType;
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
    
    public Double getRiskScore() {
        return riskScore;
    }
    
    public void setRiskScore(Double riskScore) {
        this.riskScore = riskScore;
    }
    
    public Integer getVulnerabilitiesFound() {
        return vulnerabilitiesFound;
    }
    
    public void setVulnerabilitiesFound(Integer vulnerabilitiesFound) {
        this.vulnerabilitiesFound = vulnerabilitiesFound;
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
    
    public LocalDateTime getStartedAt() {
        return startedAt;
    }
    
    public void setStartedAt(LocalDateTime startedAt) {
        this.startedAt = startedAt;
    }
    
    public LocalDateTime getCompletedAt() {
        return completedAt;
    }
    
    public void setCompletedAt(LocalDateTime completedAt) {
        this.completedAt = completedAt;
    }
    
    public Long getScanDurationMs() {
        return scanDurationMs;
    }
    
    public void setScanDurationMs(Long scanDurationMs) {
        this.scanDurationMs = scanDurationMs;
    }
    
    public String getScannerVersion() {
        return scannerVersion;
    }
    
    public void setScannerVersion(String scannerVersion) {
        this.scannerVersion = scannerVersion;
    }
    
    public String getScanConfiguration() {
        return scanConfiguration;
    }
    
    public void setScanConfiguration(String scanConfiguration) {
        this.scanConfiguration = scanConfiguration;
    }
    
    public String getScanResults() {
        return scanResults;
    }
    
    public void setScanResults(String scanResults) {
        this.scanResults = scanResults;
    }
    
    public String getProjectDescription() {
        return projectDescription;
    }
    
    public void setProjectDescription(String projectDescription) {
        this.projectDescription = projectDescription;
    }
    
    public String getScanTypeDisplay() {
        return scanTypeDisplay;
    }
    
    public void setScanTypeDisplay(String scanTypeDisplay) {
        this.scanTypeDisplay = scanTypeDisplay;
    }
    
    public String getStatusDisplay() {
        return statusDisplay;
    }
    
    public void setStatusDisplay(String statusDisplay) {
        this.statusDisplay = statusDisplay;
    }
    
    public String getDurationDisplay() {
        return durationDisplay;
    }
    
    public void setDurationDisplay(String durationDisplay) {
        this.durationDisplay = durationDisplay;
    }
} 