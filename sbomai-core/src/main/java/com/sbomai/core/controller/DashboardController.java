package com.sbomai.core.controller;

import com.sbomai.core.service.DashboardService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Dashboard Controller
 * Provides comprehensive dashboard data and metrics for the SBOMAI application
 */
@RestController
@RequestMapping("/dashboard")
@CrossOrigin(origins = "*")
@Tag(name = "Dashboard", description = "Dashboard data and metrics APIs for overview, trends, and insights")
@SecurityRequirement(name = "apiKey")
@SecurityRequirement(name = "bearerAuth")
public class DashboardController {
    
    private static final Logger logger = LoggerFactory.getLogger(DashboardController.class);
    
    @Autowired
    private DashboardService dashboardService;
    
    /**
     * GET /api/v1/dashboard/summary - Get dashboard summary
     */
    @GetMapping("/summary")
    @Operation(
        summary = "Get Dashboard Summary",
        description = "Retrieves a comprehensive summary of dashboard metrics including total SBOMs, vulnerabilities, " +
                     "policy violations, AI suggestions, and project statistics for the specified time period.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Dashboard summary retrieved successfully",
                content = @Content(schema = @Schema(implementation = DashboardService.DashboardSummary.class))
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid time period parameter"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<DashboardService.DashboardSummary> getDashboardSummary(
            @Parameter(description = "Number of days for summary data (default: 30)", required = false)
            @RequestParam(defaultValue = "30") int days) {
        try {
            logger.info("Dashboard summary requested for {} days", days);
            
            DashboardService.DashboardSummary summary = dashboardService.getDashboardSummary(days);
            
            return ResponseEntity.ok(summary);
            
        } catch (Exception e) {
            logger.error("Error retrieving dashboard summary: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/dashboard/trends - Get dashboard trends
     */
    @GetMapping("/trends")
    @Operation(
        summary = "Get Dashboard Trends",
        description = "Retrieves trend data for vulnerabilities over the specified time period, including critical, " +
                     "high, medium, low severity counts and AI-predicted values.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Trend data retrieved successfully",
                content = @Content(schema = @Schema(implementation = DashboardService.TrendData.class))
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid time period parameter"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<List<DashboardService.TrendData>> getDashboardTrends(
            @Parameter(description = "Number of days for trend analysis (default: 30)", required = false)
            @RequestParam(defaultValue = "30") int days) {
        try {
            logger.info("Dashboard trends requested for {} days", days);
            
            List<DashboardService.TrendData> trends = dashboardService.getDashboardTrends(days);
            
            return ResponseEntity.ok(trends);
            
        } catch (Exception e) {
            logger.error("Error retrieving dashboard trends: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/dashboard/project-coverage - Get project coverage
     */
    @GetMapping("/project-coverage")
    @Operation(
        summary = "Get Project Coverage",
        description = "Retrieves SBOM coverage data for all projects, including coverage percentage, outdated " +
                     "packages count, and risk scores.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Project coverage data retrieved successfully",
                content = @Content(schema = @Schema(implementation = DashboardService.ProjectCoverage.class))
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<List<DashboardService.ProjectCoverage>> getProjectCoverage() {
        try {
            logger.info("Project coverage data requested");
            
            List<DashboardService.ProjectCoverage> coverage = dashboardService.getProjectCoverage();
            
            return ResponseEntity.ok(coverage);
            
        } catch (Exception e) {
            logger.error("Error retrieving project coverage: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/dashboard/at-risk-repos - Get at-risk repositories
     */
    @GetMapping("/at-risk-repos")
    @Operation(
        summary = "Get At-Risk Repositories",
        description = "Retrieves a list of repositories identified as at-risk based on risk scores, critical " +
                     "vulnerabilities, and AI analysis notes.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "At-risk repositories retrieved successfully",
                content = @Content(schema = @Schema(implementation = DashboardService.AtRiskRepo.class))
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<List<DashboardService.AtRiskRepo>> getAtRiskRepos() {
        try {
            logger.info("At-risk repositories requested");
            
            List<DashboardService.AtRiskRepo> repos = dashboardService.getAtRiskRepos();
            
            return ResponseEntity.ok(repos);
            
        } catch (Exception e) {
            logger.error("Error retrieving at-risk repositories: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/dashboard/ai-recommendations - Get AI recommendations
     */
    @GetMapping("/ai-recommendations")
    @Operation(
        summary = "Get AI Recommendations",
        description = "Retrieves AI-generated recommendations for security improvements, dependency updates, " +
                     "and compliance fixes.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "AI recommendations retrieved successfully",
                content = @Content(schema = @Schema(implementation = DashboardService.AIRecommendation.class))
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<List<DashboardService.AIRecommendation>> getAIRecommendations() {
        try {
            logger.info("AI recommendations requested");
            
            List<DashboardService.AIRecommendation> recommendations = dashboardService.getAIRecommendations();
            
            return ResponseEntity.ok(recommendations);
            
        } catch (Exception e) {
            logger.error("Error retrieving AI recommendations: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/dashboard/security-metrics - Get security metrics
     */
    @GetMapping("/security-metrics")
    @Operation(
        summary = "Get Security Metrics",
        description = "Retrieves comprehensive security metrics including scan counts, vulnerability statistics, " +
                     "remediation progress, compliance scores, and threat intelligence data.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Security metrics retrieved successfully",
                content = @Content(schema = @Schema(implementation = DashboardService.SecurityMetrics.class))
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<DashboardService.SecurityMetrics> getSecurityMetrics() {
        try {
            logger.info("Security metrics requested");
            
            DashboardService.SecurityMetrics metrics = dashboardService.getSecurityMetrics();
            
            return ResponseEntity.ok(metrics);
            
        } catch (Exception e) {
            logger.error("Error retrieving security metrics: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/dashboard/recent-activity - Get recent activity
     */
    @GetMapping("/recent-activity")
    @Operation(
        summary = "Get Recent Activity",
        description = "Retrieves a list of recent activities including scans, analyses, alerts, and other " +
                     "system events, limited to the specified number of items.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Recent activity retrieved successfully",
                content = @Content(schema = @Schema(implementation = DashboardService.RecentActivity.class))
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid limit parameter"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<List<DashboardService.RecentActivity>> getRecentActivity(
            @Parameter(description = "Maximum number of activities to return (default: 10)", required = false)
            @RequestParam(defaultValue = "10") int limit) {
        try {
            logger.info("Recent activity requested with limit: {}", limit);
            
            List<DashboardService.RecentActivity> activities = dashboardService.getRecentActivity(limit);
            
            return ResponseEntity.ok(activities);
            
        } catch (Exception e) {
            logger.error("Error retrieving recent activity: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/dashboard/alerts - Get alerts
     */
    @GetMapping("/alerts")
    @Operation(
        summary = "Get Alerts",
        description = "Retrieves security alerts filtered by severity and limited to the specified number of items. " +
                     "Alerts include critical vulnerabilities, policy violations, and other security issues.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Alerts retrieved successfully",
                content = @Content(schema = @Schema(implementation = DashboardService.Alert.class))
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid parameters"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<List<DashboardService.Alert>> getAlerts(
            @Parameter(description = "Filter by severity (CRITICAL, HIGH, MEDIUM, LOW, or ALL for all severities)", required = false)
            @RequestParam(required = false, defaultValue = "ALL") String severity,
            @Parameter(description = "Maximum number of alerts to return (default: 20)", required = false)
            @RequestParam(defaultValue = "20") int limit) {
        try {
            logger.info("Alerts requested with severity: {} and limit: {}", severity, limit);
            
            List<DashboardService.Alert> alerts = dashboardService.getAlerts(severity, limit);
            
            return ResponseEntity.ok(alerts);
            
        } catch (Exception e) {
            logger.error("Error retrieving alerts: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/dashboard/compliance-status - Get compliance status
     */
    @GetMapping("/compliance-status")
    @Operation(
        summary = "Get Compliance Status",
        description = "Retrieves overall compliance status including compliance scores, compliant vs non-compliant " +
                     "projects, supported frameworks, and current violations.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Compliance status retrieved successfully",
                content = @Content(schema = @Schema(implementation = DashboardService.ComplianceStatus.class))
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<DashboardService.ComplianceStatus> getComplianceStatus() {
        try {
            logger.info("Compliance status requested");
            
            DashboardService.ComplianceStatus status = dashboardService.getComplianceStatus();
            
            return ResponseEntity.ok(status);
            
        } catch (Exception e) {
            logger.error("Error retrieving compliance status: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/dashboard/performance-metrics - Get performance metrics
     */
    @GetMapping("/performance-metrics")
    @Operation(
        summary = "Get Performance Metrics",
        description = "Retrieves system performance metrics including average scan times, analysis times, " +
                     "total operations completed, system uptime, and average response times.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Performance metrics retrieved successfully",
                content = @Content(schema = @Schema(implementation = DashboardService.PerformanceMetrics.class))
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<DashboardService.PerformanceMetrics> getPerformanceMetrics() {
        try {
            logger.info("Performance metrics requested");
            
            DashboardService.PerformanceMetrics metrics = dashboardService.getPerformanceMetrics();
            
            return ResponseEntity.ok(metrics);
            
        } catch (Exception e) {
            logger.error("Error retrieving performance metrics: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * GET /api/v1/dashboard/overview - Get complete dashboard overview
     * This endpoint combines multiple dashboard data sources for a single comprehensive response
     */
    @GetMapping("/overview")
    @Operation(
        summary = "Get Complete Dashboard Overview",
        description = "Retrieves a comprehensive dashboard overview combining summary, trends, coverage, " +
                     "security metrics, and recommendations in a single response. Useful for initial dashboard load.",
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Dashboard overview retrieved successfully"
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid time period parameter"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<DashboardOverview> getDashboardOverview(
            @Parameter(description = "Number of days for summary and trends (default: 30)", required = false)
            @RequestParam(defaultValue = "30") int days) {
        try {
            logger.info("Complete dashboard overview requested for {} days", days);
            
            DashboardOverview overview = new DashboardOverview(
                dashboardService.getDashboardSummary(days),
                dashboardService.getDashboardTrends(days),
                dashboardService.getProjectCoverage(),
                dashboardService.getAtRiskRepos(),
                dashboardService.getAIRecommendations(),
                dashboardService.getSecurityMetrics(),
                dashboardService.getRecentActivity(10),
                dashboardService.getAlerts("ALL", 20),
                dashboardService.getComplianceStatus(),
                dashboardService.getPerformanceMetrics()
            );
            
            return ResponseEntity.ok(overview);
            
        } catch (Exception e) {
            logger.error("Error retrieving dashboard overview: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * Complete dashboard overview data structure
     */
    public record DashboardOverview(
        DashboardService.DashboardSummary summary,
        List<DashboardService.TrendData> trends,
        List<DashboardService.ProjectCoverage> projectCoverage,
        List<DashboardService.AtRiskRepo> atRiskRepos,
        List<DashboardService.AIRecommendation> aiRecommendations,
        DashboardService.SecurityMetrics securityMetrics,
        List<DashboardService.RecentActivity> recentActivity,
        List<DashboardService.Alert> alerts,
        DashboardService.ComplianceStatus complianceStatus,
        DashboardService.PerformanceMetrics performanceMetrics
    ) {}
}

