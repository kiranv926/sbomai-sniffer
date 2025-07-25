package com.sbomai.core.ports;

import com.sbomai.core.domain.SbomDocument;
import com.sbomai.core.domain.AiAnalysisResult;

import java.util.concurrent.CompletableFuture;

/**
 * Core interface for AI-powered SBOM analysis operations.
 * 
 * This interface defines the contract for analyzing SBOM documents
 * using AI models to provide risk assessment and recommendations.
 */
public interface AiAnalyzer {

    /**
     * Analyzes an SBOM document using AI to assess risks and provide insights.
     * 
     * @param sbomDocument The SBOM document to analyze
     * @return CompletableFuture containing the AI analysis result
     * @throws AiAnalysisException if analysis fails
     */
    CompletableFuture<AiAnalysisResult> analyze(SbomDocument sbomDocument) throws AiAnalysisException;

    /**
     * Analyzes an SBOM document with specific analysis parameters.
     * 
     * @param sbomDocument The SBOM document to analyze
     * @param parameters Analysis parameters (model, confidence threshold, etc.)
     * @return CompletableFuture containing the AI analysis result
     * @throws AiAnalysisException if analysis fails
     */
    CompletableFuture<AiAnalysisResult> analyze(SbomDocument sbomDocument, AnalysisParameters parameters) throws AiAnalysisException;

    /**
     * Gets available AI models for analysis.
     * 
     * @return Array of available model names
     */
    String[] getAvailableModels();

    /**
     * Checks if the AI analyzer is available and ready to use.
     * 
     * @return true if the analyzer is available, false otherwise
     */
    boolean isAvailable();

    /**
     * Gets the analyzer version and capabilities.
     * 
     * @return Analyzer information
     */
    AnalyzerInfo getAnalyzerInfo();

    /**
     * Gets the cost estimate for analyzing an SBOM document.
     * 
     * @param sbomDocument The SBOM document to estimate cost for
     * @return Cost estimate in the configured currency
     */
    CostEstimate estimateCost(SbomDocument sbomDocument);
} 