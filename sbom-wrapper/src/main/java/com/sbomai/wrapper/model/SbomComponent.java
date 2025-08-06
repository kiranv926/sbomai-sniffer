package com.sbomai.wrapper.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.LocalDateTime;
import java.util.*;

/**
 * Represents a normalized SBOM component across all ecosystems.
 * This is the core data model that unifies components from different sources.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public class SbomComponent {
    
    @JsonProperty("id")
    private String id;
    
    @JsonProperty("name")
    private String name;
    
    @JsonProperty("version")
    private String version;
    
    @JsonProperty("description")
    private String description;
    
    @JsonProperty("purl")
    private String purl;
    
    @JsonProperty("cpe")
    private String cpe;
    
    @JsonProperty("licenses")
    private List<License> licenses = new ArrayList<>();
    
    @JsonProperty("checksums")
    private List<Checksum> checksums = new ArrayList<>();
    
    @JsonProperty("externalReferences")
    private List<ExternalReference> externalReferences = new ArrayList<>();
    
    @JsonProperty("properties")
    private Map<String, String> properties = new HashMap<>();
    
    @JsonProperty("supplier")
    private Supplier supplier;
    
    @JsonProperty("author")
    private String author;
    
    @JsonProperty("publisher")
    private String publisher;
    
    @JsonProperty("group")
    private String group;
    
    @JsonProperty("scope")
    private String scope;
    
    @JsonProperty("type")
    private String type;
    
    @JsonProperty("ecosystem")
    private String ecosystem;
    
    @JsonProperty("source")
    private String source;
    
    @JsonProperty("createdAt")
    private LocalDateTime createdAt;
    
    @JsonProperty("updatedAt")
    private LocalDateTime updatedAt;
    
    @JsonProperty("dependencies")
    private List<String> dependencies = new ArrayList<>();
    
    @JsonProperty("vulnerabilities")
    private List<Vulnerability> vulnerabilities = new ArrayList<>();
    
    @JsonProperty("metadata")
    private ComponentMetadata metadata;
    
    // Constructors
    public SbomComponent() {
        this.id = UUID.randomUUID().toString();
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }
    
    public SbomComponent(String name, String version) {
        this();
        this.name = name;
        this.version = version;
    }
    
    // Builder pattern for fluent API
    public static Builder builder() {
        return new Builder();
    }
    
    public static class Builder {
        private SbomComponent component;
        
        public Builder() {
            this.component = new SbomComponent();
        }
        
        public Builder name(String name) {
            component.name = name;
            return this;
        }
        
        public Builder version(String version) {
            component.version = version;
            return this;
        }
        
        public Builder description(String description) {
            component.description = description;
            return this;
        }
        
        public Builder purl(String purl) {
            component.purl = purl;
            return this;
        }
        
        public Builder ecosystem(String ecosystem) {
            component.ecosystem = ecosystem;
            return this;
        }
        
        public Builder source(String source) {
            component.source = source;
            return this;
        }
        
        public Builder type(String type) {
            component.type = type;
            return this;
        }
        
        public Builder license(License license) {
            component.licenses.add(license);
            return this;
        }
        
        public Builder checksum(Checksum checksum) {
            component.checksums.add(checksum);
            return this;
        }
        
        public Builder property(String key, String value) {
            component.properties.put(key, value);
            return this;
        }
        
        public SbomComponent build() {
            return component;
        }
    }
    
    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public String getPurl() { return purl; }
    public void setPurl(String purl) { this.purl = purl; }
    
    public String getCpe() { return cpe; }
    public void setCpe(String cpe) { this.cpe = cpe; }
    
    public List<License> getLicenses() { return licenses; }
    public void setLicenses(List<License> licenses) { this.licenses = licenses; }
    
    public List<Checksum> getChecksums() { return checksums; }
    public void setChecksums(List<Checksum> checksums) { this.checksums = checksums; }
    
    public List<ExternalReference> getExternalReferences() { return externalReferences; }
    public void setExternalReferences(List<ExternalReference> externalReferences) { this.externalReferences = externalReferences; }
    
    public Map<String, String> getProperties() { return properties; }
    public void setProperties(Map<String, String> properties) { this.properties = properties; }
    
    public Supplier getSupplier() { return supplier; }
    public void setSupplier(Supplier supplier) { this.supplier = supplier; }
    
    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }
    
    public String getPublisher() { return publisher; }
    public void setPublisher(String publisher) { this.publisher = publisher; }
    
    public String getGroup() { return group; }
    public void setGroup(String group) { this.group = group; }
    
    public String getScope() { return scope; }
    public void setScope(String scope) { this.scope = scope; }
    
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    
    public String getEcosystem() { return ecosystem; }
    public void setEcosystem(String ecosystem) { this.ecosystem = ecosystem; }
    
    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    
    public List<String> getDependencies() { return dependencies; }
    public void setDependencies(List<String> dependencies) { this.dependencies = dependencies; }
    
    public List<Vulnerability> getVulnerabilities() { return vulnerabilities; }
    public void setVulnerabilities(List<Vulnerability> vulnerabilities) { this.vulnerabilities = vulnerabilities; }
    
    public ComponentMetadata getMetadata() { return metadata; }
    public void setMetadata(ComponentMetadata metadata) { this.metadata = metadata; }
    
    // Utility methods
    public void addLicense(License license) {
        this.licenses.add(license);
    }
    
    public void addChecksum(Checksum checksum) {
        this.checksums.add(checksum);
    }
    
    public void addDependency(String dependencyId) {
        this.dependencies.add(dependencyId);
    }
    
    public void addVulnerability(Vulnerability vulnerability) {
        this.vulnerabilities.add(vulnerability);
    }
    
    public void addProperty(String key, String value) {
        this.properties.put(key, value);
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        SbomComponent that = (SbomComponent) o;
        return Objects.equals(purl, that.purl) || 
               (Objects.equals(name, that.name) && Objects.equals(version, that.version));
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(purl, name, version);
    }
    
    @Override
    public String toString() {
        return String.format("SbomComponent{name='%s', version='%s', ecosystem='%s', source='%s'}", 
                           name, version, ecosystem, source);
    }
} 