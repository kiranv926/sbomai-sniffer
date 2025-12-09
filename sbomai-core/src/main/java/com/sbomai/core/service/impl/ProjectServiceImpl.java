package com.sbomai.core.service.impl;

import com.sbomai.core.domain.Project;
import com.sbomai.core.domain.ProjectStatus;
import com.sbomai.core.domain.RepositoryInfo;
import com.sbomai.core.domain.VulnerabilityCount;
import com.sbomai.core.domain.SbomFormat;
import com.sbomai.core.dto.ProjectDto;
import com.sbomai.core.repository.ProjectRepository;
import com.sbomai.core.service.ProjectService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
public class ProjectServiceImpl implements ProjectService {

    @Autowired
    private ProjectRepository projectRepository;

    @Override
    public Page<ProjectDto> getProjects(String search, String status, String team, String sortBy, String sortOrder, Pageable pageable) {
        // For now, return all projects with basic pagination
        Page<Project> projects = projectRepository.findAll(pageable);
        return projects.map(this::convertToDto);
    }

    @Override
    public ProjectDto getProject(UUID id) {
        return projectRepository.findById(id)
                .map(this::convertToDto)
                .orElse(null);
    }

    @Override
    public ProjectDto createProject(ProjectDto projectDto) {
        Project project = convertToEntity(projectDto);
        project.setId(UUID.randomUUID());
        project.setCreatedAt(LocalDateTime.now());
        project.setUpdatedAt(LocalDateTime.now());
        project.setActive(true);
        project.setStatus(ProjectStatus.ACTIVE);
        
        Project savedProject = projectRepository.save(project);
        return convertToDto(savedProject);
    }

    @Override
    public ProjectDto updateProject(UUID id, ProjectDto projectDto) {
        return projectRepository.findById(id)
                .map(existingProject -> {
                    updateProjectFromDto(existingProject, projectDto);
                    existingProject.setUpdatedAt(LocalDateTime.now());
                    Project savedProject = projectRepository.save(existingProject);
                    return convertToDto(savedProject);
                })
                .orElse(null);
    }

    @Override
    public void deleteProject(UUID id) {
        projectRepository.deleteById(id);
    }

    @Override
    public void bulkDeleteProjects(List<UUID> projectIds) {
        projectRepository.deleteAllById(projectIds);
    }

    @Override
    public List<ProjectDto> bulkUpdateProjects(List<UUID> projectIds, ProjectDto updates) {
        List<Project> projects = projectRepository.findAllById(projectIds);
        projects.forEach(project -> updateProjectFromDto(project, updates));
        List<Project> savedProjects = projectRepository.saveAll(projects);
        return savedProjects.stream().map(this::convertToDto).collect(Collectors.toList());
    }

    @Override
    public String uploadSBOM(UUID projectId, MultipartFile file) {
        // TODO: Implement SBOM upload logic
        return "SBOM uploaded successfully for project: " + projectId;
    }

    @Override
    public Page<ProjectDto> getProjectScans(UUID projectId, String status, String scanType, Pageable pageable) {
        // TODO: Implement project scans logic
        return Page.empty(pageable);
    }

    @Override
    public Page<ProjectDto> getProjectVulnerabilities(UUID projectId, String severity, String status, String search, Pageable pageable) {
        // TODO: Implement project vulnerabilities logic
        return Page.empty(pageable);
    }

    @Override
    public Page<ProjectDto> getProjectDependencies(UUID projectId, String type, Boolean outdated, String search, Pageable pageable) {
        // TODO: Implement project dependencies logic
        return Page.empty(pageable);
    }

    @Override
    public Long getTotalProjects() {
        return projectRepository.count();
    }

    @Override
    public Long getProjectsWithVulnerabilities() {
        // TODO: Implement logic to count projects with vulnerabilities
        return 0L;
    }

    @Override
    public Double getAverageRiskScore() {
        // TODO: Implement logic to calculate average risk score
        return 0.0;
    }

