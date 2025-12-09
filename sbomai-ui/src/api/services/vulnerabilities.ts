import apiClient from '../client';
import { API_CONFIG } from '../config';

// Vulnerability Types
export interface Vulnerability {
  id: string;
  cveId: string;
  title: string;
  description: string;
  severity: string;
  cvssScore: number;
  status: string;
  createdDate: string;
  lastModifiedDate?: string;
  publishedDate?: string;
  lastUpdated?: string;
  projectId?: string;
  componentId?: string;
  affectedVersions?: string;
  cvssVector?: string;
  cvssVersion?: string;
  fixedVersions?: string;
  ghsaId?: string;
  osvId?: string;
  references?: string;
  source?: string;
  sourceUrl?: string;
}

export interface VulnerabilityStatistics {
  totalVulnerabilities: number;
  criticalCount: number;
  highCount: number;
  mediumCount: number;
  lowCount: number;
  openCount: number;
  fixedCount: number;
  ignoredCount: number;
  averageCvssScore: number;
  projectsAffected: number;
}

export interface VulnerabilityTrend {
  date: string;
  criticalCount: number;
  highCount: number;
  mediumCount: number;
  lowCount: number;
  totalCount: number;
}

// Vulnerability Service Class
class VulnerabilityService {
  private baseUrl = API_CONFIG.BASE_URL;

  // Get all vulnerabilities with filtering
  async getVulnerabilities(params?: {
    search?: string;
    severity?: string;
    status?: string;
    cwe?: string;
    page?: number;
    size?: number;
  }): Promise<PaginatedResponse<Vulnerability>> {
    const response = await apiClient.get<Vulnerability[]>(`${this.baseUrl}/vulnerabilities`, params);
    return response as Promise<PaginatedResponse<Vulnerability>>;
  }

  // Get vulnerability by ID
  async getVulnerability(id: string): Promise<Vulnerability> {
    const response = await apiClient.get<Vulnerability>(`${this.baseUrl}/vulnerabilities/${id}`);
    return response.data;
  }

  // Get vulnerabilities by project
  async getVulnerabilitiesByProject(projectId: string, params?: {
    severity?: string;
    status?: string;
    page?: number;
    size?: number;
  }): Promise<{ data: Vulnerability[]; pagination: any }> {
    const response = await apiClient.get<Vulnerability[]>(`${this.baseUrl}/vulnerabilities/project/${projectId}`, params);
    return response;
  }

  // Get vulnerabilities by component
  async getVulnerabilitiesByComponent(componentId: string, params?: {
    severity?: string;
    status?: string;
    page?: number;
    size?: number;
  }): Promise<{ data: Vulnerability[]; pagination: any }> {
    const response = await apiClient.get<Vulnerability[]>(`${this.baseUrl}/vulnerabilities/component/${componentId}`, params);
    return response;
  }

  // Create new vulnerability
  async createVulnerability(vulnerability: Partial<Vulnerability>): Promise<Vulnerability> {
    const response = await apiClient.post<Vulnerability>(`${this.baseUrl}/vulnerabilities`, vulnerability);
    return response.data;
  }

  // Update vulnerability
  async updateVulnerability(id: string, vulnerability: Partial<Vulnerability>): Promise<Vulnerability> {
    const response = await apiClient.put<Vulnerability>(`${this.baseUrl}/vulnerabilities/${id}`, vulnerability);
    return response.data;
  }

  // Delete vulnerability
  async deleteVulnerability(id: string): Promise<void> {
    await apiClient.delete(`${this.baseUrl}/vulnerabilities/${id}`);
  }

  // Get vulnerability statistics
  async getVulnerabilityStatistics(): Promise<VulnerabilityStatistics> {
    const response = await apiClient.get<VulnerabilityStatistics>(`${this.baseUrl}/vulnerabilities/statistics`);
    return response.data;
  }

  // Get vulnerability trends
  async getVulnerabilityTrends(days: number = 30): Promise<VulnerabilityTrend[]> {
    const response = await apiClient.get<VulnerabilityTrend[]>(`${this.baseUrl}/vulnerabilities/trends?days=${days}`);
    return response.data;
  }

  // Bulk update vulnerabilities
  async bulkUpdateVulnerabilities(ids: string[], updates: Partial<Vulnerability>): Promise<Vulnerability[]> {
    const response = await apiClient.put<Vulnerability[]>(`${this.baseUrl}/vulnerabilities/bulk-update`, { ids, updates });
    return response.data;
  }

  // Bulk delete vulnerabilities
  async bulkDeleteVulnerabilities(ids: string[]): Promise<void> {
    await apiClient.post(`${this.baseUrl}/vulnerabilities/bulk-delete`, { ids });
  }

  // Get vulnerability by CVE ID
  async getVulnerabilityByCveId(cveId: string): Promise<Vulnerability> {
    const response = await apiClient.get<Vulnerability>(`${this.baseUrl}/vulnerabilities/cve/${cveId}`);
    return response.data;
  }

  // Get vulnerabilities by severity
  async getVulnerabilitiesBySeverity(severity: string, params?: {
    page?: number;
    size?: number;
  }): Promise<{ data: Vulnerability[]; pagination: any }> {
    const response = await apiClient.get<Vulnerability[]>(`${this.baseUrl}/vulnerabilities/severity/${severity}`, params);
    return response;
  }

  // Get vulnerabilities by CWE
  async getVulnerabilitiesByCwe(cwe: string, params?: {
    page?: number;
    size?: number;
  }): Promise<{ data: Vulnerability[]; pagination: any }> {
    const response = await apiClient.get<Vulnerability[]>(`${this.baseUrl}/vulnerabilities/cwe/${cwe}`, params);
    return response;
  }
}

// Export singleton instance
export const vulnerabilityService = new VulnerabilityService();
export default vulnerabilityService;
