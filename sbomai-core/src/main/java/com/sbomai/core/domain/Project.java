package com.sbomai.core.domain;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDateTime;
import java.util.*;

@Entity
@Table(name = "projects")
public class Project {
    
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    
    @NotBlank
    @Column(name = "name", nullable = false, unique = true)
    private String name;
    
    @Column(name = "description", columnDefinition = "TEXT")
    private String description;
    
    @NotBlank
    @Column(name = "version", nullable = false)
    private String version;
    
    @Column(name = "latest_version")
    private String latestVersion;
    
    @NotBlank
    @Column(name = "classifier", nullable = false)
    private String classifier;
    
    @Column(name = "last_bom_import")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm")
    private LocalDateTime lastBomImport;
    
    @Column(name = "bom_format")
    @Enumerated(EnumType.STRING)
    private SbomFormat bomFormat;
    
    @Column(name = "risk_score")
    private Integer riskScore = 0;
    
    @Column(name = "active")
    private Boolean active = true;
    
    @Column(name = "policy_violations")
    private Integer policyViolations = 0;
    
    @Column(name = "vulnerabilities")
    private Integer vulnerabilities = 0;
    
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "project_tags", joinColumns = @JoinColumn(name = "project_id"))
    @Column(name = "tag")
    private Set<String> tags = new HashSet<>();
    
    @Column(name = "last_modified")
    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDateTime lastModified;
    
    @Column(name = "created_by")
    private String createdBy;
    
    @Column(name = "team")
    private String team;
    
    @Column(name = "language")
    private String language;
    
    @Embedded
    private RepositoryInfo repository;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "status")
    private ProjectStatus status = ProjectStatus.ACTIVE;
    
    @Embedded
    private VulnerabilityCount vulnerabilityCount = new VulnerabilityCount();
    
    @Column(name = "dependency_count")
    private Integer dependencyCount = 0;
    
    @Column(name = "outdated_deps")
    private Integer outdatedDeps = 0;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    // Temporarily commented out to fix JPA mapping issues
    // @OneToMany(mappedBy = "project", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    // @JsonIgnore
    // private List<Scan> scans = new ArrayList<>();
    
    // @OneToMany(mappedBy = "project", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    // @JsonIgnore
    // private List<Vulnerability> projectVulnerabilities = new ArrayList<>();
    
    // Constructors
    public Project() {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
        this.lastModified = LocalDateTime.now();
    }
    
    public Project(String name, String version, String classifier) {
        this();
        this.name = name;
        this.version = version;
        this.classifier = classifier;
    }
    
    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }
    
    public String getLatestVersion() { return latestVersion; }
    public void setLatestVersion(String latestVersion) { this.latestVersion = latestVersion; }
    
    public String getClassifier() { return classifier; }
    public void setClassifier(String classifier) { this.classifier = classifier; }
    
    public LocalDateTime getLastBomImport() { return lastBomImport; }
    public void setLastBomImport(LocalDateTime lastBomImport) { this.lastBomImport = lastBomImport; }
    
    public SbomFormat getBomFormat() { return bomFormat; }
    public void setBomFormat(SbomFormat bomFormat) { this.bomFormat = bomFormat; }
    
    public Integer getRiskScore() { return riskScore; }
    public void setRiskScore(Integer riskScore) { this.riskScore = riskScore; }
    
    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }
    
    public Integer getPolicyViolations() { return policyViolations; }
    public void setPolicyViolations(Integer policyViolations) { this.policyViolations = policyViolations; }
    
    public Integer getVulnerabilities() { return vulnerabilities; }
    public void setVulnerabilities(Integer vulnerabilities) { this.vulnerabilities = vulnerabilities; }
    
    public Set<String> getTags() { return tags; }
    public void setTags(Set<String> tags) { this.tags = tags; }
    
    public LocalDateTime getLastModified() { return lastModified; }
    public void setLastModified(LocalDateTime lastModified) { this.lastModified = lastModified; }
    
    public String getCreatedBy() { return createdBy; }
    public void setCreatedBy(String createdBy) { this.createdBy = createdBy; }
    
    public String getTeam() { return team; }
    public void setTeam(String team) { this.team = team; }
    
    public String getLanguage() { return language; }
    public void setLanguage(String language) { this.language = language; }
    
    public RepositoryInfo getRepository() { return repository; }
    public void setRepository(RepositoryInfo repository) { this.repository = repository; }
    
    public ProjectStatus getStatus() { return status; }
    public void setStatus(ProjectStatus status) { this.status = status; }
    
    public VulnerabilityCount getVulnerabilityCount() { return vulnerabilityCount; }
    public void setVulnerabilityCount(VulnerabilityCount vulnerabilityCount) { this.vulnerabilityCount = vulnerabilityCount; }
    
    public Integer getDependencyCount() { return dependencyCount; }
    public void setDependencyCount(Integer dependencyCount) { this.dependencyCount = dependencyCount; }
    
    public Integer getOutdatedDeps() { return outdatedDeps; }
    public void setOutdatedDeps(Integer outdatedDeps) { this.outdatedDeps = outdatedDeps; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    
    // Temporarily commented out to fix JPA mapping issues
    // public List<Scan> getScans() { return scans; }
    // public void setScans(List<Scan> scans) { this.scans = scans; }
    
    // public List<Vulnerability> getProjectVulnerabilities() { return projectVulnerabilities; }
    // public void setProjectVulnerabilities(List<Vulnerability> projectVulnerabilities) { this.projectVulnerabilities = projectVulnerabilities; }
    
    // Helper methods
    public void addTag(String tag) {
        if (this.tags == null) {
            this.tags = new HashSet<>();
        }
        this.tags.add(tag);
    }
    
    public void removeTag(String tag) {
        if (this.tags != null) {
            this.tags.remove(tag);
        }
    }
    
    @PreUpdate
    public void preUpdate() {
        this.updatedAt = LocalDateTime.now();
        this.lastModified = LocalDateTime.now();
    }
} 