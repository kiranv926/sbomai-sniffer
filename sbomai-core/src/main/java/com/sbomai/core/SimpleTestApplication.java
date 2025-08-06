package com.sbomai.core;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class SimpleTestApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(SimpleTestApplication.class, args);
    }
    
    @GetMapping("/health")
    public String health() {
        return "SBOMAI Core is running! Infrastructure test successful.";
    }
    
    @GetMapping("/")
    public String home() {
        return "Welcome to SBOMAI Core - AI-Powered SBOM Analysis Platform";
    }
} 