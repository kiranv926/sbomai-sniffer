package com.sbomai.core.adapters;

import com.sbomai.core.domain.AiAnalysisResult;
import com.sbomai.core.domain.RiskLevel;
import com.sbomai.core.domain.AnalysisStatus;
import com.sbomai.core.domain.SbomDocument;
import com.sbomai.core.ports.AiAnalyzer;
import com.sbomai.core.ports.AiAnalysisException;
import com.sbomai.core.ports.AnalysisParameters;
import com.sbomai.core.ports.AnalyzerInfo;
import com.sbomai.core.ports.CostEstimate;
import com.theokanning.openai.completion.chat.ChatCompletionRequest;
import com.theokanning.openai.completion.chat.ChatMessage;
import com.theokanning.openai.service.OpenAiService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;

/**
 * OpenAI-based implementation of the AiAnalyzer interface.
 * 
 * This adapter provides AI-powered SBOM analysis using OpenAI's GPT models
 * to assess security risks, provide recommendations, and generate insights.
 */
@Service
public class OpenAiAnalyzer implements AiAnalyzer {

    private static final Logger logger = LoggerFactory.getLogger(OpenAiAnalyzer.class);
    
    private final OpenAiService openAiService;
    private final Executor analysisExecutor;
    
    @Value("${sbomai.core.ai.openai.model:gpt-4}")
    private String defaultModel;
    
    @Value("${sbomai.core.ai.openai.max-tokens:4000}")
    private int defaultMaxTokens;
    
    @Value("${sbomai.core.ai.openai.temperature:0.3}")
    private double defaultTemperature;
    
    @Value("${sbomai.core.ai.openai.enabled:true}")
    private boolean enabled;

    public OpenAiAnalyzer(
            @Value("${sbomai.core.ai.openai.api-key:}") String apiKey,
            Executor analysisExecutor) {
        this.analysisExecutor = analysisExecutor;
        
        if (apiKey != null && !apiKey.trim().isEmpty()) {
            this.openAiService = new OpenAiService(apiKey, Duration.ofSeconds(60));
            logger.info("OpenAI service initialized successfully");
        } else {
            this.openAiService = null;
            logger.warn("OpenAI API key not provided, AI analysis will be disabled");
        }
    }

    @Override
    public CompletableFuture<AiAnalysisResult> analyze(SbomDocument sbomDocument) throws AiAnalysisException {
        return analyze(sbomDocument, getDefaultParameters());
    }

    @Override
    public CompletableFuture<AiAnalysisResult> analyze(SbomDocument sbomDocument, AnalysisParameters parameters) throws AiAnalysisException {
        if (!isAvailable()) {
            throw new AiAnalysisException("OpenAI analyzer is not available");
        }

        return CompletableFuture.supplyAsync(() -> {
            long startTime = System.currentTimeMillis();
            AiAnalysisResult result = new AiAnalysisResult();
            result.setStatus(AnalysisStatus.PENDING);
            
            try {
                logger.info("Starting AI analysis for SBOM document: {}", sbomDocument.getDocumentName());
                
                // Prepare the analysis prompt
                String prompt = buildAnalysisPrompt(sbomDocument, parameters);
                
                // Create chat completion request
                ChatCompletionRequest request = ChatCompletionRequest.builder()
                    .model(parameters.getModel())
                    .messages(List.of(
                        new ChatMessage("system", getSystemPrompt()),
                        new ChatMessage("user", prompt)
                    ))
                    .maxTokens(parameters.getMaxTokens())
                    .temperature(parameters.getTemperature())
                    .build();

                // Execute the analysis
                String response = openAiService.createChatCompletion(request)
                    .getChoices().get(0).getMessage().getContent();
                
                // Parse the response and build result
                result = parseAnalysisResponse(response, sbomDocument, parameters);
                result.setAnalysisDurationMs(System.currentTimeMillis() - startTime);
                result.setStatus(AnalysisStatus.COMPLETED);
                
                logger.info("AI analysis completed successfully for document: {}", sbomDocument.getDocumentName());
                
            } catch (Exception e) {
                logger.error("AI analysis failed for document: {}", sbomDocument.getDocumentName(), e);
                result.setStatus(AnalysisStatus.FAILED);
                result.setErrorMessage("AI analysis failed: " + e.getMessage());
            }
            
            return result;
        }, analysisExecutor);
    }

    @Override
    public String[] getAvailableModels() {
        return new String[]{"gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"};
    }

    @Override
    public boolean isAvailable() {
        return enabled && openAiService != null;
    }

    @Override
    public AnalyzerInfo getAnalyzerInfo() {
        return new AnalyzerInfo(
            "OpenAI GPT Analyzer",
            "1.0.0",
            getAvailableModels(),
            isAvailable(),
            "OpenAI"
        );
    }

    @Override
    public CostEstimate estimateCost(SbomDocument sbomDocument) {
        // Rough cost estimation based on token count
        int estimatedTokens = estimateTokenCount(sbomDocument);
        double costPer1kTokens = 0.03; // Approximate cost for GPT-4
        double estimatedCost = (estimatedTokens / 1000.0) * costPer1kTokens;
        
        return new CostEstimate(estimatedCost, "USD", defaultModel, estimatedTokens, "Token-based estimation");
    }

    /**
     * Builds the analysis prompt for the AI model.
     */
    private String buildAnalysisPrompt(SbomDocument sbomDocument, AnalysisParameters parameters) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("Please analyze the following SBOM (Software Bill of Materials) for security risks and provide insights:\n\n");
        
