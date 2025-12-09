

package com.sbomai.core.controller;

import com.sbomai.core.service.SbomParserService;
import com.sbomai.core.service.impl.SbomParserServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/health")
@CrossOrigin(origins = "*")
public class HealthController {
    
    @Autowired
    private SbomParserServiceImpl sbomParserService;
    
    /**
     * GET /api/v1/health/parser - Check Go parser health
     */
    @GetMapping("/parser")
    public ResponseEntity<Map<String, Object>> getParserHealth() {
        Map<String, Object> health = new HashMap<>();
        
        try {
            boolean parserAvailable = sbomParserService.testParserAvailability();
            String parserVersion = sbomParserService.getParserVersion();
            String[] supportedFormats = sbomParserService.getSupportedFormats();
            
            health.put("status", parserAvailable ? "healthy" : "unhealthy");
            health.put("parserAvailable", parserAvailable);
            health.put("parserVersion", parserVersion);
            health.put("supportedFormats", supportedFormats);
            health.put("timestamp", System.currentTimeMillis());
            
            return ResponseEntity.ok(health);
            
        } catch (Exception e) {
            health.put("status", "unhealthy");
            health.put("error", e.getMessage());
            health.put("timestamp", System.currentTimeMillis());
            
            return ResponseEntity.status(503).body(health);
        }
    }
    
    /**
     * GET /api/v1/health/system - Get system health information
     */
    @GetMapping("/system")
    public ResponseEntity<Map<String, Object>> getSystemHealth() {
        Map<String, Object> health = new HashMap<>();
        
        try {
            Runtime runtime = Runtime.getRuntime();
            
            health.put("status", "healthy");
            health.put("javaVersion", System.getProperty("java.version"));
            health.put("javaVendor", System.getProperty("java.vendor"));
            health.put("osName", System.getProperty("os.name"));
            health.put("osVersion", System.getProperty("os.version"));
            health.put("totalMemory", runtime.totalMemory());
            health.put("freeMemory", runtime.freeMemory());
            health.put("maxMemory", runtime.maxMemory());
            health.put("availableProcessors", runtime.availableProcessors());
            health.put("timestamp", System.currentTimeMillis());
            
            return ResponseEntity.ok(health);
            
        } catch (Exception e) {
            health.put("status", "unhealthy");
            health.put("error", e.getMessage());
            health.put("timestamp", System.currentTimeMillis());
            
            return ResponseEntity.status(503).body(health);
        }
    }
} 