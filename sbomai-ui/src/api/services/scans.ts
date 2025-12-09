import apiClient from '../client';
import { API_CONFIG } from '../config';

// Scan Types
export interface Scan {
  id: string;
  projectId?: string;
  projectName: string;
  sourcePath: string;
  sourceType: string;
  status: string;
  createdAt: string;
  updatedAt?: string;
  riskScore?: number;
  vulnerabilitiesFound?: number;
  errorMessage?: string;
  sbomDocumentId?: string;
}

export interface ScanProgress {
  id: string;
  status: string;
  progress: number;
  currentStep: string;
  estimatedTimeRemaining: string;
  processedItems: number;
  totalItems: number;
}

export interface ScanResults {
  id: string;
  status: string;
  totalComponents: number;
  totalDependencies: number;
  criticalVulnerabilities: number;
  riskScore: number;
  summary: string;
  findings: string[];
}

export interface ScanStatistics {
  totalScans: number;
  completedScans: number;
  failedScans: number;
  cancelledScans: number;
  successRate: number;
  averageScanTime: number;
  totalComponentsScanned: number;
  totalDependenciesScanned: number;
}

export interface ScanTrend {
  date: string;
  totalScans: number;
  successfulScans: number;
  failedScans: number;
  averageRiskScore: number;
}

export interface ScanLog {
  timestamp: string;
  level: string;
  message: string;
  details: string;
}

// Scan Service Class
class ScanService {
  private baseUrl = API_CONFIG.BASE_URL;

  // Get all scans with filtering
  async getScans(params?: {
    search?: string;
    status?: string;
    scanType?: string;
    projectId?: string;
    page?: number;
    size?: number;
  }): Promise<PaginatedResponse<Scan>> {
    const response = await apiClient.get<Scan[]>(`${this.baseUrl}/scans`, params);
    return response as Promise<PaginatedResponse<Scan>>;
  }

  // Get scan by ID
  async getScan(id: string): Promise<Scan> {
    const response = await apiClient.get<Scan>(`${this.baseUrl}/scans/${id}`);
    return response.data;
  }

  // Get scans by project
  async getScansByProject(projectId: string, params?: {
    status?: string;
    scanType?: string;
    page?: number;
    size?: number;
  }): Promise<PaginatedResponse<Scan>> {
    const response = await apiClient.get<Scan[]>(`${this.baseUrl}/scans/project/${projectId}`, params);
    return response as Promise<PaginatedResponse<Scan>>;
  }

  // Create new scan
  async createScan(scan: Partial<Scan>): Promise<Scan> {
    const response = await apiClient.post<Scan>(`${this.baseUrl}/scans`, scan);
    return response.data;
  }

  // Update scan
  async updateScan(id: string, scan: Partial<Scan>): Promise<Scan> {
    const response = await apiClient.put<Scan>(`${this.baseUrl}/scans/${id}`, scan);
    return response.data;
  }

  // Delete scan
  async deleteScan(id: string): Promise<void> {
    await apiClient.delete(`${this.baseUrl}/scans/${id}`);
  }

  // Start scan
  async startScan(id: string): Promise<Scan> {
    const response = await apiClient.post<Scan>(`${this.baseUrl}/scans/${id}/start`);
    return response.data;
  }

  // Stop scan
  async stopScan(id: string): Promise<Scan> {
    const response = await apiClient.post<Scan>(`${this.baseUrl}/scans/${id}/stop`);
    return response.data;
  }

  // Get scan status
  async getScanStatus(id: string): Promise<string> {
    const response = await apiClient.get<string>(`${this.baseUrl}/scans/${id}/status`);
    return response.data;
  }

  // Get scan progress
  async getScanProgress(id: string): Promise<ScanProgress> {
    const response = await apiClient.get<ScanProgress>(`${this.baseUrl}/scans/${id}/progress`);
    return response.data;
  }

  // Get scan results
  async getScanResults(id: string): Promise<ScanResults> {
    const response = await apiClient.get<ScanResults>(`${this.baseUrl}/scans/${id}/results`);
    return response.data;
  }

  // Get scan statistics
  async getScanStatistics(): Promise<ScanStatistics> {
    const response = await apiClient.get<ScanStatistics>(`${this.baseUrl}/scans/statistics`);
    return response.data;
  }

  // Get scan trends
  async getScanTrends(days: number = 30): Promise<ScanTrend[]> {
    const response = await apiClient.get<ScanTrend[]>(`${this.baseUrl}/scans/trends?days=${days}`);
    return response.data;
  }

  // Bulk delete scans
  async bulkDeleteScans(ids: string[]): Promise<void> {
    await apiClient.post(`${this.baseUrl}/scans/bulk-delete`, { ids });
  }

  // Retry scan
  async retryScan(id: string): Promise<Scan> {
    const response = await apiClient.post<Scan>(`${this.baseUrl}/scans/${id}/retry`);
    return response.data;
  }

  // Get scan logs
  async getScanLogs(id: string): Promise<ScanLog[]> {
    const response = await apiClient.get<ScanLog[]>(`${this.baseUrl}/scans/${id}/logs`);
    return response.data;
  }
}

// Export singleton instance
export const scanService = new ScanService();
export default scanService;
