package com.sbomai.core.config;

import com.sbomai.core.adapters.LocalAiAnalyzer;
import com.sbomai.core.adapters.OpenAiAnalyzer;
import com.sbomai.core.ports.AiAnalyzer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

import java.util.concurrent.Executor;

/**
 * Configuration for AI analyzer selection and management.
 * 
 * This configuration determines which AI analyzer to use based on
 * availability and configuration settings.
 */
@Configuration
public class AiAnalyzerConfig {

    private static final Logger logger = LoggerFactory.getLogger(AiAnalyzerConfig.class);

    @Value("${sbomai.core.ai.provider:auto}")
    private String aiProvider;

    @Value("${sbomai.core.ai.openai.enabled:true}")
    private boolean openAiEnabled;

    @Value("${sbomai.core.ai.local.enabled:false}")
    private boolean localAiEnabled;

    @Autowired
    private OpenAiAnalyzer openAiAnalyzer;

    @Autowired
    private LocalAiAnalyzer localAiAnalyzer;

    /**
     * Provides the primary AI analyzer based on configuration and availability.
     * 
     * Priority order:
     * 1. OpenAI (if enabled and available)
     * 2. Local AI (if enabled)
     * 3. Fallback to Local AI with warning
     * 
     * @return The primary AI analyzer to use
     */
    @Bean
    @Primary
    public AiAnalyzer primaryAiAnalyzer() {
        logger.info("Configuring AI analyzer with provider: {}", aiProvider);
        
        // Check if OpenAI is preferred and available
        if (("openai".equals(aiProvider) || "auto".equals(aiProvider)) && 
            openAiEnabled && openAiAnalyzer.isAvailable()) {
            logger.info("Using OpenAI analyzer as primary AI provider");
            return openAiAnalyzer;
        }
        
        // Check if Local AI is enabled
        if (("local".equals(aiProvider) || "auto".equals(aiProvider)) && 
            localAiEnabled && localAiAnalyzer.isAvailable()) {
            logger.info("Using Local AI analyzer as primary AI provider");
            return localAiAnalyzer;
        }
        
        // Fallback to Local AI with warning
        if (localAiAnalyzer.isAvailable()) {
            logger.warn("No preferred AI analyzer available, falling back to Local AI analyzer");
            return localAiAnalyzer;
        }
        
        // No AI analyzer available
        logger.error("No AI analyzer is available. Please check configuration.");
        return createNoOpAnalyzer();
    }

    /**
     * Creates a no-op analyzer when no AI services are available.
     */
    private AiAnalyzer createNoOpAnalyzer() {
        return new AiAnalyzer() {
            @Override
            public java.util.concurrent.CompletableFuture<com.sbomai.core.domain.AiAnalysisResult> analyze(
                    com.sbomai.core.domain.SbomDocument sbomDocument) throws com.sbomai.core.ports.AiAnalysisException {
                throw new com.sbomai.core.ports.AiAnalysisException("No AI analyzer is available");
            }

            @Override
            public java.util.concurrent.CompletableFuture<com.sbomai.core.domain.AiAnalysisResult> analyze(
                    com.sbomai.core.domain.SbomDocument sbomDocument, 
                    com.sbomai.core.ports.AnalysisParameters parameters) throws com.sbomai.core.ports.AiAnalysisException {
                throw new com.sbomai.core.ports.AiAnalysisException("No AI analyzer is available");
            }

            @Override
            public String[] getAvailableModels() {
                return new String[0];
            }

            @Override
            public boolean isAvailable() {
                return false;
            }

            @Override
            public com.sbomai.core.ports.AnalyzerInfo getAnalyzerInfo() {
                return new com.sbomai.core.ports.AnalyzerInfo(
                    "No AI Analyzer Available",
                    "0.0.0",
                    new String[0],
                    false,
                    "None"
                );
            }

            @Override
            public com.sbomai.core.ports.CostEstimate estimateCost(com.sbomai.core.domain.SbomDocument sbomDocument) {
                return new com.sbomai.core.ports.CostEstimate(0.0, "USD", "none", 0, "No AI analyzer available");
            }
        };
    }

    /**
     * Provides an executor for AI analysis operations.
     */
    @Bean
    public Executor aiAnalysisExecutor() {
        return java.util.concurrent.Executors.newFixedThreadPool(5);
    }
} 