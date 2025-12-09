package com.sbomai.core.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class AIRecommendationDto {
    
    private UUID id;
    private String title;
    private String description;
    private String impact;
    private String category;
    private String priority;
    private String status;
    private List<String> affectedProjects;
    private Integer affectedProjectsCount;
    private List<String> affectedComponents;
    private String recommendation;
    private String rationale;
    private Double confidenceScore;
    private String modelUsed;
    private String modelVersion;
    private List<String> tags;
    private String source;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime createdDate;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime updatedDate;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime implementedDate;
    
    private String implementedBy;
    private String implementationNotes;
    
    // Constructors
    public AIRecommendationDto() {}
    
    public AIRecommendationDto(UUID id, String title, String description, String impact, 
                              String category, String priority, String status) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.impact = impact;
        this.category = category;
        this.priority = priority;
        this.status = status;
    }
    
    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public String getImpact() { return impact; }
    public void setImpact(String impact) { this.impact = impact; }
    
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    
    public String getPriority() { return priority; }
    public void setPriority(String priority) { this.priority = priority; }
    
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    
    public List<String> getAffectedProjects() { return affectedProjects; }
    public void setAffectedProjects(List<String> affectedProjects) { this.affectedProjects = affectedProjects; }
    
    public Integer getAffectedProjectsCount() { return affectedProjectsCount; }
    public void setAffectedProjectsCount(Integer affectedProjectsCount) { this.affectedProjectsCount = affectedProjectsCount; }
    
    public List<String> getAffectedComponents() { return affectedComponents; }
    public void setAffectedComponents(List<String> affectedComponents) { this.affectedComponents = affectedComponents; }
    
    public String getRecommendation() { return recommendation; }
    public void setRecommendation(String recommendation) { this.recommendation = recommendation; }
    
    public String getRationale() { return rationale; }
    public void setRationale(String rationale) { this.rationale = rationale; }
    
    public Double getConfidenceScore() { return confidenceScore; }
    public void setConfidenceScore(Double confidenceScore) { this.confidenceScore = confidenceScore; }
    
    public String getModelUsed() { return modelUsed; }
    public void setModelUsed(String modelUsed) { this.modelUsed = modelUsed; }
    
    public String getModelVersion() { return modelVersion; }
    public void setModelVersion(String modelVersion) { this.modelVersion = modelVersion; }
    
    public List<String> getTags() { return tags; }
    public void setTags(List<String> tags) { this.tags = tags; }
    
    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }
    
    public LocalDateTime getCreatedDate() { return createdDate; }
    public void setCreatedDate(LocalDateTime createdDate) { this.createdDate = createdDate; }
    
    public LocalDateTime getUpdatedDate() { return updatedDate; }
    public void setUpdatedDate(LocalDateTime updatedDate) { this.updatedDate = updatedDate; }
    
    public LocalDateTime getImplementedDate() { return implementedDate; }
    public void setImplementedDate(LocalDateTime implementedDate) { this.implementedDate = implementedDate; }
    
    public String getImplementedBy() { return implementedBy; }
    public void setImplementedBy(String implementedBy) { this.implementedBy = implementedBy; }
    
    public String getImplementationNotes() { return implementationNotes; }
    public void setImplementationNotes(String implementationNotes) { this.implementationNotes = implementationNotes; }
} 