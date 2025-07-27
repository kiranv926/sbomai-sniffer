package com.sbomai.webscan.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Domain entity representing exposed metadata found during web scanning.
 */
@Entity
@Table(name = "exposed_metadata")
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class ExposedMetadata {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "metadata_type", nullable = false)
    private String metadataType;

    @Column(name = "metadata_key")
    private String metadataKey;

    @Column(name = "metadata_value", columnDefinition = "TEXT")
    private String metadataValue;

    @Column(name = "source_location")
    private String sourceLocation;

    @Column(name = "detection_method")
    private String detectionMethod;

    @Enumerated(EnumType.STRING)
    @Column(name = "severity")
    private Severity severity;

    @Enumerated(EnumType.STRING)
    @Column(name = "sensitivity_level")
    private SensitivityLevel sensitivityLevel;

    @Column(name = "is_sensitive")
    private Boolean isSensitive;

    @Column(name = "risk_description")
    private String riskDescription;

    @Column(name = "recommendation")
    private String recommendation;

    @Column(name = "line_number")
    private Integer lineNumber;

    @Column(name = "file_path")
    private String filePath;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "web_scan_result_id")
    private WebScanResult webScanResult;

    @Column(name = "created_date")
    private LocalDateTime createdDate;

    // Constructors
    public ExposedMetadata() {
        this.createdDate = LocalDateTime.now();
    }

    public ExposedMetadata(String metadataType, String metadataKey, String metadataValue) {
        this();
        this.metadataType = metadataType;
        this.metadataKey = metadataKey;
        this.metadataValue = metadataValue;
    }

    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getMetadataType() { return metadataType; }
    public void setMetadataType(String metadataType) { this.metadataType = metadataType; }

    public String getMetadataKey() { return metadataKey; }
    public void setMetadataKey(String metadataKey) { this.metadataKey = metadataKey; }

    public String getMetadataValue() { return metadataValue; }
    public void setMetadataValue(String metadataValue) { this.metadataValue = metadataValue; }

    public String getSourceLocation() { return sourceLocation; }
    public void setSourceLocation(String sourceLocation) { this.sourceLocation = sourceLocation; }

    public String getDetectionMethod() { return detectionMethod; }
    public void setDetectionMethod(String detectionMethod) { this.detectionMethod = detectionMethod; }

    public Severity getSeverity() { return severity; }
    public void setSeverity(Severity severity) { this.severity = severity; }

    public SensitivityLevel getSensitivityLevel() { return sensitivityLevel; }
    public void setSensitivityLevel(SensitivityLevel sensitivityLevel) { this.sensitivityLevel = sensitivityLevel; }

    public Boolean getIsSensitive() { return isSensitive; }
    public void setIsSensitive(Boolean isSensitive) { this.isSensitive = isSensitive; }

    public String getRiskDescription() { return riskDescription; }
    public void setRiskDescription(String riskDescription) { this.riskDescription = riskDescription; }

    public String getRecommendation() { return recommendation; }
    public void setRecommendation(String recommendation) { this.recommendation = recommendation; }

    public Integer getLineNumber() { return lineNumber; }
    public void setLineNumber(Integer lineNumber) { this.lineNumber = lineNumber; }

    public String getFilePath() { return filePath; }
    public void setFilePath(String filePath) { this.filePath = filePath; }

    public WebScanResult getWebScanResult() { return webScanResult; }
    public void setWebScanResult(WebScanResult webScanResult) { this.webScanResult = webScanResult; }

    public LocalDateTime getCreatedDate() { return createdDate; }
    public void setCreatedDate(LocalDateTime createdDate) { this.createdDate = createdDate; }

    // Business methods
    public boolean isHighSensitivity() {
        return SensitivityLevel.HIGH.equals(sensitivityLevel) || SensitivityLevel.CRITICAL.equals(sensitivityLevel);
    }

    public boolean isCriticalSeverity() {
        return Severity.CRITICAL.equals(severity);
    }

    public String getDisplayValue() {
        if (metadataValue != null && metadataValue.length() > 100) {
            return metadataValue.substring(0, 100) + "...";
        }
        return metadataValue;
    }

    public String getLocationInfo() {
        if (filePath != null && lineNumber != null) {
            return filePath + ":" + lineNumber;
        } else if (filePath != null) {
            return filePath;
        } else if (sourceLocation != null) {
            return sourceLocation;
        }
        return "Unknown";
    }

    @Override
    public String toString() {
        return "ExposedMetadata{" +
                "metadataType='" + metadataType + '\'' +
                ", metadataKey='" + metadataKey + '\'' +
                ", severity=" + severity +
                ", sensitivityLevel=" + sensitivityLevel +
                ", isSensitive=" + isSensitive +
                '}';
    }
} 