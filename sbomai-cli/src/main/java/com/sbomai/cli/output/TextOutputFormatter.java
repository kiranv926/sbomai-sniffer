package com.sbomai.cli.output;

import com.sbomai.cli.commands.AnalysisResult;
import org.springframework.stereotype.Component;

/**
 * Text formatter for human-readable console output.
 */
@Component
public class TextOutputFormatter implements OutputFormatter {

    @Override
    public String format(AnalysisResult result) {
        StringBuilder sb = new StringBuilder();
        
        // Header
        sb.append("🔍 SBOMAI Analysis Results\n");
        sb.append("==========================\n\n");
        
        // SBOM Document Information
        if (result.getSbomDocument() != null) {
            sb.append("📄 SBOM Document Information:\n");
            sb.append("   Name: ").append(result.getSbomDocument().getDocumentName()).append("\n");
            sb.append("   Version: ").append(result.getSbomDocument().getDocumentVersion()).append("\n");
            sb.append("   Format: ").append(result.getSbomDocument().getSbomFormat()).append("\n");
            sb.append("   Components: ").append(result.getSbomDocument().getComponents().size()).append("\n");
            sb.append("   Created: ").append(result.getSbomDocument().getCreatedDate()).append("\n");
            sb.append("\n");
        }
        
        // Vulnerability Report
        if (result.getVulnerabilityReport() != null) {
            sb.append("🔒 Vulnerability Analysis:\n");
            sb.append("   Total Vulnerabilities: ").append(result.getVulnerabilityReport().getTotalVulnerabilities()).append("\n");
            
            if (result.getVulnerabilityReport().getCriticalCount() != null && result.getVulnerabilityReport().getCriticalCount() > 0) {
                sb.append("   ⚠️  Critical: ").append(result.getVulnerabilityReport().getCriticalCount()).append("\n");
            }
            if (result.getVulnerabilityReport().getHighCount() != null && result.getVulnerabilityReport().getHighCount() > 0) {
                sb.append("   🚨 High: ").append(result.getVulnerabilityReport().getHighCount()).append("\n");
            }
            if (result.getVulnerabilityReport().getMediumCount() != null && result.getVulnerabilityReport().getMediumCount() > 0) {
                sb.append("   ⚡ Medium: ").append(result.getVulnerabilityReport().getMediumCount()).append("\n");
            }
            if (result.getVulnerabilityReport().getLowCount() != null && result.getVulnerabilityReport().getLowCount() > 0) {
                sb.append("   ℹ️  Low: ").append(result.getVulnerabilityReport().getLowCount()).append("\n");
            }
            sb.append("\n");
        }
        
        // Policy Violations
        if (result.getPolicyViolations() != null && !result.getPolicyViolations().isEmpty()) {
            sb.append("📋 Policy Violations:\n");
            sb.append("   Total Violations: ").append(result.getPolicyViolations().size()).append("\n");
            
            long blockingViolations = result.getPolicyViolations().stream()
                .filter(v -> v.isBlockingViolation())
                .count();
            if (blockingViolations > 0) {
                sb.append("   🚫 Blocking: ").append(blockingViolations).append("\n");
            }
            sb.append("\n");
        }
        
        // AI Analysis Result
        if (result.getAiAnalysisResult() != null) {
            sb.append("🤖 AI Risk Analysis:\n");
            sb.append("   Risk Level: ").append(result.getAiAnalysisResult().getRiskLevel()).append("\n");
            sb.append("   Risk Score: ").append(String.format("%.2f", result.getAiAnalysisResult().getRiskScore())).append("/10\n");
            
            if (result.getAiAnalysisResult().getConfidenceScore() != null) {
                sb.append("   Confidence: ").append(String.format("%.1f%%", result.getAiAnalysisResult().getConfidenceScore() * 100)).append("\n");
            }
            sb.append("\n");
        }
        
        // Status
        if (result.isSuccessful()) {
            sb.append("✅ Analysis completed successfully!\n");
        } else {
            sb.append("❌ Analysis failed: ").append(result.getErrorMessage()).append("\n");
        }
        
        return sb.toString();
    }

    @Override
    public String getFileExtension() {
        return "txt";
    }
} 