    @Override
    public List<ProjectDto> getHighRiskProjects(Integer minRiskScore) {
        // TODO: Implement logic to get high risk projects
        return List.of();
    }

    @Override
    public List<Object[]> getProjectCountByTeam() {
        // TODO: Implement logic to get project count by team
        return List.of();
    }

    private ProjectDto convertToDto(Project project) {
        ProjectDto dto = new ProjectDto();
        dto.setId(project.getId());
        dto.setName(project.getName());
        dto.setVersion(project.getVersion());
        dto.setDescription(project.getDescription());
        dto.setClassifier(project.getClassifier());
        dto.setLanguage(project.getLanguage());
        dto.setTeam(project.getTeam());
        dto.setStatus(project.getStatus() != null ? project.getStatus().name() : null);
        
        // Handle repository info
        RepositoryInfo repo = project.getRepository();
        if (repo != null) {
            dto.setRepoUrl(repo.getUrl());
            dto.setRepoType(repo.getType());
            dto.setRepoBranch(repo.getBranch());
        }
        
        dto.setBomFormat(project.getBomFormat() != null ? project.getBomFormat().getCode() : null);
        dto.setLatestVersion(project.getLatestVersion());
        dto.setCreatedBy(project.getCreatedBy());
        dto.setCreatedAt(project.getCreatedAt());
        dto.setUpdatedAt(project.getUpdatedAt());
        dto.setLastModified(project.getLastModified());
        dto.setLastBomImport(project.getLastBomImport());
        dto.setActive(project.getActive());
        dto.setRiskScore(project.getRiskScore());
        dto.setVulnerabilities(project.getVulnerabilities());
        
        // Handle vulnerability counts
        VulnerabilityCount vulnCount = project.getVulnerabilityCount();
        if (vulnCount != null) {
            dto.setCriticalCount(vulnCount.getCritical());
            dto.setHighCount(vulnCount.getHigh());
            dto.setMediumCount(vulnCount.getMedium());
            dto.setLowCount(vulnCount.getLow());
        }
        
        dto.setDependencyCount(project.getDependencyCount());
        dto.setOutdatedDeps(project.getOutdatedDeps());
        dto.setPolicyViolations(project.getPolicyViolations());
        
        // Handle tags
        if (project.getTags() != null) {
            dto.setTags(project.getTags().stream().collect(Collectors.toList()));
        }
        
        return dto;
    }

    private Project convertToEntity(ProjectDto dto) {
        Project project = new Project();
        project.setId(dto.getId());
        project.setName(dto.getName());
        project.setVersion(dto.getVersion());
        project.setDescription(dto.getDescription());
        project.setClassifier(dto.getClassifier());
        project.setLanguage(dto.getLanguage());
        project.setTeam(dto.getTeam());
        project.setStatus(parseProjectStatus(dto.getStatus()));
        
        // Handle repository info
        if (dto.getRepoUrl() != null || dto.getRepoType() != null || dto.getRepoBranch() != null) {
            RepositoryInfo repo = new RepositoryInfo(dto.getRepoUrl(), dto.getRepoType(), dto.getRepoBranch());
            project.setRepository(repo);
        }
        
        project.setBomFormat(dto.getBomFormat() != null ? SbomFormat.fromCode(dto.getBomFormat()) : null);
        project.setLatestVersion(dto.getLatestVersion());
        project.setCreatedBy(dto.getCreatedBy());
        project.setCreatedAt(dto.getCreatedAt());
        project.setUpdatedAt(dto.getUpdatedAt());
        project.setLastModified(dto.getLastModified());
        project.setLastBomImport(dto.getLastBomImport());
        project.setActive(dto.getActive());
        project.setRiskScore(dto.getRiskScore());
        project.setVulnerabilities(dto.getVulnerabilities());
        
        // Handle vulnerability counts
        if (dto.getCriticalCount() != null || dto.getHighCount() != null || 
            dto.getMediumCount() != null || dto.getLowCount() != null) {
            VulnerabilityCount vulnCount = new VulnerabilityCount(
                dto.getCriticalCount(), dto.getHighCount(), 
                dto.getMediumCount(), dto.getLowCount()
            );
            project.setVulnerabilityCount(vulnCount);
        }
        
        project.setDependencyCount(dto.getDependencyCount());
        project.setOutdatedDeps(dto.getOutdatedDeps());
        project.setPolicyViolations(dto.getPolicyViolations());
        
        // Handle tags
        if (dto.getTags() != null) {
            project.setTags(dto.getTags().stream().collect(Collectors.toSet()));
        }
        
        return project;
    }

