import { useState, useEffect, useCallback } from 'react';
import { 
  projectsService, 
  Project, 
  CreateProjectRequest, 
  UpdateProjectRequest,
  ProjectScan,
  ProjectVulnerability,
  ProjectDependency,
  UploadSBOMResponse
} from '../api/services/projects';
import { ApiError } from '../api/config';

// Hook for managing projects list
export const useProjects = (params?: {
  page?: number;
  size?: number;
  search?: string;
  status?: string;
  team?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}) => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    page: 1,
    size: 10,
    total: 0,
    totalPages: 0
  });

  const fetchProjects = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await projectsService.getProjects(params);
      setProjects(response.data);
      setPagination(response.pagination);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to fetch projects');
    } finally {
      setLoading(false);
    }
  }, [params]);

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  return {
    projects,
    loading,
    error,
    pagination,
    refetch: fetchProjects
  };
};

// Hook for managing a single project
export const useProject = (id: string) => {
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProject = useCallback(async () => {
    if (!id) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await projectsService.getProject(id);
      setProject(response.data);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to fetch project');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchProject();
  }, [fetchProject]);

  return {
    project,
    loading,
    error,
    refetch: fetchProject
  };
};

// Hook for project CRUD operations
export const useProjectOperations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createProject = useCallback(async (projectData: CreateProjectRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await projectsService.createProject(projectData);
      return response.data;
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to create project');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateProject = useCallback(async (id: string, projectData: UpdateProjectRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await projectsService.updateProject(id, projectData);
      return response.data;
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to update project');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteProject = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      await projectsService.deleteProject(id);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to delete project');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const bulkDeleteProjects = useCallback(async (projectIds: string[]) => {
    setLoading(true);
    setError(null);
    try {
      await projectsService.bulkDeleteProjects(projectIds);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to delete projects');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const bulkUpdateProjects = useCallback(async (projectIds: string[], updates: UpdateProjectRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await projectsService.bulkUpdateProjects(projectIds, updates);
      return response.data;
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to update projects');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    createProject,
    updateProject,
    deleteProject,
    bulkDeleteProjects,
    bulkUpdateProjects
  };
};

// Hook for project scans
export const useProjectScans = (projectId: string, params?: {
  page?: number;
  size?: number;
  status?: string;
  scanType?: string;
}) => {
  const [scans, setScans] = useState<ProjectScan[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    page: 1,
    size: 10,
    total: 0,
    totalPages: 0
  });

  const fetchScans = useCallback(async () => {
    if (!projectId) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await projectsService.getProjectScans(projectId, params);
      setScans(response.data);
      setPagination(response.pagination);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to fetch project scans');
    } finally {
      setLoading(false);
    }
  }, [projectId, params]);

  useEffect(() => {
    fetchScans();
  }, [fetchScans]);

  return {
    scans,
    loading,
    error,
    pagination,
    refetch: fetchScans
  };
};

// Hook for project vulnerabilities
export const useProjectVulnerabilities = (projectId: string, params?: {
  page?: number;
  size?: number;
  severity?: string;
  status?: string;
  search?: string;
}) => {
  const [vulnerabilities, setVulnerabilities] = useState<ProjectVulnerability[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    page: 1,
    size: 10,
    total: 0,
    totalPages: 0
  });

  const fetchVulnerabilities = useCallback(async () => {
    if (!projectId) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await projectsService.getProjectVulnerabilities(projectId, params);
      setVulnerabilities(response.data);
      setPagination(response.pagination);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to fetch project vulnerabilities');
    } finally {
      setLoading(false);
    }
  }, [projectId, params]);

  useEffect(() => {
    fetchVulnerabilities();
  }, [fetchVulnerabilities]);

  return {
    vulnerabilities,
    loading,
    error,
    pagination,
    refetch: fetchVulnerabilities
  };
};

// Hook for project dependencies
export const useProjectDependencies = (projectId: string, params?: {
  page?: number;
  size?: number;
  type?: string;
  outdated?: boolean;
  search?: string;
}) => {
  const [dependencies, setDependencies] = useState<ProjectDependency[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    page: 1,
    size: 10,
    total: 0,
    totalPages: 0
  });

  const fetchDependencies = useCallback(async () => {
    if (!projectId) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await projectsService.getProjectDependencies(projectId, params);
      setDependencies(response.data);
      setPagination(response.pagination);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to fetch project dependencies');
    } finally {
      setLoading(false);
    }
  }, [projectId, params]);

  useEffect(() => {
    fetchDependencies();
  }, [fetchDependencies]);

  return {
    dependencies,
    loading,
    error,
    pagination,
    refetch: fetchDependencies
  };
};

// Hook for SBOM upload
export const useSBOMUpload = () => {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const uploadSBOM = useCallback(async (projectId: string, file: File) => {
    setUploading(true);
    setProgress(0);
    setError(null);
    
    try {
      const response = await projectsService.uploadSBOM(
        projectId, 
        file, 
        (progressValue) => setProgress(progressValue)
      );
      return response.data;
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to upload SBOM');
      throw err;
    } finally {
      setUploading(false);
      setProgress(0);
    }
  }, []);

  return {
    uploading,
    progress,
    error,
    uploadSBOM
  };
};
