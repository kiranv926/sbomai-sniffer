package com.sbomai.core.dto;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

public class ProjectDto {
    private UUID id;
    private String name;
    private String version;
    private String description;
    private String classifier;
    private String language;
    private String team;
    private String status;
    private String repoUrl;
    private String repoType;
    private String repoBranch;
    private String bomFormat;
    private String latestVersion;
    private String createdBy;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime lastModified;
    private LocalDateTime lastBomImport;
    private Boolean active;
    private Integer riskScore;
    private Integer vulnerabilities;
    private Integer criticalCount;
    private Integer highCount;
    private Integer mediumCount;
    private Integer lowCount;
    private Integer dependencyCount;
    private Integer outdatedDeps;
    private Integer policyViolations;
    private List<String> tags;

    // Constructors
    public ProjectDto() {}

    public ProjectDto(UUID id, String name, String version) {
        this.id = id;
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

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getClassifier() { return classifier; }
    public void setClassifier(String classifier) { this.classifier = classifier; }

    public String getLanguage() { return language; }
    public void setLanguage(String language) { this.language = language; }

    public String getTeam() { return team; }
    public void setTeam(String team) { this.team = team; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getRepoUrl() { return repoUrl; }
    public void setRepoUrl(String repoUrl) { this.repoUrl = repoUrl; }

    public String getRepoType() { return repoType; }
    public void setRepoType(String repoType) { this.repoType = repoType; }

    public String getRepoBranch() { return repoBranch; }
    public void setRepoBranch(String repoBranch) { this.repoBranch = repoBranch; }

    public String getBomFormat() { return bomFormat; }
    public void setBomFormat(String bomFormat) { this.bomFormat = bomFormat; }

    public String getLatestVersion() { return latestVersion; }
    public void setLatestVersion(String latestVersion) { this.latestVersion = latestVersion; }

    public String getCreatedBy() { return createdBy; }
    public void setCreatedBy(String createdBy) { this.createdBy = createdBy; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }

    public LocalDateTime getLastModified() { return lastModified; }
    public void setLastModified(LocalDateTime lastModified) { this.lastModified = lastModified; }

    public LocalDateTime getLastBomImport() { return lastBomImport; }
    public void setLastBomImport(LocalDateTime lastBomImport) { this.lastBomImport = lastBomImport; }

    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }

    public Integer getRiskScore() { return riskScore; }
    public void setRiskScore(Integer riskScore) { this.riskScore = riskScore; }

    public Integer getVulnerabilities() { return vulnerabilities; }
    public void setVulnerabilities(Integer vulnerabilities) { this.vulnerabilities = vulnerabilities; }

    public Integer getCriticalCount() { return criticalCount; }
    public void setCriticalCount(Integer criticalCount) { this.criticalCount = criticalCount; }

    public Integer getHighCount() { return highCount; }
    public void setHighCount(Integer highCount) { this.highCount = highCount; }

    public Integer getMediumCount() { return mediumCount; }
    public void setMediumCount(Integer mediumCount) { this.mediumCount = mediumCount; }

    public Integer getLowCount() { return lowCount; }
    public void setLowCount(Integer lowCount) { this.lowCount = lowCount; }

    public Integer getDependencyCount() { return dependencyCount; }
    public void setDependencyCount(Integer dependencyCount) { this.dependencyCount = dependencyCount; }

    public Integer getOutdatedDeps() { return outdatedDeps; }
    public void setOutdatedDeps(Integer outdatedDeps) { this.outdatedDeps = outdatedDeps; }

    public Integer getPolicyViolations() { return policyViolations; }
    public void setPolicyViolations(Integer policyViolations) { this.policyViolations = policyViolations; }

    public List<String> getTags() { return tags; }
    public void setTags(List<String> tags) { this.tags = tags; }
}
