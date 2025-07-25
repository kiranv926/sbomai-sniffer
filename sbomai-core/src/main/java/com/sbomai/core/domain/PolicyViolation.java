package com.sbomai.core.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Domain entity representing a policy violation found in an SBOM document.
 */
@Entity
@Table(name = "policy_violations")
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class PolicyViolation {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "policy_name", nullable = false)
    private String policyName;

    @Column(name = "policy_type")
    @Enumerated(EnumType.STRING)
    private PolicyType policyType;

    @Column(name = "severity")
    @Enumerated(EnumType.STRING)
    private Severity severity;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "component_name")
    private String componentName;

    @Column(name = "component_version")
    private String componentVersion;

    @Column(name = "license_name")
    private String licenseName;

    @Column(name = "cvss_score")
    private Double cvssScore;

    @Column(name = "recommendation", columnDefinition = "TEXT")
    private String recommendation;

    @Column(name = "is_blocking")
    private Boolean isBlocking = false;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "sbom_document_id")
    private SbomDocument sbomDocument;

    @Column(name = "created_date")
    private LocalDateTime createdDate;

    // Constructors
    public PolicyViolation() {
        this.createdDate = LocalDateTime.now();
    }

    public PolicyViolation(String policyName, PolicyType policyType, Severity severity) {
        this.policyName = policyName;
        this.policyType = policyType;
        this.severity = severity;
        this.createdDate = LocalDateTime.now();
    }

    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getPolicyName() { return policyName; }
    public void setPolicyName(String policyName) { this.policyName = policyName; }

    public PolicyType getPolicyType() { return policyType; }
    public void setPolicyType(PolicyType policyType) { this.policyType = policyType; }

    public Severity getSeverity() { return severity; }
    public void setSeverity(Severity severity) { this.severity = severity; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getComponentName() { return componentName; }
    public void setComponentName(String componentName) { this.componentName = componentName; }

    public String getComponentVersion() { return componentVersion; }
    public void setComponentVersion(String componentVersion) { this.componentVersion = componentVersion; }

    public String getLicenseName() { return licenseName; }
    public void setLicenseName(String licenseName) { this.licenseName = licenseName; }

    public Double getCvssScore() { return cvssScore; }
    public void setCvssScore(Double cvssScore) { this.cvssScore = cvssScore; }

    public String getRecommendation() { return recommendation; }
    public void setRecommendation(String recommendation) { this.recommendation = recommendation; }

    public Boolean getIsBlocking() { return isBlocking; }
    public void setIsBlocking(Boolean isBlocking) { this.isBlocking = isBlocking; }

    public SbomDocument getSbomDocument() { return sbomDocument; }
    public void setSbomDocument(SbomDocument sbomDocument) { this.sbomDocument = sbomDocument; }

    public LocalDateTime getCreatedDate() { return createdDate; }
    public void setCreatedDate(LocalDateTime createdDate) { this.createdDate = createdDate; }

    // Business methods
    public boolean isBlockingViolation() {
        return Boolean.TRUE.equals(isBlocking);
    }

    public boolean isHighSeverity() {
        return Severity.HIGH.equals(severity) || Severity.CRITICAL.equals(severity);
    }

    @Override
    public String toString() {
        return "PolicyViolation{" +
                "id=" + id +
                ", policyName='" + policyName + '\'' +
                ", policyType=" + policyType +
                ", severity=" + severity +
                ", isBlocking=" + isBlocking +
                '}';
    }
} 