package com.sbomai.common.domain;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Objects;

/**
 * Represents a component within a Software Bill of Materials (SBOM)
 */
@Entity
@Table(name = "sbom_components")
public class SbomComponent {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotBlank
    @Column(name = "name", nullable = false)
    private String name;
    
    @NotBlank
    @Column(name = "version", nullable = false)
    private String version;
    
    @Column(name = "group_id")
    private String groupId;
    
    @Column(name = "description", columnDefinition = "TEXT")
    private String description;
    
    @Column(name = "license")
    private String license;
    
    @Column(name = "purl")
    private String purl;
    
    @Column(name = "cpe")
    private String cpe;
    
    @Column(name = "sha256")
    private String sha256;
    
    @Column(name = "md5")
    private String md5;
    
    @Column(name = "file_path")
    private String filePath;
    
    @Column(name = "file_size")
    private Long fileSize;
    
    @Column(name = "supplier")
    private String supplier;
    
    @Column(name = "author")
    private String author;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @Column(name = "created_date")
    private LocalDateTime createdDate;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @Column(name = "last_modified_date")
    private LocalDateTime lastModifiedDate;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "sbom_document_id")
    private SbomDocument sbomDocument;
    
    @OneToMany(mappedBy = "component", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Vulnerability> vulnerabilities;
    
    @OneToMany(mappedBy = "component", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<PolicyViolation> policyViolations;
    
    // Constructors
    public SbomComponent() {
        this.createdDate = LocalDateTime.now();
        this.lastModifiedDate = LocalDateTime.now();
    }
    
    public SbomComponent(String name, String version) {
        this();
        this.name = name;
        this.version = version;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getVersion() {
        return version;
    }
    
    public void setVersion(String version) {
        this.version = version;
    }
    
    public String getGroupId() {
        return groupId;
    }
    
    public void setGroupId(String groupId) {
        this.groupId = groupId;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public String getLicense() {
        return license;
    }
    
    public void setLicense(String license) {
        this.license = license;
    }
    
    public String getPurl() {
        return purl;
    }
    
    public void setPurl(String purl) {
        this.purl = purl;
    }
    
    public String getCpe() {
        return cpe;
    }
    
    public void setCpe(String cpe) {
        this.cpe = cpe;
    }
    
    public String getSha256() {
        return sha256;
    }
    
    public void setSha256(String sha256) {
        this.sha256 = sha256;
    }
    
    public String getMd5() {
        return md5;
    }
    
    public void setMd5(String md5) {
        this.md5 = md5;
    }
    
    public String getFilePath() {
        return filePath;
    }
    
    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }
    
    public Long getFileSize() {
        return fileSize;
    }
    
    public void setFileSize(Long fileSize) {
        this.fileSize = fileSize;
    }
    
    public String getSupplier() {
        return supplier;
    }
    
    public void setSupplier(String supplier) {
        this.supplier = supplier;
    }
    
    public String getAuthor() {
        return author;
    }
    
    public void setAuthor(String author) {
        this.author = author;
    }
    
    public LocalDateTime getCreatedDate() {
        return createdDate;
    }
    
    public void setCreatedDate(LocalDateTime createdDate) {
        this.createdDate = createdDate;
    }
    
    public LocalDateTime getLastModifiedDate() {
        return lastModifiedDate;
    }
    
    public void setLastModifiedDate(LocalDateTime lastModifiedDate) {
        this.lastModifiedDate = lastModifiedDate;
    }
    
    public SbomDocument getSbomDocument() {
        return sbomDocument;
    }
    
    public void setSbomDocument(SbomDocument sbomDocument) {
        this.sbomDocument = sbomDocument;
    }
    
    public List<Vulnerability> getVulnerabilities() {
        return vulnerabilities;
    }
    
    public void setVulnerabilities(List<Vulnerability> vulnerabilities) {
        this.vulnerabilities = vulnerabilities;
    }
    
    public List<PolicyViolation> getPolicyViolations() {
        return policyViolations;
    }
    
    public void setPolicyViolations(List<PolicyViolation> policyViolations) {
        this.policyViolations = policyViolations;
    }
    
    // Utility methods
    public void updateLastModified() {
        this.lastModifiedDate = LocalDateTime.now();
    }
    
    public String getFullName() {
        if (groupId != null && !groupId.isEmpty()) {
            return groupId + ":" + name;
        }
        return name;
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        SbomComponent that = (SbomComponent) o;
        return Objects.equals(id, that.id) &&
               Objects.equals(name, that.name) &&
               Objects.equals(version, that.version) &&
               Objects.equals(groupId, that.groupId);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id, name, version, groupId);
    }
    
    @Override
    public String toString() {
        return "SbomComponent{" +
               "id=" + id +
               ", name='" + name + '\'' +
               ", version='" + version + '\'' +
               ", groupId='" + groupId + '\'' +
               ", purl='" + purl + '\'' +
               '}';
    }
} 