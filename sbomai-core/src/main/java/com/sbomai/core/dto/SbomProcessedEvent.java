package com.sbomai.core.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.UUID;

public class SbomProcessedEvent {
    @JsonProperty("scan_id")
    private UUID scanId;
    
    @JsonProperty("sbom_document_id")
    private UUID sbomDocumentId;
    
    @JsonProperty("components_count")
    private Integer componentsCount;
    
    public SbomProcessedEvent() {}
    
    public SbomProcessedEvent(UUID scanId, UUID sbomDocumentId, Integer componentsCount) {
        this.scanId = scanId;
        this.sbomDocumentId = sbomDocumentId;
        this.componentsCount = componentsCount;
    }
    
    // Getters and Setters
    public UUID getScanId() { return scanId; }
    public void setScanId(UUID scanId) { this.scanId = scanId; }
    
    public UUID getSbomDocumentId() { return sbomDocumentId; }
    public void setSbomDocumentId(UUID sbomDocumentId) { this.sbomDocumentId = sbomDocumentId; }
    
    public Integer getComponentsCount() { return componentsCount; }
    public void setComponentsCount(Integer componentsCount) { this.componentsCount = componentsCount; }
}
