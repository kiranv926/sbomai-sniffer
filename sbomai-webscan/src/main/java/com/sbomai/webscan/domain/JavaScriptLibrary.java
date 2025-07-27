package com.sbomai.webscan.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Domain entity representing a detected JavaScript library with version information.
 */
@Entity
@Table(name = "javascript_libraries")
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class JavaScriptLibrary {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "library_name", nullable = false)
    private String libraryName;

    @Column(name = "version")
    private String version;

    @Column(name = "detected_version")
    private String detectedVersion;

    @Column(name = "latest_version")
    private String latestVersion;

    @Column(name = "source_url")
    private String sourceUrl;

    @Column(name = "detection_method")
    private String detectionMethod;

    @Enumerated(EnumType.STRING)
    @Column(name = "security_status")
    private SecurityStatus securityStatus;

    @Column(name = "is_outdated")
    private Boolean isOutdated;

    @Column(name = "outdated_reason")
    private String outdatedReason;

    @Column(name = "known_vulnerabilities")
    private Integer knownVulnerabilities;

    @Column(name = "cve_count")
    private Integer cveCount;

    @Column(name = "recommendation")
    private String recommendation;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "web_scan_result_id")
    private WebScanResult webScanResult;

    @Column(name = "created_date")
    private LocalDateTime createdDate;

    // Constructors
    public JavaScriptLibrary() {
        this.createdDate = LocalDateTime.now();
    }

    public JavaScriptLibrary(String libraryName, String version) {
        this();
        this.libraryName = libraryName;
        this.version = version;
        this.detectedVersion = version;
    }

    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getLibraryName() { return libraryName; }
    public void setLibraryName(String libraryName) { this.libraryName = libraryName; }

    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }

    public String getDetectedVersion() { return detectedVersion; }
    public void setDetectedVersion(String detectedVersion) { this.detectedVersion = detectedVersion; }

    public String getLatestVersion() { return latestVersion; }
    public void setLatestVersion(String latestVersion) { this.latestVersion = latestVersion; }

    public String getSourceUrl() { return sourceUrl; }
    public void setSourceUrl(String sourceUrl) { this.sourceUrl = sourceUrl; }

    public String getDetectionMethod() { return detectionMethod; }
    public void setDetectionMethod(String detectionMethod) { this.detectionMethod = detectionMethod; }

    public SecurityStatus getSecurityStatus() { return securityStatus; }
    public void setSecurityStatus(SecurityStatus securityStatus) { this.securityStatus = securityStatus; }

    public Boolean getIsOutdated() { return isOutdated; }
    public void setIsOutdated(Boolean isOutdated) { this.isOutdated = isOutdated; }

    public String getOutdatedReason() { return outdatedReason; }
    public void setOutdatedReason(String outdatedReason) { this.outdatedReason = outdatedReason; }

    public Integer getKnownVulnerabilities() { return knownVulnerabilities; }
    public void setKnownVulnerabilities(Integer knownVulnerabilities) { this.knownVulnerabilities = knownVulnerabilities; }

    public Integer getCveCount() { return cveCount; }
    public void setCveCount(Integer cveCount) { this.cveCount = cveCount; }

    public String getRecommendation() { return recommendation; }
    public void setRecommendation(String recommendation) { this.recommendation = recommendation; }

    public WebScanResult getWebScanResult() { return webScanResult; }
    public void setWebScanResult(WebScanResult webScanResult) { this.webScanResult = webScanResult; }

    public LocalDateTime getCreatedDate() { return createdDate; }
    public void setCreatedDate(LocalDateTime createdDate) { this.createdDate = createdDate; }

    // Business methods
    public boolean isVulnerable() {
        return knownVulnerabilities != null && knownVulnerabilities > 0;
    }

    public boolean needsUpdate() {
        return isOutdated != null && isOutdated;
    }

    public String getVersionInfo() {
        if (latestVersion != null && !latestVersion.equals(version)) {
            return version + " (latest: " + latestVersion + ")";
        }
        return version;
    }

    @Override
    public String toString() {
        return "JavaScriptLibrary{" +
                "libraryName='" + libraryName + '\'' +
                ", version='" + version + '\'' +
                ", isOutdated=" + isOutdated +
                ", securityStatus=" + securityStatus +
                ", knownVulnerabilities=" + knownVulnerabilities +
                '}';
    }
} 