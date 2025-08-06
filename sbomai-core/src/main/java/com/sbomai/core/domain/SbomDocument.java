package com.sbomai.core.domain;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "sbom_documents")
public class SbomDocument {
    
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    
    @Column(name = "scan_id", nullable = false)
    private UUID scanId;
    
    @Column(name = "format", nullable = false)
    private String format;
    
    @Column(name = "spec_version", nullable = false)
    private String specVersion;
    
    @Column(name = "raw_json", columnDefinition = "jsonb")
    private String rawJson;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @Column(name = "ingested_at")
    private LocalDateTime ingestedAt;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    // Constructors
    public SbomDocument() {
        this.ingestedAt = LocalDateTime.now();
        this.createdAt = LocalDateTime.now();
    }
    
    public SbomDocument(UUID scanId, String format, String specVersion, String rawJson) {
        this();
        this.scanId = scanId;
        this.format = format;
        this.specVersion = specVersion;
        this.rawJson = rawJson;
    }
    
    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    
    public UUID getScanId() { return scanId; }
    public void setScanId(UUID scanId) { this.scanId = scanId; }
    
    public String getFormat() { return format; }
    public void setFormat(String format) { this.format = format; }
    
    public String getSpecVersion() { return specVersion; }
    public void setSpecVersion(String specVersion) { this.specVersion = specVersion; }
    
    public String getRawJson() { return rawJson; }
    public void setRawJson(String rawJson) { this.rawJson = rawJson; }
    
    public LocalDateTime getIngestedAt() { return ingestedAt; }
    public void setIngestedAt(LocalDateTime ingestedAt) { this.ingestedAt = ingestedAt; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
