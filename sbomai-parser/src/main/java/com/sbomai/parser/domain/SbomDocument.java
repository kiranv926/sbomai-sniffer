package com.sbomai.parser.domain;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

/**
 * Domain model representing a parsed SBOM document.
 * This is the unified internal format for SBOM data across all supported formats.
 */
public class SbomDocument {
    
    private UUID id;
    private String name;
    private String version;
    private SbomFormat format;
    private String description;
    private String supplier;
    private String author;
    private LocalDateTime creationDate;
    private LocalDateTime lastModified;
    private String license;
    private String namespace;
    private List<SbomComponent> components;
    private List<SbomRelationship> relationships;
    private String originalContent;
    private ParsingMetadata parsingMetadata;
    
    // Constructors
    public SbomDocument() {}
    
    public SbomDocument(String name, String version, SbomFormat format) {
        this.id = UUID.randomUUID();
        this.name = name;
        this.version = version;
        this.format = format;
        this.creationDate = LocalDateTime.now();
        this.lastModified = LocalDateTime.now();
    }
    
    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }
    
    public SbomFormat getFormat() { return format; }
    public void setFormat(SbomFormat format) { this.format = format; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public String getSupplier() { return supplier; }
    public void setSupplier(String supplier) { this.supplier = supplier; }
    
    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }
    
    public LocalDateTime getCreationDate() { return creationDate; }
    public void setCreationDate(LocalDateTime creationDate) { this.creationDate = creationDate; }
    
    public LocalDateTime getLastModified() { return lastModified; }
    public void setLastModified(LocalDateTime lastModified) { this.lastModified = lastModified; }
    
    public String getLicense() { return license; }
    public void setLicense(String license) { this.license = license; }
    
    public String getNamespace() { return namespace; }
    public void setNamespace(String namespace) { this.namespace = namespace; }
    
    public List<SbomComponent> getComponents() { return components; }
    public void setComponents(List<SbomComponent> components) { this.components = components; }
    
    public List<SbomRelationship> getRelationships() { return relationships; }
    public void setRelationships(List<SbomRelationship> relationships) { this.relationships = relationships; }
    
    public String getOriginalContent() { return originalContent; }
    public void setOriginalContent(String originalContent) { this.originalContent = originalContent; }
    
    public ParsingMetadata getParsingMetadata() { return parsingMetadata; }
    public void setParsingMetadata(ParsingMetadata parsingMetadata) { this.parsingMetadata = parsingMetadata; }
    
    @Override
    public String toString() {
        return String.format("SbomDocument{id=%s, name='%s', version='%s', format=%s, components=%d}",
                id, name, version, format, components != null ? components.size() : 0);
    }
} 