    private void updateProjectFromDto(Project project, ProjectDto dto) {
        if (dto.getName() != null) project.setName(dto.getName());
        if (dto.getVersion() != null) project.setVersion(dto.getVersion());
        if (dto.getDescription() != null) project.setDescription(dto.getDescription());
        if (dto.getClassifier() != null) project.setClassifier(dto.getClassifier());
        if (dto.getLanguage() != null) project.setLanguage(dto.getLanguage());
        if (dto.getTeam() != null) project.setTeam(dto.getTeam());
        if (dto.getStatus() != null) project.setStatus(parseProjectStatus(dto.getStatus()));
        
        // Handle repository info
        if (dto.getRepoUrl() != null || dto.getRepoType() != null || dto.getRepoBranch() != null) {
            RepositoryInfo repo = project.getRepository();
            if (repo == null) {
                repo = new RepositoryInfo();
                project.setRepository(repo);
            }
            if (dto.getRepoUrl() != null) repo.setUrl(dto.getRepoUrl());
            if (dto.getRepoType() != null) repo.setType(dto.getRepoType());
            if (dto.getRepoBranch() != null) repo.setBranch(dto.getRepoBranch());
        }
        
        if (dto.getBomFormat() != null) project.setBomFormat(SbomFormat.fromCode(dto.getBomFormat()));
        if (dto.getLatestVersion() != null) project.setLatestVersion(dto.getLatestVersion());
        if (dto.getCreatedBy() != null) project.setCreatedBy(dto.getCreatedBy());
        if (dto.getActive() != null) project.setActive(dto.getActive());
        if (dto.getRiskScore() != null) project.setRiskScore(dto.getRiskScore());
        if (dto.getVulnerabilities() != null) project.setVulnerabilities(dto.getVulnerabilities());
        
        // Handle vulnerability counts
        if (dto.getCriticalCount() != null || dto.getHighCount() != null || 
            dto.getMediumCount() != null || dto.getLowCount() != null) {
            VulnerabilityCount vulnCount = project.getVulnerabilityCount();
            if (vulnCount == null) {
                vulnCount = new VulnerabilityCount();
                project.setVulnerabilityCount(vulnCount);
            }
            if (dto.getCriticalCount() != null) vulnCount.setCritical(dto.getCriticalCount());
            if (dto.getHighCount() != null) vulnCount.setHigh(dto.getHighCount());
            if (dto.getMediumCount() != null) vulnCount.setMedium(dto.getMediumCount());
            if (dto.getLowCount() != null) vulnCount.setLow(dto.getLowCount());
        }
        
        if (dto.getDependencyCount() != null) project.setDependencyCount(dto.getDependencyCount());
        if (dto.getOutdatedDeps() != null) project.setOutdatedDeps(dto.getOutdatedDeps());
        if (dto.getPolicyViolations() != null) project.setPolicyViolations(dto.getPolicyViolations());
        
        // Handle tags
        if (dto.getTags() != null) {
            project.setTags(dto.getTags().stream().collect(Collectors.toSet()));
        }
    }
    
    private ProjectStatus parseProjectStatus(String status) {
        if (status == null || status.trim().isEmpty()) {
            return ProjectStatus.ACTIVE;
        }
        try {
            return ProjectStatus.valueOf(status.toUpperCase());
        } catch (IllegalArgumentException e) {
            // Default to ACTIVE if invalid status provided
            return ProjectStatus.ACTIVE;
        }
    }
}
