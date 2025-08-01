package com.sbomai.common.domain;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Objects;

/**
 * Represents a Software Bill of Materials (SBOM) document
 */
@Entity
@Table(name = "sbom_documents")
public class SbomDocument {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
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
    
    @Column(name = "description", columnDefinition = "TEXT")
    private String description;
    
    @Column(name = "author")
    private String author;
    
    @Column(name = "supplier")
    private String supplier;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @Column(name = "created_date")
    private LocalDateTime createdDate;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @Column(name = "last_modified_date")
    private LocalDateTime lastModifiedDate;
    
    @OneToMany(mappedBy = "sbomDocument", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<SbomComponent> components;
    
    @Column(name = "file_path")
    private String filePath;
    
    @Column(name = "file_size")
    private Long fileSize;
    
    @Column(name = "checksum")
    private String checksum;
    
    @Column(name = "checksum_algorithm")
    private String checksumAlgorithm;
    
    // Constructors
    public SbomDocument() {
        this.createdDate = LocalDateTime.now();
        this.lastModifiedDate = LocalDateTime.now();
    }
    
    public SbomDocument(String documentName, String documentVersion, SbomFormat sbomFormat) {
        this();
        this.documentName = documentName;
        this.documentVersion = documentVersion;
        this.sbomFormat = sbomFormat;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getDocumentName() {
        return documentName;
    }
    
    public void setDocumentName(String documentName) {
        this.documentName = documentName;
    }
    
    public String getDocumentVersion() {
        return documentVersion;
    }
    
    public void setDocumentVersion(String documentVersion) {
        this.documentVersion = documentVersion;
    }
    
    public SbomFormat getSbomFormat() {
        return sbomFormat;
    }
    
    public void setSbomFormat(SbomFormat sbomFormat) {
        this.sbomFormat = sbomFormat;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public String getAuthor() {
        return author;
    }
    
    public void setAuthor(String author) {
        this.author = author;
    }
    
    public String getSupplier() {
        return supplier;
    }
    
    public void setSupplier(String supplier) {
        this.supplier = supplier;
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
    
    public List<SbomComponent> getComponents() {
        return components;
    }
    
    public void setComponents(List<SbomComponent> components) {
        this.components = components;
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
    
    public String getChecksum() {
        return checksum;
    }
    
    public void setChecksum(String checksum) {
        this.checksum = checksum;
    }
    
    public String getChecksumAlgorithm() {
        return checksumAlgorithm;
    }
    
    public void setChecksumAlgorithm(String checksumAlgorithm) {
        this.checksumAlgorithm = checksumAlgorithm;
    }
    
    // Utility methods
    public void updateLastModified() {
        this.lastModifiedDate = LocalDateTime.now();
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        SbomDocument that = (SbomDocument) o;
        return Objects.equals(id, that.id) &&
               Objects.equals(documentName, that.documentName) &&
               Objects.equals(documentVersion, that.documentVersion) &&
               sbomFormat == that.sbomFormat;
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id, documentName, documentVersion, sbomFormat);
    }
    
    @Override
    public String toString() {
        return "SbomDocument{" +
               "id=" + id +
               ", documentName='" + documentName + '\'' +
               ", documentVersion='" + documentVersion + '\'' +
               ", sbomFormat=" + sbomFormat +
               ", createdDate=" + createdDate +
               '}';
    }
} 