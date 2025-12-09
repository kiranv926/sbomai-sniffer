import { useState, useCallback } from 'react';
import { aiService } from '../api/services/ai';
import { scanService } from '../api/services/scans';
import { vulnerabilityService } from '../api/services/vulnerabilities';
import { projectsService } from '../api/services/projects';

// Generic API hook state
interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

// Generic API hook
export function useApi<T>(
  apiCall: () => Promise<T>,
  dependencies: any[] = []
) {
  const [state, setState] = useState<ApiState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const result = await apiCall();
      setState({ data: result, loading: false, error: null });
      return result;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An error occurred';
      setState({ data: null, loading: false, error: errorMessage });
      throw error;
    }
  }, dependencies);

  return { ...state, execute };
}

// AI Service Hooks
export function useAIAnalysis(sbomDocumentId: string, analysisType: string = 'VULNERABILITY') {
  return useApi(
    () => aiService.analyzeSbom(sbomDocumentId, analysisType),
    [sbomDocumentId, analysisType]
  );
}

export function useComprehensiveAIAnalysis(sbomDocumentId: string) {
  return useApi(
    () => aiService.performComprehensiveAnalysis(sbomDocumentId),
    [sbomDocumentId]
  );
}

export function useProjectRecommendations(projectId: string) {
  return useApi(
    () => aiService.getProjectRecommendations(projectId),
    [projectId]
  );
}

export function usePortfolioRecommendations() {
  return useApi(
    () => aiService.getPortfolioRecommendations(),
    []
  );
}

export function useVulnerabilityRecommendations(vulnerabilityId: string) {
  return useApi(
    () => aiService.getVulnerabilityRecommendations(vulnerabilityId),
    [vulnerabilityId]
  );
}

export function useAIModelHealth() {
  return useApi(
    () => aiService.getModelHealth(),
    []
  );
}

export function useAIModelPerformance(modelType: string) {
  return useApi(
    () => aiService.getModelPerformance(modelType),
    [modelType]
  );
}

export function useDashboardInsights() {
  return useApi(
    () => aiService.getDashboardInsights(),
    []
  );
}

export function useRiskAssessment(projectId: string) {
  return useApi(
    () => aiService.getRiskAssessment(projectId),
    [projectId]
  );
}

export function useTrendAnalysis(days: number = 30) {
  return useApi(
    () => aiService.getTrendAnalysis(days),
    [days]
  );
}

export function useSecurityInsights() {
  return useApi(
    () => aiService.getSecurityInsights(),
    []
  );
}

// Scan Service Hooks
export function useScans(params?: {
  search?: string;
  status?: string;
  scanType?: string;
  projectId?: string;
  page?: number;
  size?: number;
}) {
  return useApi(
    () => scanService.getScans(params),
    [JSON.stringify(params)]
  );
}

export function useScan(id: string) {
  return useApi(
    () => scanService.getScan(id),
    [id]
  );
}

export function useScanProgress(id: string) {
  return useApi(
    () => scanService.getScanProgress(id),
    [id]
  );
}

export function useScanResults(id: string) {
  return useApi(
    () => scanService.getScanResults(id),
    [id]
  );
}

export function useScanStatistics() {
  return useApi(
    () => scanService.getScanStatistics(),
    []
  );
}

export function useScanTrends(days: number = 30) {
  return useApi(
    () => scanService.getScanTrends(days),
    [days]
  );
}

// Vulnerability Service Hooks
export function useVulnerabilities(params?: {
  search?: string;
  severity?: string;
  status?: string;
  cwe?: string;
  page?: number;
  size?: number;
}) {
  return useApi(
    () => vulnerabilityService.getVulnerabilities(params),
    [JSON.stringify(params)]
  );
}

export function useVulnerability(id: string) {
  return useApi(
    () => vulnerabilityService.getVulnerability(id),
    [id]
  );
}

export function useVulnerabilityStatistics() {
  return useApi(
    () => vulnerabilityService.getVulnerabilityStatistics(),
    []
  );
}

export function useVulnerabilityTrends(days: number = 30) {
  return useApi(
    () => vulnerabilityService.getVulnerabilityTrends(days),
    [days]
  );
}

// Project Service Hooks
export function useProjects(params?: {
  search?: string;
  status?: string;
  team?: string;
  page?: number;
  size?: number;
}) {
  return useApi(
    () => projectsService.getProjects(params),
    [JSON.stringify(params)]
  );
}

export function useProject(id: string) {
  return useApi(
    () => projectsService.getProject(id),
    [id]
  );
}

// Utility hook for manual API calls
export function useManualApi<T>() {
  const [state, setState] = useState<ApiState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(async (apiCall: () => Promise<T>) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const result = await apiCall();
      setState({ data: result, loading: false, error: null });
      return result;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An error occurred';
      setState({ data: null, loading: false, error: errorMessage });
      throw error;
    }
  }, []);

  return { ...state, execute };
}

// Export all services for direct use
export { aiService, scanService, vulnerabilityService, projectsService }; 