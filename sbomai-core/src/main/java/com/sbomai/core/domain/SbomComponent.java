package com.sbomai.core.domain;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "sbom_components")
public class SbomComponent {
    
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    
    @Column(name = "sbom_id", nullable = false)
    private UUID sbomId;
    
    @Column(name = "bom_ref", nullable = false)
    private String bomRef;
    
    @Column(name = "name", nullable = false)
    private String name;
    
    @Column(name = "version")
    private String version;
    
    @Column(name = "type")
    private String type;
    
    @Column(name = "purl")
    private String purl;
    
    @Column(name = "cpe")
    private String cpe;
    
    @Column(name = "license_id")
    private String licenseId;
    
    @Column(name = "description")
    private String description;
    
    @Column(name = "author")
    private String author;
    
    @Column(name = "supplier")
    private String supplier;
    
    @Column(name = "checksums", columnDefinition = "jsonb")
    private String checksums;
    
    @Column(name = "properties", columnDefinition = "jsonb")
    private String properties;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    // Constructors
    public SbomComponent() {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }
    
    public SbomComponent(UUID sbomId, String bomRef, String name, String version, String type) {
        this();
        this.sbomId = sbomId;
        this.bomRef = bomRef;
        this.name = name;
        this.version = version;
        this.type = type;
    }
    
    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    
    public UUID getSbomId() { return sbomId; }
    public void setSbomId(UUID sbomId) { this.sbomId = sbomId; }
    
    public String getBomRef() { return bomRef; }
    public void setBomRef(String bomRef) { this.bomRef = bomRef; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }
    
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    
    public String getPurl() { return purl; }
    public void setPurl(String purl) { this.purl = purl; }
    
    public String getCpe() { return cpe; }
    public void setCpe(String cpe) { this.cpe = cpe; }
    
    public String getLicenseId() { return licenseId; }
    public void setLicenseId(String licenseId) { this.licenseId = licenseId; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }
    
    public String getSupplier() { return supplier; }
    public void setSupplier(String supplier) { this.supplier = supplier; }
    
    public String getChecksums() { return checksums; }
    public void setChecksums(String checksums) { this.checksums = checksums; }
    
    public String getProperties() { return properties; }
    public void setProperties(String properties) { this.properties = properties; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
