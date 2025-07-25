package com.sbomai.parser.domain;

import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Domain model representing a component within an SBOM.
 */
public class SbomComponent {
    
    private UUID id;
    private String name;
    private String version;
    private String purl; // Package URL
    private String cpe; // Common Platform Enumeration
    private String license;
    private String description;
    private String supplier;
    private String author;
    private String homepage;
    private String downloadUrl;
    private String checksum;
    private String checksumAlgorithm;
    private List<String> tags;
    private Map<String, Object> properties;
    private List<SbomComponent> dependencies;
    
    // Constructors
    public SbomComponent() {}
    
    public SbomComponent(String name, String version) {
        this.id = UUID.randomUUID();
        this.name = name;
        this.version = version;
    }
    
    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }
    
    public String getPurl() { return purl; }
    public void setPurl(String purl) { this.purl = purl; }
    
    public String getCpe() { return cpe; }
    public void setCpe(String cpe) { this.cpe = cpe; }
    
    public String getLicense() { return license; }
    public void setLicense(String license) { this.license = license; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public String getSupplier() { return supplier; }
    public void setSupplier(String supplier) { this.supplier = supplier; }
    
    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }
    
    public String getHomepage() { return homepage; }
    public void setHomepage(String homepage) { this.homepage = homepage; }
    
    public String getDownloadUrl() { return downloadUrl; }
    public void setDownloadUrl(String downloadUrl) { this.downloadUrl = downloadUrl; }
    
    public String getChecksum() { return checksum; }
    public void setChecksum(String checksum) { this.checksum = checksum; }
    
    public String getChecksumAlgorithm() { return checksumAlgorithm; }
    public void setChecksumAlgorithm(String checksumAlgorithm) { this.checksumAlgorithm = checksumAlgorithm; }
    
    public List<String> getTags() { return tags; }
    public void setTags(List<String> tags) { this.tags = tags; }
    
    public Map<String, Object> getProperties() { return properties; }
    public void setProperties(Map<String, Object> properties) { this.properties = properties; }
    
    public List<SbomComponent> getDependencies() { return dependencies; }
    public void setDependencies(List<SbomComponent> dependencies) { this.dependencies = dependencies; }
    
    @Override
    public String toString() {
        return String.format("SbomComponent{id=%s, name='%s', version='%s', purl='%s'}",
                id, name, version, purl);
    }
} 