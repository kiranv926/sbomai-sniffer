import apiClient from '../client';
import { type ApiResponse, type PaginatedResponse } from '../config';

// Project data models
export interface Project {
  id: string;
  name: string;
  description?: string;
  version: string;
  latest: string;
  classifier: string;
  lastBomImport: string;
  bomFormat: string;
  riskScore: number;
  active: boolean;
  policyViolations: number;
  vulnerabilities: number;
  tags?: string[];
  lastModified: string;
  createdBy: string;
  team?: string;
  language?: string;
  repository?: {
    url: string;
    type: 'github' | 'gitlab' | 'bitbucket';
    branch: string;
  };
  status?: 'active' | 'archived' | 'deprecated';
  vulnerabilityCount?: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  dependencyCount?: number;
  outdatedDeps?: number;
  createdAt?: string;
  updatedAt?: string;
}

export interface CreateProjectRequest {
  name: string;
  description?: string;
  version: string;
  classifier: string;
  tags?: string[];
  team?: string;
  language?: string;
  repository?: {
    url: string;
    type: 'github' | 'gitlab' | 'bitbucket';
    branch: string;
  };
}

export interface UpdateProjectRequest extends Partial<CreateProjectRequest> {
  active?: boolean;
  status?: 'active' | 'archived' | 'deprecated';
}

export interface ProjectScan {
  id: string;
  projectId: string;
  scanType: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  startedAt: string;
  completedAt?: string;
  results?: any;
}

export interface ProjectVulnerability {
  id: string;
  projectId: string;
  cveId: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  cvssScore: number;
  affectedComponent: string;
  discoveredAt: string;
  status: 'open' | 'fixed' | 'ignored';
}

export interface ProjectDependency {
  id: string;
  projectId: string;
  name: string;
  version: string;
  latestVersion: string;
  type: string;
  license?: string;
  vulnerabilities: number;
  outdated: boolean;
  direct: boolean;
}

export interface UploadSBOMResponse {
  projectId: string;
  uploadId: string;
  status: 'processing' | 'completed' | 'failed';
  message?: string;
  processedComponents?: number;
  vulnerabilitiesFound?: number;
}

// Projects API service
class ProjectsService {
  private baseUrl = '/projects';

  // GET /api/v1/projects - List all projects
  async getProjects(params?: {
    page?: number;
    size?: number;
    search?: string;
    status?: string;
    team?: string;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }): Promise<PaginatedResponse<Project>> {
    return apiClient.get<Project[]>(this.baseUrl, params) as Promise<PaginatedResponse<Project>>;
  }

  // POST /api/v1/projects - Create new project
  async createProject(project: CreateProjectRequest): Promise<ApiResponse<Project>> {
    return apiClient.post<Project>(this.baseUrl, project);
  }

  // GET /api/v1/projects/{id} - Get project details
  async getProject(id: string): Promise<ApiResponse<Project>> {
    return apiClient.get<Project>(`${this.baseUrl}/${id}`);
  }

  // PUT /api/v1/projects/{id} - Update project
  async updateProject(id: string, project: UpdateProjectRequest): Promise<ApiResponse<Project>> {
    return apiClient.put<Project>(`${this.baseUrl}/${id}`, project);
  }

  // DELETE /api/v1/projects/{id} - Delete project
  async deleteProject(id: string): Promise<ApiResponse<void>> {
    return apiClient.delete<void>(`${this.baseUrl}/${id}`);
  }

  // GET /api/v1/projects/{id}/scans - Get project scans
  async getProjectScans(projectId: string, params?: {
    page?: number;
    size?: number;
    status?: string;
    scanType?: string;
  }): Promise<PaginatedResponse<ProjectScan>> {
    return apiClient.get<ProjectScan[]>(`${this.baseUrl}/${projectId}/scans`, params) as Promise<PaginatedResponse<ProjectScan>>;
  }

  // GET /api/v1/projects/{id}/vulnerabilities - Get project vulnerabilities
  async getProjectVulnerabilities(projectId: string, params?: {
    page?: number;
    size?: number;
    severity?: string;
    status?: string;
    search?: string;
  }): Promise<PaginatedResponse<ProjectVulnerability>> {
    return apiClient.get<ProjectVulnerability[]>(`${this.baseUrl}/${projectId}/vulnerabilities`, params) as Promise<PaginatedResponse<ProjectVulnerability>>;
  }

  // GET /api/v1/projects/{id}/dependencies - Get project dependencies
  async getProjectDependencies(projectId: string, params?: {
    page?: number;
    size?: number;
    type?: string;
    outdated?: boolean;
    search?: string;
  }): Promise<PaginatedResponse<ProjectDependency>> {
    return apiClient.get<ProjectDependency[]>(`${this.baseUrl}/${projectId}/dependencies`, params) as Promise<PaginatedResponse<ProjectDependency>>;
  }

  // POST /api/v1/projects/{id}/upload-sbom - Upload SBOM for project
  async uploadSBOM(
    projectId: string, 
    file: File, 
    onProgress?: (progress: number) => void
  ): Promise<ApiResponse<UploadSBOMResponse>> {
    return apiClient.upload<UploadSBOMResponse>(
      `${this.baseUrl}/${projectId}/upload-sbom`,
      file,
      onProgress
    );
  }

  // Bulk operations
  async bulkDeleteProjects(projectIds: string[]): Promise<ApiResponse<void>> {
    return apiClient.post<void>(`${this.baseUrl}/bulk-delete`, { projectIds });
  }

  async bulkUpdateProjects(projectIds: string[], updates: UpdateProjectRequest): Promise<ApiResponse<Project[]>> {
    return apiClient.put<Project[]>(`${this.baseUrl}/bulk-update`, { projectIds, updates });
  }
}

export const projectsService = new ProjectsService();
export default projectsService; 