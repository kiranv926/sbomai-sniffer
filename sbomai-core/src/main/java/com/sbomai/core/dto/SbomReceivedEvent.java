package com.sbomai.core.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.UUID;

public class SbomReceivedEvent {
    @JsonProperty("scan_id")
    private UUID scanId;
    
    @JsonProperty("raw_sbom_content")
    private String rawSbomContent;
    
    @JsonProperty("target_identifier")
    private String targetIdentifier;
    
    @JsonProperty("scan_type")
    private String scanType;
    
    public SbomReceivedEvent() {}
    
    public SbomReceivedEvent(UUID scanId, String rawSbomContent, String targetIdentifier, String scanType) {
        this.scanId = scanId;
        this.rawSbomContent = rawSbomContent;
        this.targetIdentifier = targetIdentifier;
        this.scanType = scanType;
    }
    
    // Getters and Setters
    public UUID getScanId() { return scanId; }
    public void setScanId(UUID scanId) { this.scanId = scanId; }
    
    public String getRawSbomContent() { return rawSbomContent; }
    public void setRawSbomContent(String rawSbomContent) { this.rawSbomContent = rawSbomContent; }
    
    public String getTargetIdentifier() { return targetIdentifier; }
    public void setTargetIdentifier(String targetIdentifier) { this.targetIdentifier = targetIdentifier; }
    
    public String getScanType() { return scanType; }
    public void setScanType(String scanType) { this.scanType = scanType; }
}
