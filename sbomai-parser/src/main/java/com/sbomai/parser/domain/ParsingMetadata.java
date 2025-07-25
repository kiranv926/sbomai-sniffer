package com.sbomai.parser.domain;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

/**
 * Metadata about the parsing process of an SBOM document.
 */
public class ParsingMetadata {
    
    private LocalDateTime parsedAt;
    private String parserVersion;
    private String originalFormat;
    private String originalVersion;
    private List<String> warnings;
    private List<String> errors;
    private Map<String, Object> formatSpecificData;
    private long parsingDurationMs;
    private boolean validationPassed;
    private List<String> validationErrors;
    
    // Constructors
    public ParsingMetadata() {
        this.parsedAt = LocalDateTime.now();
    }
    
    public ParsingMetadata(String parserVersion, String originalFormat) {
        this();
        this.parserVersion = parserVersion;
        this.originalFormat = originalFormat;
    }
    
    // Getters and Setters
    public LocalDateTime getParsedAt() { return parsedAt; }
    public void setParsedAt(LocalDateTime parsedAt) { this.parsedAt = parsedAt; }
    
    public String getParserVersion() { return parserVersion; }
    public void setParserVersion(String parserVersion) { this.parserVersion = parserVersion; }
    
    public String getOriginalFormat() { return originalFormat; }
    public void setOriginalFormat(String originalFormat) { this.originalFormat = originalFormat; }
    
    public String getOriginalVersion() { return originalVersion; }
    public void setOriginalVersion(String originalVersion) { this.originalVersion = originalVersion; }
    
    public List<String> getWarnings() { return warnings; }
    public void setWarnings(List<String> warnings) { this.warnings = warnings; }
    
    public List<String> getErrors() { return errors; }
    public void setErrors(List<String> errors) { this.errors = errors; }
    
    public Map<String, Object> getFormatSpecificData() { return formatSpecificData; }
    public void setFormatSpecificData(Map<String, Object> formatSpecificData) { this.formatSpecificData = formatSpecificData; }
    
    public long getParsingDurationMs() { return parsingDurationMs; }
    public void setParsingDurationMs(long parsingDurationMs) { this.parsingDurationMs = parsingDurationMs; }
    
    public boolean isValidationPassed() { return validationPassed; }
    public void setValidationPassed(boolean validationPassed) { this.validationPassed = validationPassed; }
    
    public List<String> getValidationErrors() { return validationErrors; }
    public void setValidationErrors(List<String> validationErrors) { this.validationErrors = validationErrors; }
    
    @Override
    public String toString() {
        return String.format("ParsingMetadata{parsedAt=%s, parserVersion='%s', originalFormat='%s', duration=%dms, validationPassed=%s}",
                parsedAt, parserVersion, originalFormat, parsingDurationMs, validationPassed);
    }
} 