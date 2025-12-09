package com.sbomai.core.service;

import java.util.List;

public interface DashboardService {
    
    DashboardSummary getDashboardSummary(int days);
    List<TrendData> getDashboardTrends(int days);
    List<ProjectCoverage> getProjectCoverage();
    List<AtRiskRepo> getAtRiskRepos();
    List<AIRecommendation> getAIRecommendations();
    SecurityMetrics getSecurityMetrics();
    List<RecentActivity> getRecentActivity(int limit);
    List<Alert> getAlerts(String severity, int limit);
    ComplianceStatus getComplianceStatus();
    PerformanceMetrics getPerformanceMetrics();
    
    record DashboardSummary(
        long totalSboms,
        long openVulnerabilities,
        long criticalVulnerabilities,
        long policyViolations,
        long aiSuggestions,
        double averageRiskScore,
        long totalProjects,
        long activeProjects
    ) {}
    
    record TrendData(
        String date,
        long critical,
        long high,
        long medium,
        long low,
        long predicted
    ) {}
    
    record ProjectCoverage(
        String name,
        double coverage,
        long outdatedPackages,
        double riskScore
    ) {}
    
    record AtRiskRepo(
        String name,
        double riskScore,
        long criticalVulns,
        String aiNote
    ) {}
    
    record AIRecommendation(
        String id,
        String title,
        String description,
        String impact,
        long affectedProjects
    ) {}
    
    record SecurityMetrics(
        long networkScans,
        long webScans,
        long directoryScans,
        long osDetections,
        long totalVulnerabilities,
        double remediationProgress,
        double complianceScore,
        long threatIntelligence
    ) {}
    
    record RecentActivity(
        String id,
        String type,
        String description,
        String timestamp,
        String severity,
        String projectName
    ) {}
    
    record Alert(
        String id,
        String title,
        String description,
        String severity,
        String timestamp,
        boolean acknowledged
    ) {}
    
    record ComplianceStatus(
        double overallScore,
        long compliantProjects,
        long nonCompliantProjects,
        List<String> complianceFrameworks,
        List<String> violations
    ) {}
    
    record PerformanceMetrics(
        double averageScanTime,
        double averageAnalysisTime,
        long totalScansCompleted,
        long totalAnalysesCompleted,
        double systemUptime,
        double responseTime
    ) {}
} 