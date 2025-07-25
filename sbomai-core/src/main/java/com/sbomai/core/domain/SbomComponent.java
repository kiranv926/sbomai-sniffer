package com.sbomai.core.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * Domain entity representing a component within an SBOM document.
 */
@Entity
@Table(name = "sbom_components")
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class SbomComponent {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @NotBlank
    @Column(name = "name", nullable = false)
    private String name;

    @NotBlank
    @Column(name = "version", nullable = false)
    private String version;

    @Column(name = "group_id")
    private String groupId;

    @Column(name = "artifact_id")
    private String artifactId;

    @Column(name = "purl")
    private String purl;

    @Column(name = "cpe")
    private String cpe;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "license")
    private String license;

    @Column(name = "license_url")
    private String licenseUrl;

    @Column(name = "homepage_url")
    private String homepageUrl;

    @Column(name = "download_url")
    private String downloadUrl;

    @Column(name = "checksum")
    private String checksum;

    @Column(name = "checksum_algorithm")
    private String checksumAlgorithm;

    @Column(name = "file_size")
    private Long fileSize;

    @Column(name = "supplier_name")
    private String supplierName;

    @Column(name = "supplier_email")
    private String supplierEmail;

    @Column(name = "supplier_url")
    private String supplierUrl;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "sbom_document_id")
    private SbomDocument sbomDocument;

    @OneToMany(mappedBy = "component", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Vulnerability> vulnerabilities = new ArrayList<>();

    @Column(name = "created_date")
    private LocalDateTime createdDate;

    @Column(name = "last_updated")
    private LocalDateTime lastUpdated;

    // Constructors
    public SbomComponent() {}

    public SbomComponent(String name, String version) {
        this.name = name;
        this.version = version;
        this.createdDate = LocalDateTime.now();
        this.lastUpdated = LocalDateTime.now();
    }

    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }

    public String getGroupId() { return groupId; }
    public void setGroupId(String groupId) { this.groupId = groupId; }

    public String getArtifactId() { return artifactId; }
    public void setArtifactId(String artifactId) { this.artifactId = artifactId; }

    public String getPurl() { return purl; }
    public void setPurl(String purl) { this.purl = purl; }

    public String getCpe() { return cpe; }
    public void setCpe(String cpe) { this.cpe = cpe; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getLicense() { return license; }
    public void setLicense(String license) { this.license = license; }

    public String getLicenseUrl() { return licenseUrl; }
    public void setLicenseUrl(String licenseUrl) { this.licenseUrl = licenseUrl; }

    public String getHomepageUrl() { return homepageUrl; }
    public void setHomepageUrl(String homepageUrl) { this.homepageUrl = homepageUrl; }

    public String getDownloadUrl() { return downloadUrl; }
    public void setDownloadUrl(String downloadUrl) { this.downloadUrl = downloadUrl; }

    public String getChecksum() { return checksum; }
    public void setChecksum(String checksum) { this.checksum = checksum; }

    public String getChecksumAlgorithm() { return checksumAlgorithm; }
    public void setChecksumAlgorithm(String checksumAlgorithm) { this.checksumAlgorithm = checksumAlgorithm; }

    public Long getFileSize() { return fileSize; }
    public void setFileSize(Long fileSize) { this.fileSize = fileSize; }

    public String getSupplierName() { return supplierName; }
    public void setSupplierName(String supplierName) { this.supplierName = supplierName; }

    public String getSupplierEmail() { return supplierEmail; }
    public void setSupplierEmail(String supplierEmail) { this.supplierEmail = supplierEmail; }

    public String getSupplierUrl() { return supplierUrl; }
    public void setSupplierUrl(String supplierUrl) { this.supplierUrl = supplierUrl; }

    public SbomDocument getSbomDocument() { return sbomDocument; }
    public void setSbomDocument(SbomDocument sbomDocument) { this.sbomDocument = sbomDocument; }

    public List<Vulnerability> getVulnerabilities() { return vulnerabilities; }
    public void setVulnerabilities(List<Vulnerability> vulnerabilities) { this.vulnerabilities = vulnerabilities; }

    public LocalDateTime getCreatedDate() { return createdDate; }
    public void setCreatedDate(LocalDateTime createdDate) { this.createdDate = createdDate; }

    public LocalDateTime getLastUpdated() { return lastUpdated; }
    public void setLastUpdated(LocalDateTime lastUpdated) { this.lastUpdated = lastUpdated; }

    // Business methods
    public void addVulnerability(Vulnerability vulnerability) {
        vulnerability.setComponent(this);
        this.vulnerabilities.add(vulnerability);
    }

    public void updateLastModified() {
        this.lastUpdated = LocalDateTime.now();
    }

    @Override
    public String toString() {
        return "SbomComponent{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", version='" + version + '\'' +
                ", purl='" + purl + '\'' +
                '}';
    }
} 