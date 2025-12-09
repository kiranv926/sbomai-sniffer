import apiClient from '../client';
import { API_CONFIG } from '../config';

// AI Analysis Types
export interface AIAnalysis {
  id: string;
  sbomDocumentId?: string;
  analysisType: string;
  status: string;
  riskScore: number;
  riskLevel: string;
  analysisSummary: string;
  keyFindings: string[];
  recommendations: string[];
  modelUsed: string;
  modelVersion: string;
  confidenceScore: number;
  analysisDurationMs: number;
  analysisDate: string;
}

// AI Recommendation Types
export interface AIRecommendation {
  id: string;
  title: string;
  description: string;
  category: string;
  priority: string;
  status: string;
  recommendation: string;
  confidenceScore: number;
  modelUsed: string;
  createdDate: string;
}

// AI Model Health Types
export interface AIModelHealth {
  overallStatus: string;
  modelStatuses: ModelStatus[];
  averageAccuracy: number;
  totalPredictions: number;
  lastUpdated: string;
}

export interface ModelStatus {
  modelName: string;
  status: string;
  accuracy: number;
  predictions: number;
  lastUsed: string;
}

// AI Model Performance Types
export interface AIModelPerformance {
  modelName: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1Score: number;
  totalPredictions: number;
  correctPredictions: number;
  averageResponseTime: number;
  lastEvaluation: string;
}

// AI Service Class
class AIService {
  private baseUrl = API_CONFIG.AI_URL;

  // Comprehensive AI Analysis
  async performComprehensiveAnalysis(sbomDocumentId: string): Promise<AIAnalysis> {
    const response = await apiClient.post<AIAnalysis>(
      `${this.baseUrl}/enhanced/comprehensive-analysis?sbomDocumentId=${sbomDocumentId}`
    );
    return response.data;
  }

  // Targeted AI Analysis
  async performTargetedAnalysis(sbomDocumentId: string, analysisType: string): Promise<AIAnalysis> {
    const response = await apiClient.post<AIAnalysis>(
      `${this.baseUrl}/enhanced/targeted-analysis?sbomDocumentId=${sbomDocumentId}&analysisType=${analysisType}`
    );
    return response.data;
  }

  // Synchronous SBOM Analysis
  async analyzeSbom(sbomDocumentId: string, analysisType: string = 'VULNERABILITY'): Promise<AIAnalysis> {
    const response = await apiClient.post<AIAnalysis>(
      `${this.baseUrl}/enhanced/analyze-sbom?sbomDocumentId=${sbomDocumentId}&analysisType=${analysisType}`
    );
    return response.data;
  }

  // Get AI Analysis by ID
  async getAIAnalysis(analysisId: string): Promise<AIAnalysis> {
    const response = await apiClient.get<AIAnalysis>(`${this.baseUrl}/enhanced/analysis/${analysisId}`);
    return response.data;
  }

  // Get AI Analysis by SBOM Document
  async getAIAnalysisBySbomDocument(sbomDocumentId: string): Promise<AIAnalysis> {
    const response = await apiClient.get<AIAnalysis>(`${this.baseUrl}/enhanced/analysis/sbom/${sbomDocumentId}`);
    return response.data;
  }

  // Project Recommendations
  async getProjectRecommendations(projectId: string): Promise<AIRecommendation[]> {
    const response = await apiClient.get<AIRecommendation[]>(`${this.baseUrl}/enhanced/recommendations/project/${projectId}`);
    return response.data;
  }

  // Portfolio Recommendations
  async getPortfolioRecommendations(): Promise<AIRecommendation[]> {
    const response = await apiClient.get<AIRecommendation[]>(`${this.baseUrl}/enhanced/recommendations/portfolio`);
    return response.data;
  }

  // Vulnerability Recommendations
  async getVulnerabilityRecommendations(vulnerabilityId: string): Promise<AIRecommendation[]> {
    const response = await apiClient.get<AIRecommendation[]>(`${this.baseUrl}/enhanced/recommendations/vulnerability/${vulnerabilityId}`);
    return response.data;
  }

  // AI Model Health
  async getModelHealth(): Promise<AIModelHealth> {
    const response = await apiClient.get<AIModelHealth>(`${this.baseUrl}/enhanced/model-health`);
    return response.data;
  }

  // AI Model Performance
  async getModelPerformance(modelType: string): Promise<AIModelPerformance> {
    const response = await apiClient.get<AIModelPerformance>(`${this.baseUrl}/enhanced/model-performance/${modelType}`);
    return response.data;
  }

  // Update Model Configuration
  async updateModelConfiguration(modelType: string, configuration: string): Promise<void> {
    await apiClient.put(`${this.baseUrl}/enhanced/model-configuration?modelType=${modelType}`, configuration);
  }

  // Retrain Model
  async retrainModel(modelType: string): Promise<void> {
    await apiClient.post(`${this.baseUrl}/enhanced/retrain-model?modelType=${modelType}`);
  }

  // Dashboard Insights
  async getDashboardInsights(): Promise<any> {
    const response = await apiClient.get(`${this.baseUrl}/enhanced/dashboard-insights`);
    return response.data;
  }

  // Risk Assessment
  async getRiskAssessment(projectId: string): Promise<any> {
    const response = await apiClient.get(`${this.baseUrl}/enhanced/risk-assessment/${projectId}`);
    return response.data;
  }

  // Trend Analysis
  async getTrendAnalysis(days: number = 30): Promise<any> {
    const response = await apiClient.get(`${this.baseUrl}/enhanced/trend-analysis?days=${days}`);
    return response.data;
  }

  // Security Insights
  async getSecurityInsights(): Promise<any> {
    const response = await apiClient.get(`${this.baseUrl}/enhanced/security-insights`);
    return response.data;
  }

  // Model Status
  async getModelStatus(): Promise<any> {
    const response = await apiClient.get(`${this.baseUrl}/enhanced/model-status`);
    return response.data;
  }
}

// Export singleton instance
export const aiService = new AIService();
export default aiService;