        // Add SBOM metadata
        prompt.append("Document Information:\n");
        prompt.append("- Name: ").append(sbomDocument.getDocumentName()).append("\n");
        prompt.append("- Version: ").append(sbomDocument.getDocumentVersion()).append("\n");
        prompt.append("- Format: ").append(sbomDocument.getSbomFormat()).append("\n");
        prompt.append("- Created: ").append(sbomDocument.getCreatedDate()).append("\n\n");
        
        // Add components information
        prompt.append("Components (").append(sbomDocument.getComponents().size()).append(" total):\n");
        sbomDocument.getComponents().forEach(component -> {
            prompt.append("- ").append(component.getName())
                  .append(" ").append(component.getVersion())
                  .append(" (").append(component.getGroupId() != null ? component.getGroupId() : "library").append(")\n");
        });
        
        prompt.append("\nPlease provide:\n");
        prompt.append("1. Overall risk assessment (LOW, MEDIUM, HIGH, CRITICAL)\n");
        prompt.append("2. Risk score (0-10)\n");
        prompt.append("3. Key security findings\n");
        prompt.append("4. Specific recommendations\n");
        prompt.append("5. Confidence level in your assessment (0-1)\n");
        
        if (parameters.isIncludeRecommendations()) {
            prompt.append("6. Detailed remediation steps\n");
        }
        
        return prompt.toString();
    }

    /**
     * Gets the system prompt for the AI model.
     */
    private String getSystemPrompt() {
        return "You are an expert cybersecurity analyst specializing in Software Bill of Materials (SBOM) analysis. " +
               "Your role is to assess security risks in software components and provide actionable recommendations. " +
               "Always provide structured, professional analysis with clear risk levels and specific recommendations. " +
               "Focus on identifying potential vulnerabilities, outdated components, and security best practices.";
    }

    /**
     * Parses the AI model response into an AiAnalysisResult.
     */
    private AiAnalysisResult parseAnalysisResponse(String response, SbomDocument sbomDocument, AnalysisParameters parameters) {
        AiAnalysisResult result = new AiAnalysisResult();
        result.setSbomDocument(sbomDocument);
        result.setModelUsed(parameters.getModel());
        result.setModelVersion("1.0.0");
        
        try {
            // Extract risk level
            if (response.toLowerCase().contains("critical")) {
                result.setRiskLevel(RiskLevel.CRITICAL);
                result.setRiskScore(9.0);
            } else if (response.toLowerCase().contains("high")) {
                result.setRiskLevel(RiskLevel.HIGH);
                result.setRiskScore(7.0);
            } else if (response.toLowerCase().contains("medium")) {
                result.setRiskLevel(RiskLevel.MEDIUM);
                result.setRiskScore(5.0);
            } else {
                result.setRiskLevel(RiskLevel.LOW);
                result.setRiskScore(2.0);
            }
            
            // Extract confidence score (look for patterns like "confidence: 0.8" or "confidence level: 0.8")
            String confidencePattern = "confidence.*?(\\d+\\.\\d+)";
            java.util.regex.Pattern pattern = java.util.regex.Pattern.compile(confidencePattern, java.util.regex.Pattern.CASE_INSENSITIVE);
            java.util.regex.Matcher matcher = pattern.matcher(response);
            if (matcher.find()) {
                result.setConfidenceScore(Double.parseDouble(matcher.group(1)));
            } else {
                result.setConfidenceScore(0.7); // Default confidence
            }
            
            // Set analysis content
            result.setAnalysisSummary(extractSection(response, "summary", "analysis"));
            result.setKeyFindings(extractSection(response, "findings", "key"));
            result.setRecommendations(extractSection(response, "recommendations", "remediation"));
            
        } catch (Exception e) {
            logger.warn("Failed to parse AI response, using fallback parsing", e);
            // Fallback: use the entire response as analysis summary
            result.setAnalysisSummary(response);
            result.setRiskLevel(RiskLevel.MEDIUM);
            result.setRiskScore(5.0);
            result.setConfidenceScore(0.5);
        }
        
        return result;
    }

    /**
     * Extracts a specific section from the AI response.
     */
    private String extractSection(String response, String... keywords) {
        String[] lines = response.split("\n");
        StringBuilder section = new StringBuilder();
        boolean inSection = false;
        
        for (String line : lines) {
            String lowerLine = line.toLowerCase();
            if (java.util.Arrays.stream(keywords).anyMatch(keyword -> lowerLine.contains(keyword.toLowerCase()))) {
                inSection = true;
                continue;
            }
            
            if (inSection) {
                if (line.trim().isEmpty() || line.matches("^\\d+\\..*")) {
                    break;
                }
                section.append(line).append("\n");
            }
        }
        
        return section.toString().trim();
    }

    /**
     * Estimates the token count for the SBOM document.
     */
    private int estimateTokenCount(SbomDocument sbomDocument) {
        // Rough estimation: 1 token ≈ 4 characters
        int totalChars = sbomDocument.getDocumentName().length() +
                        sbomDocument.getDocumentVersion().length() +
                        sbomDocument.getSbomFormat().toString().length();
        
        for (var component : sbomDocument.getComponents()) {
            totalChars += component.getName().length() +
                         component.getVersion().length() +
                         (component.getGroupId() != null ? component.getGroupId().length() : "library".length());
        }
        
        return totalChars / 4;
    }

    /**
     * Gets default analysis parameters.
     */
    private AnalysisParameters getDefaultParameters() {
        return new AnalysisParameters.Builder()
            .model(defaultModel)
            .maxTokens(defaultMaxTokens)
            .temperature(defaultTemperature)
            .confidenceThreshold(0.7)
            .includeRecommendations(true)
            .build();
    }


} 