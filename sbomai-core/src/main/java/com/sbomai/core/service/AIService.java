package com.sbomai.core.service;

import com.sbomai.core.dto.AIAnalysisDto;
import com.sbomai.core.dto.AIRecommendationDto;

import java.util.List;
import java.util.UUID;
import java.util.Map;

public interface AIService {
    
    /**
     * Analyze SBOM with AI
     */
    AIAnalysisDto analyzeSbom(UUID sbomDocumentId, String analysisType);
    
    /**
     * Get AI analysis by ID
     */
    AIAnalysisDto getAIAnalysis(UUID analysisId);
    
    /**
     * Get AI analysis by SBOM document ID
     */
    AIAnalysisDto getAIAnalysisBySbomDocument(UUID sbomDocumentId);
    
    /**
     * Get AI recommendations for project
     */
    List<AIRecommendationDto> getAIRecommendations(UUID projectId);
    
    /**
     * Get AI recommendations for vulnerability
     */
    List<AIRecommendationDto> getVulnerabilityRecommendations(UUID vulnerabilityId);
    
    /**
     * Get AI recommendations for portfolio
     */
    List<AIRecommendationDto> getPortfolioRecommendations();
    
    /**
     * Generate AI insights for dashboard
     */
    DashboardInsights getDashboardInsights();
    
    /**
     * Get AI risk assessment
     */
    RiskAssessment getRiskAssessment(UUID projectId);
    
    /**
     * Get AI trend analysis
     */
    TrendAnalysis getTrendAnalysis(int days);
    
    /**
     * Get AI security insights
     */
    SecurityInsights getSecurityInsights();
    
    /**
     * Get AI model status
     */
    ModelStatus getModelStatus();
    
    /**
     * Update AI model configuration
     */
    void updateModelConfiguration(String modelType, String configuration);
    
    /**
     * Retrain AI model
     */
    void retrainModel(String modelType);
    
    /**
     * Get AI model performance metrics
     */
    ModelPerformance getModelPerformance(String modelType);
    
    /**
     * Dashboard insights data class
     */
    record DashboardInsights(
        String summary,
        List<String> keyFindings,
        List<String> recommendations,
        double riskScore,
        String riskLevel,
        long criticalIssues,
        long highPriorityActions,
        String trendAnalysis,
        long totalSboms,
        long policyViolations,
        List<Map<String, Object>> trendData,
        List<Map<String, Object>> projectCoverage,
        List<Map<String, Object>> atRiskRepos,
        Map<String, Object> automationScores,
        Map<String, Object> securityMetrics
    ) {}
    
    /**
     * Risk assessment data class
     */
    record RiskAssessment(
        UUID projectId,
        double overallRiskScore,
        String riskLevel,
        List<String> riskFactors,
        List<String> mitigationStrategies,
        double confidenceScore,
        String assessmentDate
    ) {}
    
    /**
     * Trend analysis data class
     */
    record TrendAnalysis(
        String period,
        List<String> trends,
        List<String> predictions,
        double trendScore,
        String trendDirection,
        List<String> recommendations
    ) {}
    
    /**
     * Security insights data class
     */
    record SecurityInsights(
        String overallSecurityPosture,
        List<String> criticalVulnerabilities,
        List<String> emergingThreats,
        List<String> complianceGaps,
        List<String> remediationPriorities,
        double securityScore
    ) {}
    
    /**
     * Model status data class
     */
    record ModelStatus(
        String modelType,
        String status,
        String version,
        String lastUpdated,
        boolean isAvailable,
        String healthStatus
    ) {}
    
    /**
     * Model performance data class
     */
    record ModelPerformance(
        String modelType,
        double accuracy,
        double precision,
        double recall,
        double f1Score,
        long totalPredictions,
        long correctPredictions,
        String lastEvaluation
    ) {}
} 