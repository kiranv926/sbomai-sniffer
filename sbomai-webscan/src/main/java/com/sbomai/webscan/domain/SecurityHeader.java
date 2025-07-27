package com.sbomai.webscan.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Domain entity representing a security header analysis result.
 */
@Entity
@Table(name = "security_headers")
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class SecurityHeader {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "header_name", nullable = false)
    private String headerName;

    @Column(name = "header_value")
    private String headerValue;

    @Column(name = "is_present")
    private Boolean isPresent;

    @Enumerated(EnumType.STRING)
    @Column(name = "security_status")
    private SecurityStatus securityStatus;

    @Enumerated(EnumType.STRING)
    @Column(name = "severity")
    private Severity severity;

    @Column(name = "recommendation")
    private String recommendation;

    @Column(name = "description")
    private String description;

    @Column(name = "best_practice_value")
    private String bestPracticeValue;

    @Column(name = "is_critical")
    private Boolean isCritical;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "web_scan_result_id")
    private WebScanResult webScanResult;

    @Column(name = "created_date")
    private LocalDateTime createdDate;

    // Constructors
    public SecurityHeader() {
        this.createdDate = LocalDateTime.now();
    }

    public SecurityHeader(String headerName) {
        this();
        this.headerName = headerName;
        this.isPresent = false;
    }

    public SecurityHeader(String headerName, String headerValue) {
        this();
        this.headerName = headerName;
        this.headerValue = headerValue;
        this.isPresent = true;
    }

    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getHeaderName() { return headerName; }
    public void setHeaderName(String headerName) { this.headerName = headerName; }

    public String getHeaderValue() { return headerValue; }
    public void setHeaderValue(String headerValue) { this.headerValue = headerValue; }

    public Boolean getIsPresent() { return isPresent; }
    public void setIsPresent(Boolean isPresent) { this.isPresent = isPresent; }

    public SecurityStatus getSecurityStatus() { return securityStatus; }
    public void setSecurityStatus(SecurityStatus securityStatus) { this.securityStatus = securityStatus; }

    public Severity getSeverity() { return severity; }
    public void setSeverity(Severity severity) { this.severity = severity; }

    public String getRecommendation() { return recommendation; }
    public void setRecommendation(String recommendation) { this.recommendation = recommendation; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getBestPracticeValue() { return bestPracticeValue; }
    public void setBestPracticeValue(String bestPracticeValue) { this.bestPracticeValue = bestPracticeValue; }

    public Boolean getIsCritical() { return isCritical; }
    public void setIsCritical(Boolean isCritical) { this.isCritical = isCritical; }

    public WebScanResult getWebScanResult() { return webScanResult; }
    public void setWebScanResult(WebScanResult webScanResult) { this.webScanResult = webScanResult; }

    public LocalDateTime getCreatedDate() { return createdDate; }
    public void setCreatedDate(LocalDateTime createdDate) { this.createdDate = createdDate; }

    // Business methods
    public boolean isMissing() {
        return isPresent != null && !isPresent;
    }

    public boolean isSecure() {
        return SecurityStatus.SECURE.equals(securityStatus);
    }

    public boolean isInsecure() {
        return SecurityStatus.INSECURE.equals(securityStatus);
    }

    public boolean isMissingOrInsecure() {
        return isMissing() || isInsecure();
    }

    public String getStatusDescription() {
        if (isMissing()) {
            return "Missing";
        } else if (isSecure()) {
            return "Secure";
        } else if (isInsecure()) {
            return "Insecure";
        } else {
            return "Unknown";
        }
    }

    @Override
    public String toString() {
        return "SecurityHeader{" +
                "headerName='" + headerName + '\'' +
                ", isPresent=" + isPresent +
                ", securityStatus=" + securityStatus +
                ", severity=" + severity +
                '}';
    }
} 