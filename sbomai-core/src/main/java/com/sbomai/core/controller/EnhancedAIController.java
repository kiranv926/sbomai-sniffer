package com.sbomai.core.controller;

import com.sbomai.core.dto.AIAnalysisDto;
import com.sbomai.core.dto.AIRecommendationDto;
import com.sbomai.core.service.AIOrchestrationService;
import com.sbomai.core.service.AIService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

@RestController
@RequestMapping("/ai/enhanced")
@CrossOrigin(origins = "*")
@Tag(name = "Enhanced AI Analysis", description = "Advanced AI-powered SBOM analysis and recommendations")
@SecurityRequirement(name = "apiKey")
@SecurityRequirement(name = "bearerAuth")
public class EnhancedAIController {
    
    private static final Logger logger = LoggerFactory.getLogger(EnhancedAIController.class);
    
    @Autowired
    private AIService aiService;
    
    @Autowired
    private AIOrchestrationService aiOrchestrationService;
    
    /**
     * POST /api/v1/ai/enhanced/comprehensive-analysis - Perform comprehensive AI analysis
     */
    @PostMapping("/comprehensive-analysis")
    @Operation(
        summary = "Perform Comprehensive AI Analysis",
        description = "Initiates a comprehensive AI analysis of an SBOM document, including vulnerability assessment, " +
                     "risk scoring, compliance checking, and supply chain analysis. This is an asynchronous operation " +
                     "that returns a CompletableFuture for tracking progress.",
        responses = {
            @ApiResponse(
                responseCode = "202",
                description = "Analysis initiated successfully",
                content = @Content(schema = @Schema(implementation = AIAnalysisDto.class))
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid SBOM document ID"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error during analysis initiation"
            )
        }
    )
    public ResponseEntity<CompletableFuture<AIAnalysisDto>> performComprehensiveAnalysis(
            @Parameter(description = "UUID of the SBOM document to analyze", required = true)
            @RequestParam UUID sbomDocumentId) {
        try {
            logger.info("Comprehensive AI analysis requested for SBOM document: {}", sbomDocumentId);
            
            CompletableFuture<AIAnalysisDto> future = aiOrchestrationService.performComprehensiveAnalysis(sbomDocumentId);
            
            return ResponseEntity.accepted().body(future);
            
        } catch (Exception e) {
            logger.error("Error initiating comprehensive AI analysis: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * POST /api/v1/ai/enhanced/targeted-analysis - Perform targeted AI analysis
     */
    @PostMapping("/targeted-analysis")
    @Operation(
        summary = "Perform Targeted AI Analysis",
        description = "Performs a targeted AI analysis on an SBOM document based on the specified analysis type. " +
                     "Supported types include: VULNERABILITY, COMPLIANCE, SUPPLY_CHAIN, PERFORMANCE, SECURITY.",
        responses = {
            @ApiResponse(
                responseCode = "202",
                description = "Targeted analysis initiated successfully",
                content = @Content(schema = @Schema(implementation = AIAnalysisDto.class))
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid analysis type or SBOM document ID"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error during analysis"
            )
        }
    )
    public ResponseEntity<CompletableFuture<AIAnalysisDto>> performTargetedAnalysis(
            @Parameter(description = "UUID of the SBOM document to analyze", required = true)
            @RequestParam UUID sbomDocumentId,
            @Parameter(description = "Type of analysis to perform (VULNERABILITY, COMPLIANCE, SUPPLY_CHAIN, PERFORMANCE, SECURITY)", required = true)
            @RequestParam String analysisType) {
        try {
            logger.info("Targeted AI analysis requested for SBOM document: {} with type: {}", sbomDocumentId, analysisType);
            
            CompletableFuture<AIAnalysisDto> future = aiOrchestrationService.performTargetedAnalysis(sbomDocumentId, analysisType);
            
            return ResponseEntity.accepted().body(future);
            
        } catch (Exception e) {
            logger.error("Error initiating targeted AI analysis: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/recommendations/project/{projectId} - Get AI recommendations for project
     */
    @GetMapping("/recommendations/project/{projectId}")
    @Operation(
        summary = "Get AI Recommendations for Project",
        description = "Retrieves AI-generated recommendations for a specific project, including security improvements, " +
                     "dependency updates, compliance fixes, and performance optimizations.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Recommendations retrieved successfully",
                content = @Content(schema = @Schema(implementation = AIRecommendationDto.class))
            ),
            @ApiResponse(
                responseCode = "404",
                description = "Project not found"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<List<AIRecommendationDto>> getProjectRecommendations(
            @Parameter(description = "UUID of the project", required = true)
            @PathVariable UUID projectId) {
        try {
            logger.info("AI recommendations requested for project: {}", projectId);
            
            List<AIRecommendationDto> recommendations = aiOrchestrationService.generateProjectRecommendations(projectId);
            
            return ResponseEntity.ok(recommendations);
            
        } catch (Exception e) {
            logger.error("Error generating project recommendations: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/recommendations/portfolio - Get AI recommendations for portfolio
     */
    @GetMapping("/recommendations/portfolio")
    @Operation(
        summary = "Get AI Portfolio Recommendations",
        description = "Retrieves AI-generated recommendations for the entire portfolio, including cross-project " +
                     "security improvements, standardization opportunities, and strategic recommendations.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Portfolio recommendations retrieved successfully",
                content = @Content(schema = @Schema(implementation = AIRecommendationDto.class))
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<List<AIRecommendationDto>> getPortfolioRecommendations() {
        try {
            logger.info("AI portfolio recommendations requested");
            
            List<AIRecommendationDto> recommendations = aiOrchestrationService.generatePortfolioRecommendations();
            
            return ResponseEntity.ok(recommendations);
            
        } catch (Exception e) {
            logger.error("Error generating portfolio recommendations: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/recommendations/vulnerability/{vulnerabilityId} - Get AI recommendations for vulnerability
     */
    @GetMapping("/recommendations/vulnerability/{vulnerabilityId}")
    @Operation(
        summary = "Get AI Recommendations for Vulnerability",
        description = "Retrieves AI-generated recommendations for addressing a specific vulnerability, including " +
                     "patch suggestions, workarounds, and mitigation strategies.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Vulnerability recommendations retrieved successfully",
                content = @Content(schema = @Schema(implementation = AIRecommendationDto.class))
            ),
            @ApiResponse(
                responseCode = "404",
                description = "Vulnerability not found"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<List<AIRecommendationDto>> getVulnerabilityRecommendations(
            @Parameter(description = "UUID of the vulnerability", required = true)
            @PathVariable UUID vulnerabilityId) {
        try {
            logger.info("AI vulnerability recommendations requested: {}", vulnerabilityId);
            
            List<AIRecommendationDto> recommendations = aiOrchestrationService.generateVulnerabilityRecommendations(vulnerabilityId);
            
            return ResponseEntity.ok(recommendations);
            
        } catch (Exception e) {
            logger.error("Error generating vulnerability recommendations: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/model-health - Get AI model health
     */
    @GetMapping("/model-health")
    @Operation(
        summary = "Get AI Model Health",
        description = "Retrieves the health status of AI models, including availability, performance metrics, " +
                     "and operational status.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Model health status retrieved successfully",
                content = @Content(schema = @Schema(implementation = AIService.ModelStatus.class))
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<AIService.ModelStatus> getModelHealth() {
        try {
            logger.info("AI model health requested");
            
            AIService.ModelStatus status = aiService.getModelStatus();
            
            return ResponseEntity.ok(status);
            
        } catch (Exception e) {
            logger.error("Error retrieving model health: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/model-performance/{modelType} - Get AI model performance
     */
    @GetMapping("/model-performance/{modelType}")
    @Operation(
        summary = "Get AI Model Performance",
        description = "Retrieves performance metrics for a specific AI model type, including accuracy, precision, " +
                     "recall, and F1 scores.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Model performance retrieved successfully",
                content = @Content(schema = @Schema(implementation = AIService.ModelPerformance.class))
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid model type"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<AIService.ModelPerformance> getModelPerformance(
            @Parameter(description = "Type of AI model (VULNERABILITY, COMPLIANCE, SUPPLY_CHAIN, etc.)", required = true)
            @PathVariable String modelType) {
        try {
            logger.info("AI model performance requested for type: {}", modelType);
            
            AIService.ModelPerformance performance = aiService.getModelPerformance(modelType);
            
            return ResponseEntity.ok(performance);
            
        } catch (Exception e) {
            logger.error("Error retrieving model performance: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * POST /api/v1/ai/enhanced/model-config - Update AI model configuration
     */
    @PostMapping("/model-config")
    @Operation(
        summary = "Update AI Model Configuration",
        description = "Updates the configuration for a specific AI model type, including parameters, thresholds, " +
                     "and operational settings.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Model configuration updated successfully"
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid configuration parameters"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<Void> updateModelConfiguration(
            @Parameter(description = "Type of AI model to configure", required = true)
            @RequestParam String modelType,
            @Parameter(description = "JSON configuration string", required = true)
            @RequestParam String configuration) {
        try {
            logger.info("AI model configuration update requested for type: {}", modelType);
            
            aiService.updateModelConfiguration(modelType, configuration);
            
            return ResponseEntity.ok().build();
            
        } catch (Exception e) {
            logger.error("Error updating model configuration: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * POST /api/v1/ai/enhanced/model-retrain - Retrain AI model
     */
    @PostMapping("/model-retrain")
    @Operation(
        summary = "Retrain AI Model",
        description = "Initiates retraining of a specific AI model type with updated data and parameters. " +
                     "This is an asynchronous operation.",
        responses = {
            @ApiResponse(
                responseCode = "202",
                description = "Model retraining initiated successfully"
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid model type"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<Void> retrainModel(
            @Parameter(description = "Type of AI model to retrain", required = true)
            @RequestParam String modelType) {
        try {
            logger.info("AI model retraining requested for type: {}", modelType);
            
            aiService.retrainModel(modelType);
            
            return ResponseEntity.accepted().build();
            
        } catch (Exception e) {
            logger.error("Error initiating model retraining: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/dashboard-insights - Get dashboard insights
     */
    @GetMapping("/dashboard-insights")
    @Operation(
        summary = "Get Dashboard Insights",
        description = "Retrieves comprehensive dashboard insights including security metrics, trend analysis, " +
                     "risk assessments, and AI-powered recommendations for the entire portfolio.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Dashboard insights retrieved successfully",
                content = @Content(schema = @Schema(implementation = AIService.DashboardInsights.class))
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<AIService.DashboardInsights> getDashboardInsights() {
        try {
            logger.info("Dashboard insights requested");
            
            AIService.DashboardInsights insights = aiService.getDashboardInsights();
            
            return ResponseEntity.ok(insights);
            
        } catch (Exception e) {
            logger.error("Error retrieving dashboard insights: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/risk-assessment/{projectId} - Get risk assessment
     */
    @GetMapping("/risk-assessment/{projectId}")
    @Operation(
        summary = "Get Risk Assessment",
        description = "Retrieves comprehensive risk assessment for a specific project, including risk factors, " +
                     "mitigation strategies, and confidence scores.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Risk assessment retrieved successfully",
                content = @Content(schema = @Schema(implementation = AIService.RiskAssessment.class))
            ),
            @ApiResponse(
                responseCode = "404",
                description = "Project not found"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<AIService.RiskAssessment> getRiskAssessment(
            @Parameter(description = "UUID of the project", required = true)
            @PathVariable UUID projectId) {
        try {
            logger.info("Risk assessment requested for project: {}", projectId);
            
            AIService.RiskAssessment assessment = aiService.getRiskAssessment(projectId);
            
            return ResponseEntity.ok(assessment);
            
        } catch (Exception e) {
            logger.error("Error retrieving risk assessment: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/trend-analysis - Get trend analysis
     */
    @GetMapping("/trend-analysis")
    @Operation(
        summary = "Get Trend Analysis",
        description = "Retrieves AI-powered trend analysis for the specified time period, including vulnerability " +
                     "trends, security posture changes, and predictive insights.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Trend analysis retrieved successfully",
                content = @Content(schema = @Schema(implementation = AIService.TrendAnalysis.class))
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid time period"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<AIService.TrendAnalysis> getTrendAnalysis(
            @Parameter(description = "Number of days for trend analysis (default: 30)", required = false)
            @RequestParam(defaultValue = "30") int days) {
        try {
            logger.info("Trend analysis requested for {} days", days);
            
            AIService.TrendAnalysis analysis = aiService.getTrendAnalysis(days);
            
            return ResponseEntity.ok(analysis);
            
        } catch (Exception e) {
            logger.error("Error retrieving trend analysis: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/security-insights - Get security insights
     */
    @GetMapping("/security-insights")
    @Operation(
        summary = "Get Security Insights",
        description = "Retrieves detailed security insights including vulnerability analysis, threat intelligence, " +
                     "compliance status, and security posture assessment.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Security insights retrieved successfully",
                content = @Content(schema = @Schema(implementation = AIService.SecurityInsights.class))
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<AIService.SecurityInsights> getSecurityInsights() {
        try {
            logger.info("Security insights requested");
            
            AIService.SecurityInsights insights = aiService.getSecurityInsights();
            
            return ResponseEntity.ok(insights);
            
        } catch (Exception e) {
            logger.error("Error retrieving security insights: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/analysis/{analysisId} - Get AI analysis by ID
     */
    @GetMapping("/analysis/{analysisId}")
    public ResponseEntity<AIAnalysisDto> getAIAnalysis(@PathVariable UUID analysisId) {
        try {
            logger.info("AI analysis requested for ID: {}", analysisId);
            
            AIAnalysisDto analysis = aiService.getAIAnalysis(analysisId);
            
            return ResponseEntity.ok(analysis);
            
        } catch (Exception e) {
            logger.error("Error retrieving AI analysis: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/analysis/sbom/{sbomDocumentId} - Get AI analysis by SBOM document ID
     */
    @GetMapping("/analysis/sbom/{sbomDocumentId}")
    public ResponseEntity<AIAnalysisDto> getAIAnalysisBySbomDocument(@PathVariable UUID sbomDocumentId) {
        try {
            logger.info("AI analysis requested for SBOM document: {}", sbomDocumentId);
            
            AIAnalysisDto analysis = aiService.getAIAnalysisBySbomDocument(sbomDocumentId);
            
            return ResponseEntity.ok(analysis);
            
        } catch (Exception e) {
            logger.error("Error retrieving AI analysis for SBOM document: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * POST /api/v1/ai/enhanced/analyze-sbom - Analyze SBOM with AI (synchronous)
     */
    @PostMapping("/analyze-sbom")
    public ResponseEntity<AIAnalysisDto> analyzeSbom(
            @RequestParam UUID sbomDocumentId,
            @RequestParam(required = false, defaultValue = "VULNERABILITY") String analysisType) {
        try {
            logger.info("Synchronous AI analysis requested for SBOM document: {} with type: {}", sbomDocumentId, analysisType);
            
            AIAnalysisDto analysis = aiService.analyzeSbom(sbomDocumentId, analysisType);
            
            return ResponseEntity.ok(analysis);
            
        } catch (Exception e) {
            logger.error("Error performing AI analysis: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/ai/enhanced/model-status - Get AI model status
     */
    @GetMapping("/model-status")
    public ResponseEntity<AIService.ModelStatus> getModelStatus() {
        try {
            logger.info("AI model status requested");
            
            AIService.ModelStatus status = aiService.getModelStatus();
            
            return ResponseEntity.ok(status);
            
        } catch (Exception e) {
            logger.error("Error retrieving AI model status: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
} 