package com.sbomai.webscan.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * Domain entity representing the results of a website security scan.
 */
@Entity
@Table(name = "web_scan_results")
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class WebScanResult {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "target_url", nullable = false)
    private String targetUrl;

    @Column(name = "scan_date")
    private LocalDateTime scanDate;

    @Column(name = "scan_duration_ms")
    private Long scanDurationMs;

    @Enumerated(EnumType.STRING)
    @Column(name = "overall_security_score")
    private SecurityScore overallSecurityScore;

    @Column(name = "total_issues")
    private Integer totalIssues;

    @Column(name = "critical_issues")
    private Integer criticalIssues;

    @Column(name = "high_issues")
    private Integer highIssues;

    @Column(name = "medium_issues")
    private Integer mediumIssues;

    @Column(name = "low_issues")
    private Integer lowIssues;

    @Column(name = "info_issues")
    private Integer infoIssues;

    @OneToMany(mappedBy = "webScanResult", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<JavaScriptLibrary> javascriptLibraries = new ArrayList<>();

    @OneToMany(mappedBy = "webScanResult", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<SecurityHeader> securityHeaders = new ArrayList<>();

    @OneToMany(mappedBy = "webScanResult", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<ExposedMetadata> exposedMetadata = new ArrayList<>();

    @OneToMany(mappedBy = "webScanResult", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<SecurityVulnerability> securityVulnerabilities = new ArrayList<>();

    @Column(name = "status")
    @Enumerated(EnumType.STRING)
    private ScanStatus status;

    @Column(name = "error_message")
    private String errorMessage;

    @Column(name = "created_date")
    private LocalDateTime createdDate;

    // Constructors
    public WebScanResult() {
        this.createdDate = LocalDateTime.now();
        this.scanDate = LocalDateTime.now();
        this.status = ScanStatus.PENDING;
    }

    public WebScanResult(String targetUrl) {
        this();
        this.targetUrl = targetUrl;
    }

    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getTargetUrl() { return targetUrl; }
    public void setTargetUrl(String targetUrl) { this.targetUrl = targetUrl; }

    public LocalDateTime getScanDate() { return scanDate; }
    public void setScanDate(LocalDateTime scanDate) { this.scanDate = scanDate; }

    public Long getScanDurationMs() { return scanDurationMs; }
    public void setScanDurationMs(Long scanDurationMs) { this.scanDurationMs = scanDurationMs; }

    public SecurityScore getOverallSecurityScore() { return overallSecurityScore; }
    public void setOverallSecurityScore(SecurityScore overallSecurityScore) { this.overallSecurityScore = overallSecurityScore; }

    public Integer getTotalIssues() { return totalIssues; }
    public void setTotalIssues(Integer totalIssues) { this.totalIssues = totalIssues; }

    public Integer getCriticalIssues() { return criticalIssues; }
    public void setCriticalIssues(Integer criticalIssues) { this.criticalIssues = criticalIssues; }

    public Integer getHighIssues() { return highIssues; }
    public void setHighIssues(Integer highIssues) { this.highIssues = highIssues; }

    public Integer getMediumIssues() { return mediumIssues; }
    public void setMediumIssues(Integer mediumIssues) { this.mediumIssues = mediumIssues; }

    public Integer getLowIssues() { return lowIssues; }
    public void setLowIssues(Integer lowIssues) { this.lowIssues = lowIssues; }

    public Integer getInfoIssues() { return infoIssues; }
    public void setInfoIssues(Integer infoIssues) { this.infoIssues = infoIssues; }

    public List<JavaScriptLibrary> getJavascriptLibraries() { return javascriptLibraries; }
    public void setJavascriptLibraries(List<JavaScriptLibrary> javascriptLibraries) { this.javascriptLibraries = javascriptLibraries; }

    public List<SecurityHeader> getSecurityHeaders() { return securityHeaders; }
    public void setSecurityHeaders(List<SecurityHeader> securityHeaders) { this.securityHeaders = securityHeaders; }

    public List<ExposedMetadata> getExposedMetadata() { return exposedMetadata; }
    public void setExposedMetadata(List<ExposedMetadata> exposedMetadata) { this.exposedMetadata = exposedMetadata; }

    public List<SecurityVulnerability> getSecurityVulnerabilities() { return securityVulnerabilities; }
    public void setSecurityVulnerabilities(List<SecurityVulnerability> securityVulnerabilities) { this.securityVulnerabilities = securityVulnerabilities; }

    public ScanStatus getStatus() { return status; }
    public void setStatus(ScanStatus status) { this.status = status; }

    public String getErrorMessage() { return errorMessage; }
    public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }

    public LocalDateTime getCreatedDate() { return createdDate; }
    public void setCreatedDate(LocalDateTime createdDate) { this.createdDate = createdDate; }

    // Business methods
    public void addJavaScriptLibrary(JavaScriptLibrary library) {
        library.setWebScanResult(this);
        this.javascriptLibraries.add(library);
    }

    public void addSecurityHeader(SecurityHeader header) {
        header.setWebScanResult(this);
        this.securityHeaders.add(header);
    }

    public void addExposedMetadata(ExposedMetadata metadata) {
        metadata.setWebScanResult(this);
        this.exposedMetadata.add(metadata);
    }

    public void addSecurityVulnerability(SecurityVulnerability vulnerability) {
        vulnerability.setWebScanResult(this);
        this.securityVulnerabilities.add(vulnerability);
    }

    public void calculateSecurityScore() {
        int score = 100;
        
        // Deduct points for issues
        if (criticalIssues != null) score -= (criticalIssues * 20);
        if (highIssues != null) score -= (highIssues * 10);
        if (mediumIssues != null) score -= (mediumIssues * 5);
        if (lowIssues != null) score -= (lowIssues * 2);
        if (infoIssues != null) score -= (infoIssues * 1);
        
        // Ensure score doesn't go below 0
        score = Math.max(0, score);
        
        // Set security score
        if (score >= 90) {
            this.overallSecurityScore = SecurityScore.EXCELLENT;
        } else if (score >= 80) {
            this.overallSecurityScore = SecurityScore.GOOD;
        } else if (score >= 70) {
            this.overallSecurityScore = SecurityScore.FAIR;
        } else if (score >= 60) {
            this.overallSecurityScore = SecurityScore.POOR;
        } else {
            this.overallSecurityScore = SecurityScore.CRITICAL;
        }
    }

    public void calculateTotalIssues() {
        this.totalIssues = (criticalIssues != null ? criticalIssues : 0) +
                          (highIssues != null ? highIssues : 0) +
                          (mediumIssues != null ? mediumIssues : 0) +
                          (lowIssues != null ? lowIssues : 0) +
                          (infoIssues != null ? infoIssues : 0);
    }

    @Override
    public String toString() {
        return "WebScanResult{" +
                "id=" + id +
                ", targetUrl='" + targetUrl + '\'' +
                ", overallSecurityScore=" + overallSecurityScore +
                ", totalIssues=" + totalIssues +
                ", status=" + status +
                ", scanDate=" + scanDate +
                '}';
    }
} 