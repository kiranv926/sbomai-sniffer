package com.sbomai.core.service;

import com.sbomai.core.dto.AIAnalysisDto;
import com.sbomai.core.dto.AIRecommendationDto;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

/**
 * AI Orchestration Service - Coordinates all AI operations and provides unified interface
 */
@Service
public interface AIOrchestrationService {
    
    /**
     * Perform comprehensive AI analysis on SBOM
     */
    CompletableFuture<AIAnalysisDto> performComprehensiveAnalysis(UUID sbomDocumentId);
    
    /**
     * Perform targeted AI analysis by type
     */
    CompletableFuture<AIAnalysisDto> performTargetedAnalysis(UUID sbomDocumentId, String analysisType);
    
    /**
     * Generate AI recommendations for project
     */
    List<AIRecommendationDto> generateProjectRecommendations(UUID projectId);
    
    /**
     * Generate AI recommendations for portfolio
     */
    List<AIRecommendationDto> generatePortfolioRecommendations();
    
    /**
     * Generate AI recommendations for vulnerability
     */
    List<AIRecommendationDto> generateVulnerabilityRecommendations(UUID vulnerabilityId);
    
    /**
     * Get AI model status and health
     */
    AIModelHealth getModelHealth();
    
    /**
     * Update AI model configuration
     */
    void updateModelConfiguration(String modelType, String configuration);
    
    /**
     * Retrain AI model
     */
    CompletableFuture<Void> retrainModel(String modelType);
    
    /**
     * Get AI model performance metrics
     */
    AIModelPerformance getModelPerformance(String modelType);
    
    /**
     * AI Model Health information
     */
    record AIModelHealth(
        String overallStatus,
        List<ModelStatus> modelStatuses,
        double averageAccuracy,
        long totalPredictions,
        String lastUpdated
    ) {}
    
    /**
     * Individual model status
     */
    record ModelStatus(
        String modelName,
        String status,
        double accuracy,
        long predictions,
        String lastUsed
    ) {}
    
    /**
     * AI Model Performance metrics
     */
    record AIModelPerformance(
        String modelName,
        double accuracy,
        double precision,
        double recall,
        double f1Score,
        long totalPredictions,
        long correctPredictions,
        double averageResponseTime,
        String lastEvaluation
    ) {}
} 