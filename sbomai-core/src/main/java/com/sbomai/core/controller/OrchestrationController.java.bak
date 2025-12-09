package com.sbomai.core.controller;

import com.sbomai.core.dto.SbomReceivedEvent;
import com.sbomai.core.service.SbomProcessingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.UUID;

@RestController
@RequestMapping("/orchestration")
public class OrchestrationController {
    
    @Autowired
    private SbomProcessingService sbomProcessingService;
    
    @PostMapping("/trigger-sbom-processing")
    public ResponseEntity<String> triggerSbomProcessing(@RequestBody SbomReceivedEvent event) {
        try {
            // This would typically be triggered by Kafka, but we provide a REST endpoint for testing
            sbomProcessingService.processSbomReceived(event);
            return ResponseEntity.ok("SBOM processing triggered successfully for scan: " + event.getScanId());
        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                    .body("Failed to trigger SBOM processing: " + e.getMessage());
        }
    }
    
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("SBOMAI Core Orchestrator is running");
    }
    
    @PostMapping("/create-scan")
    public ResponseEntity<String> createScan(@RequestParam String targetIdentifier, @RequestParam String scanType) {
        try {
            // Create a new scan for testing
            SbomReceivedEvent event = new SbomReceivedEvent();
            event.setScanId(UUID.randomUUID());
            event.setTargetIdentifier(targetIdentifier);
            event.setScanType(scanType);
            event.setRawSbomContent("{\"bomFormat\":\"CycloneDX\",\"specVersion\":\"1.6\",\"components\":[]}");
            
            sbomProcessingService.processSbomReceived(event);
            return ResponseEntity.ok("Scan created and processing started for: " + targetIdentifier);
        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                    .body("Failed to create scan: " + e.getMessage());
        }
    }
}
