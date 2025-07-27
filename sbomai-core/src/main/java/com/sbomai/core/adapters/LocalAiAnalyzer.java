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
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;

/**
 * Local AI analyzer implementation that provides basic risk assessment
 * without requiring external AI services.
 * 
 * This analyzer uses rule-based heuristics and pattern matching to
 * provide basic security insights for SBOM documents.
 */
@Service
public class LocalAiAnalyzer implements AiAnalyzer {

    private static final Logger logger = LoggerFactory.getLogger(LocalAiAnalyzer.class);
    
    private final Executor analysisExecutor;
    
    @Value("${sbomai.core.ai.local.enabled:false}")
    private boolean enabled;

    public LocalAiAnalyzer(Executor analysisExecutor) {
        this.analysisExecutor = analysisExecutor;
    }

    @Override
    public CompletableFuture<AiAnalysisResult> analyze(SbomDocument sbomDocument) throws AiAnalysisException {
        return analyze(sbomDocument, getDefaultParameters());
    }

    @Override
    public CompletableFuture<AiAnalysisResult> analyze(SbomDocument sbomDocument, AnalysisParameters parameters) throws AiAnalysisException {
        if (!isAvailable()) {
            throw new AiAnalysisException("Local AI analyzer is not available");
        }

        return CompletableFuture.supplyAsync(() -> {
            long startTime = System.currentTimeMillis();
            AiAnalysisResult result = new AiAnalysisResult();
            result.setStatus(AnalysisStatus.PENDING);
            
            try {
                logger.info("Starting local AI analysis for SBOM document: {}", sbomDocument.getDocumentName());
                
                // Perform rule-based analysis
                result = performRuleBasedAnalysis(sbomDocument, parameters);
                result.setAnalysisDurationMs(System.currentTimeMillis() - startTime);
                result.setStatus(AnalysisStatus.COMPLETED);
                
                logger.info("Local AI analysis completed successfully for document: {}", sbomDocument.getDocumentName());
                
            } catch (Exception e) {
                logger.error("Local AI analysis failed for document: {}", sbomDocument.getDocumentName(), e);
                result.setStatus(AnalysisStatus.FAILED);
                result.setErrorMessage("Local AI analysis failed: " + e.getMessage());
            }
            
            return result;
        }, analysisExecutor);
    }

    @Override
    public String[] getAvailableModels() {
        return new String[]{"local-rules", "local-heuristics"};
    }

    @Override
    public boolean isAvailable() {
        return enabled;
    }

    @Override
    public AnalyzerInfo getAnalyzerInfo() {
        return new AnalyzerInfo(
            "Local Rule-Based Analyzer",
            "1.0.0",
            getAvailableModels(),
            isAvailable(),
            "Local"
        );
    }

    @Override
    public CostEstimate estimateCost(SbomDocument sbomDocument) {
        // Local analysis is free
        return new CostEstimate(0.0, "USD", "local-rules", 0, "Free local analysis");
    }

    /**
     * Performs rule-based analysis on the SBOM document.
     */
    private AiAnalysisResult performRuleBasedAnalysis(SbomDocument sbomDocument, AnalysisParameters parameters) {
        AiAnalysisResult result = new AiAnalysisResult();
        result.setSbomDocument(sbomDocument);
        result.setModelUsed(parameters.getModel());
        result.setModelVersion("1.0.0");
        
        // Initialize counters
        int totalComponents = sbomDocument.getComponents().size();
        int outdatedComponents = 0;
        int suspiciousComponents = 0;
        int highRiskComponents = 0;
        
        StringBuilder findings = new StringBuilder();
        StringBuilder recommendations = new StringBuilder();
        
        // Analyze each component
        for (var component : sbomDocument.getComponents()) {
            ComponentRisk componentRisk = analyzeComponent(component);
            
            if (componentRisk.isOutdated()) {
                outdatedComponents++;
            }
            if (componentRisk.isSuspicious()) {
                suspiciousComponents++;
            }
            if (componentRisk.getRiskLevel() == RiskLevel.HIGH || componentRisk.getRiskLevel() == RiskLevel.CRITICAL) {
                highRiskComponents++;
            }
            
            // Add findings for high-risk components
            if (componentRisk.getRiskLevel() == RiskLevel.HIGH || componentRisk.getRiskLevel() == RiskLevel.CRITICAL) {
                findings.append("- ").append(component.getName()).append(" ").append(component.getVersion())
                        .append(": ").append(componentRisk.getReason()).append("\n");
            }
        }
        
        // Calculate overall risk score
        double riskScore = calculateRiskScore(totalComponents, outdatedComponents, suspiciousComponents, highRiskComponents);
        RiskLevel overallRiskLevel = determineRiskLevel(riskScore);
        
        // Set analysis results
        result.setRiskScore(riskScore);
        result.setRiskLevel(overallRiskLevel);
        result.setConfidenceScore(0.6); // Lower confidence for rule-based analysis
        
        // Build analysis summary
        StringBuilder summary = new StringBuilder();
        summary.append("Local rule-based analysis of ").append(totalComponents).append(" components.\n");
        summary.append("Found ").append(outdatedComponents).append(" potentially outdated components.\n");
        summary.append("Identified ").append(suspiciousComponents).append(" suspicious components.\n");
        summary.append("Detected ").append(highRiskComponents).append(" high-risk components.\n");
        summary.append("Overall risk level: ").append(overallRiskLevel);
        
        result.setAnalysisSummary(summary.toString());
        result.setKeyFindings(findings.toString());
        
        // Build recommendations
        if (outdatedComponents > 0) {
            recommendations.append("- Update ").append(outdatedComponents).append(" outdated components\n");
        }
        if (suspiciousComponents > 0) {
            recommendations.append("- Review ").append(suspiciousComponents).append(" suspicious components\n");
        }
        if (highRiskComponents > 0) {
            recommendations.append("- Prioritize remediation of ").append(highRiskComponents).append(" high-risk components\n");
        }
        recommendations.append("- Consider using a more comprehensive AI analysis for detailed insights\n");
        
        result.setRecommendations(recommendations.toString());
        
        return result;
    }

