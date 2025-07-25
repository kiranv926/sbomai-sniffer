package com.sbomai.core.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * Core domain entity representing a Software Bill of Materials (SBOM) document.
 * 
 * This entity encapsulates all the metadata and components of an SBOM,
 * supporting both SPDX and CycloneDX formats.
 */
@Entity
@Table(name = "sbom_documents")
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class SbomDocument {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @NotBlank
    @Column(name = "document_name", nullable = false)
    private String documentName;

    @NotBlank
    @Column(name = "document_version", nullable = false)
    private String documentVersion;

    @NotNull
    @Enumerated(EnumType.STRING)
    @Column(name = "sbom_format", nullable = false)
    private SbomFormat sbomFormat;

    @Column(name = "document_namespace")
    private String documentNamespace;

    @Column(name = "creator_name")
    private String creatorName;

    @Column(name = "creator_email")
    private String creatorEmail;

    @Column(name = "created_date")
    private LocalDateTime createdDate;

    @Column(name = "file_path")
    private String filePath;

    @Column(name = "file_size")
    private Long fileSize;

    @Column(name = "checksum")
    private String checksum;

    @Column(name = "checksum_algorithm")
    private String checksumAlgorithm;

    @OneToMany(mappedBy = "sbomDocument", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<SbomComponent> components = new ArrayList<>();

    @OneToMany(mappedBy = "sbomDocument", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<VulnerabilityReport> vulnerabilityReports = new ArrayList<>();

    @OneToMany(mappedBy = "sbomDocument", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<PolicyViolation> policyViolations = new ArrayList<>();

    @OneToOne(mappedBy = "sbomDocument", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private AiAnalysisResult aiAnalysisResult;

    @Column(name = "analysis_status")
    @Enumerated(EnumType.STRING)
    private AnalysisStatus analysisStatus = AnalysisStatus.PENDING;

    @Column(name = "last_analyzed")
    private LocalDateTime lastAnalyzed;

    @Column(name = "raw_content", columnDefinition = "TEXT")
    private String rawContent;

    // Constructors
    public SbomDocument() {}

    public SbomDocument(String documentName, String documentVersion, SbomFormat sbomFormat) {
        this.documentName = documentName;
        this.documentVersion = documentVersion;
        this.sbomFormat = sbomFormat;
        this.createdDate = LocalDateTime.now();
    }

    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getDocumentName() { return documentName; }
    public void setDocumentName(String documentName) { this.documentName = documentName; }

    public String getDocumentVersion() { return documentVersion; }
    public void setDocumentVersion(String documentVersion) { this.documentVersion = documentVersion; }

    public SbomFormat getSbomFormat() { return sbomFormat; }
    public void setSbomFormat(SbomFormat sbomFormat) { this.sbomFormat = sbomFormat; }

    public String getDocumentNamespace() { return documentNamespace; }
    public void setDocumentNamespace(String documentNamespace) { this.documentNamespace = documentNamespace; }

    public String getCreatorName() { return creatorName; }
    public void setCreatorName(String creatorName) { this.creatorName = creatorName; }

    public String getCreatorEmail() { return creatorEmail; }
    public void setCreatorEmail(String creatorEmail) { this.creatorEmail = creatorEmail; }

    public LocalDateTime getCreatedDate() { return createdDate; }
    public void setCreatedDate(LocalDateTime createdDate) { this.createdDate = createdDate; }

    public String getFilePath() { return filePath; }
    public void setFilePath(String filePath) { this.filePath = filePath; }

    public Long getFileSize() { return fileSize; }
    public void setFileSize(Long fileSize) { this.fileSize = fileSize; }

    public String getChecksum() { return checksum; }
    public void setChecksum(String checksum) { this.checksum = checksum; }

    public String getChecksumAlgorithm() { return checksumAlgorithm; }
    public void setChecksumAlgorithm(String checksumAlgorithm) { this.checksumAlgorithm = checksumAlgorithm; }

    public List<SbomComponent> getComponents() { return components; }
    public void setComponents(List<SbomComponent> components) { this.components = components; }

    public List<VulnerabilityReport> getVulnerabilityReports() { return vulnerabilityReports; }
    public void setVulnerabilityReports(List<VulnerabilityReport> vulnerabilityReports) { this.vulnerabilityReports = vulnerabilityReports; }

    public List<PolicyViolation> getPolicyViolations() { return policyViolations; }
    public void setPolicyViolations(List<PolicyViolation> policyViolations) { this.policyViolations = policyViolations; }

    public AiAnalysisResult getAiAnalysisResult() { return aiAnalysisResult; }
    public void setAiAnalysisResult(AiAnalysisResult aiAnalysisResult) { this.aiAnalysisResult = aiAnalysisResult; }

    public AnalysisStatus getAnalysisStatus() { return analysisStatus; }
    public void setAnalysisStatus(AnalysisStatus analysisStatus) { this.analysisStatus = analysisStatus; }

    public LocalDateTime getLastAnalyzed() { return lastAnalyzed; }
    public void setLastAnalyzed(LocalDateTime lastAnalyzed) { this.lastAnalyzed = lastAnalyzed; }

    public String getRawContent() { return rawContent; }
    public void setRawContent(String rawContent) { this.rawContent = rawContent; }

    // Business methods
    public void addComponent(SbomComponent component) {
        component.setSbomDocument(this);
        this.components.add(component);
    }

    public void addVulnerabilityReport(VulnerabilityReport report) {
        report.setSbomDocument(this);
        this.vulnerabilityReports.add(report);
    }

    public void addPolicyViolation(PolicyViolation violation) {
        violation.setSbomDocument(this);
        this.policyViolations.add(violation);
    }

    public void markAsAnalyzed() {
        this.analysisStatus = AnalysisStatus.COMPLETED;
        this.lastAnalyzed = LocalDateTime.now();
    }

    public void markAsFailed() {
        this.analysisStatus = AnalysisStatus.FAILED;
        this.lastAnalyzed = LocalDateTime.now();
    }

    @Override
    public String toString() {
        return "SbomDocument{" +
                "id=" + id +
                ", documentName='" + documentName + '\'' +
                ", documentVersion='" + documentVersion + '\'' +
                ", sbomFormat=" + sbomFormat +
                ", analysisStatus=" + analysisStatus +
                '}';
    }
} 