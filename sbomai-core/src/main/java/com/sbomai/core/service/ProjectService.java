package com.sbomai.core.service;

import com.sbomai.core.dto.ProjectDto;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.UUID;

public interface ProjectService {
    
    Page<ProjectDto> getProjects(String search, String status, String team, String sortBy, String sortOrder, Pageable pageable);
    
    ProjectDto getProject(UUID id);
    
    ProjectDto createProject(ProjectDto projectDto);
    
    ProjectDto updateProject(UUID id, ProjectDto projectDto);
    
    void deleteProject(UUID id);
    
    void bulkDeleteProjects(List<UUID> projectIds);
    
    List<ProjectDto> bulkUpdateProjects(List<UUID> projectIds, ProjectDto updates);
    
    String uploadSBOM(UUID projectId, MultipartFile file);
    
    Page<ProjectDto> getProjectScans(UUID projectId, String status, String scanType, Pageable pageable);
    
    Page<ProjectDto> getProjectVulnerabilities(UUID projectId, String severity, String status, String search, Pageable pageable);
    
    Page<ProjectDto> getProjectDependencies(UUID projectId, String type, Boolean outdated, String search, Pageable pageable);
    
    // Statistics methods
    Long getTotalProjects();
    
    Long getProjectsWithVulnerabilities();
    
    Double getAverageRiskScore();
    
    List<ProjectDto> getHighRiskProjects(Integer minRiskScore);
    
    List<Object[]> getProjectCountByTeam();
}