    /**
     * Analyzes a single component for risks.
     */
    private ComponentRisk analyzeComponent(com.sbomai.core.domain.SbomComponent component) {
        ComponentRisk risk = new ComponentRisk();
        
        // Check for outdated versions (basic heuristics)
        if (isOutdatedVersion(component.getVersion())) {
            risk.setOutdated(true);
            risk.setReason("Potentially outdated version");
        }
        
        // Check for suspicious patterns
        if (isSuspiciousComponent(component)) {
            risk.setSuspicious(true);
            risk.setReason("Suspicious component characteristics");
        }
        
        // Determine risk level
        if (risk.isOutdated() && risk.isSuspicious()) {
            risk.setRiskLevel(RiskLevel.HIGH);
        } else if (risk.isOutdated() || risk.isSuspicious()) {
            risk.setRiskLevel(RiskLevel.MEDIUM);
        } else {
            risk.setRiskLevel(RiskLevel.LOW);
        }
        
        return risk;
    }

    /**
     * Checks if a version appears to be outdated.
     */
    private boolean isOutdatedVersion(String version) {
        if (version == null || version.trim().isEmpty()) {
            return false;
        }
        
        // Basic heuristics for outdated versions
        String lowerVersion = version.toLowerCase();
        
        // Check for very old version patterns
        if (lowerVersion.contains("alpha") || lowerVersion.contains("beta") || lowerVersion.contains("rc")) {
            return true;
        }
        
        // Check for version numbers that might be old
        if (lowerVersion.matches(".*\\b(0\\.|1\\.|2\\.).*")) {
            // This is a very basic heuristic - in practice, you'd want more sophisticated version comparison
            return Math.random() < 0.3; // 30% chance for demo purposes
        }
        
        return false;
    }

    /**
     * Checks if a component appears suspicious.
     */
    private boolean isSuspiciousComponent(com.sbomai.core.domain.SbomComponent component) {
        if (component.getName() == null) {
            return false;
        }
        
        String name = component.getName().toLowerCase();
        
        // Check for suspicious patterns
        if (name.contains("test") || name.contains("example") || name.contains("demo")) {
            return true;
        }
        
        // Check for components without proper metadata
        if (component.getDescription() == null || component.getDescription().trim().isEmpty()) {
            return Math.random() < 0.2; // 20% chance for demo purposes
        }
        
        return false;
    }

    /**
     * Calculates overall risk score.
     */
    private double calculateRiskScore(int total, int outdated, int suspicious, int highRisk) {
        if (total == 0) {
            return 0.0;
        }
        
        double outdatedRatio = (double) outdated / total;
        double suspiciousRatio = (double) suspicious / total;
        double highRiskRatio = (double) highRisk / total;
        
        // Weighted risk calculation
        double riskScore = (outdatedRatio * 3.0) + (suspiciousRatio * 5.0) + (highRiskRatio * 8.0);
        
        return Math.min(riskScore, 10.0); // Cap at 10
    }

    /**
     * Determines risk level based on score.
     */
    private RiskLevel determineRiskLevel(double riskScore) {
        if (riskScore >= 7.0) {
            return RiskLevel.CRITICAL;
        } else if (riskScore >= 5.0) {
            return RiskLevel.HIGH;
        } else if (riskScore >= 3.0) {
            return RiskLevel.MEDIUM;
        } else {
            return RiskLevel.LOW;
        }
    }

    /**
     * Gets default analysis parameters.
     */
    private AnalysisParameters getDefaultParameters() {
        return new AnalysisParameters.Builder()
            .model("local-rules")
            .maxTokens(1000)
            .temperature(0.1)
            .confidenceThreshold(0.6)
            .includeRecommendations(true)
            .build();
    }

    /**
     * Internal class for component risk assessment.
     */
    private static class ComponentRisk {
        private boolean outdated = false;
        private boolean suspicious = false;
        private RiskLevel riskLevel = RiskLevel.LOW;
        private String reason = "";

        public boolean isOutdated() { return outdated; }
        public void setOutdated(boolean outdated) { this.outdated = outdated; }

        public boolean isSuspicious() { return suspicious; }
        public void setSuspicious(boolean suspicious) { this.suspicious = suspicious; }

        public RiskLevel getRiskLevel() { return riskLevel; }
        public void setRiskLevel(RiskLevel riskLevel) { this.riskLevel = riskLevel; }

        public String getReason() { return reason; }
        public void setReason(String reason) { this.reason = reason; }
    }
} 