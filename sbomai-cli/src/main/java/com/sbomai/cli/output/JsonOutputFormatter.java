package com.sbomai.cli.output;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.sbomai.cli.commands.AnalysisResult;
import org.springframework.stereotype.Component;

/**
 * JSON formatter for machine-readable output.
 */
@Component
public class JsonOutputFormatter implements OutputFormatter {

    private final ObjectMapper objectMapper;

    public JsonOutputFormatter() {
        this.objectMapper = new ObjectMapper();
        this.objectMapper.enable(SerializationFeature.INDENT_OUTPUT);
    }

    @Override
    public String format(AnalysisResult result) {
        try {
            return objectMapper.writeValueAsString(result);
        } catch (Exception e) {
            // Fallback to simple JSON if serialization fails
            return createSimpleJson(result);
        }
    }

    private String createSimpleJson(AnalysisResult result) {
        StringBuilder sb = new StringBuilder();
        sb.append("{\n");
        sb.append("  \"successful\": ").append(result.isSuccessful()).append(",\n");
        
        if (result.getErrorMessage() != null) {
            sb.append("  \"errorMessage\": \"").append(escapeJson(result.getErrorMessage())).append("\",\n");
        }
        
        if (result.getSbomDocument() != null) {
            sb.append("  \"sbomDocument\": {\n");
            sb.append("    \"documentName\": \"").append(escapeJson(result.getSbomDocument().getDocumentName())).append("\",\n");
            sb.append("    \"documentVersion\": \"").append(escapeJson(result.getSbomDocument().getDocumentVersion())).append("\",\n");
            sb.append("    \"format\": \"").append(escapeJson(result.getSbomDocument().getSbomFormat().toString())).append("\",\n");
            sb.append("    \"componentCount\": ").append(result.getSbomDocument().getComponents().size()).append("\n");
            sb.append("  },\n");
        }
        
        if (result.getVulnerabilityReport() != null) {
            sb.append("  \"vulnerabilityReport\": {\n");
            sb.append("    \"totalVulnerabilities\": ").append(result.getVulnerabilityReport().getTotalVulnerabilities()).append(",\n");
            if (result.getVulnerabilityReport().getCriticalCount() != null) {
                sb.append("    \"criticalCount\": ").append(result.getVulnerabilityReport().getCriticalCount()).append(",\n");
            }
            if (result.getVulnerabilityReport().getHighCount() != null) {
                sb.append("    \"highCount\": ").append(result.getVulnerabilityReport().getHighCount()).append(",\n");
            }
            if (result.getVulnerabilityReport().getMediumCount() != null) {
                sb.append("    \"mediumCount\": ").append(result.getVulnerabilityReport().getMediumCount()).append(",\n");
            }
            if (result.getVulnerabilityReport().getLowCount() != null) {
                sb.append("    \"lowCount\": ").append(result.getVulnerabilityReport().getLowCount()).append("\n");
            }
            sb.append("  },\n");
        }
        
        if (result.getPolicyViolations() != null && !result.getPolicyViolations().isEmpty()) {
            sb.append("  \"policyViolations\": {\n");
            sb.append("    \"totalViolations\": ").append(result.getPolicyViolations().size()).append(",\n");
            long blockingViolations = result.getPolicyViolations().stream()
                .filter(v -> v.isBlockingViolation())
                .count();
            sb.append("    \"blockingViolations\": ").append(blockingViolations).append("\n");
            sb.append("  },\n");
        }
        
        if (result.getAiAnalysisResult() != null) {
            sb.append("  \"aiAnalysisResult\": {\n");
            sb.append("    \"riskLevel\": \"").append(escapeJson(result.getAiAnalysisResult().getRiskLevel().toString())).append("\",\n");
            sb.append("    \"riskScore\": ").append(result.getAiAnalysisResult().getRiskScore()).append("\n");
            sb.append("  }\n");
        }
        
        sb.append("}");
        return sb.toString();
    }

    private String escapeJson(String value) {
        if (value == null) return "";
        return value.replace("\\", "\\\\")
                   .replace("\"", "\\\"")
                   .replace("\n", "\\n")
                   .replace("\r", "\\r")
                   .replace("\t", "\\t");
    }

    @Override
    public String getFileExtension() {
        return "json";
    }
} 