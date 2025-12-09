package com.sbomai.core.service.impl;

import com.sbomai.core.service.SbomParserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.UUID;

@Service
public class SbomParserServiceImpl implements SbomParserService {
    
    private static final Logger logger = LoggerFactory.getLogger(SbomParserServiceImpl.class);
    
    @Value("${sbomai.parser.go.executable:./sbomai-parser-go/sbomai-parser.exe}")
    private String goParserExecutable;
    
    @Value("${sbomai.upload.directory:./uploads}")
    private String uploadDirectory;
    
    @Value("${sbomai.parser.timeout:30000}")
    private int parserTimeout;
    
    private static final String[] SUPPORTED_FORMATS = {
        ".json", ".xml", ".zip", ".sbom",
        "application/json", "application/xml", "text/xml",
        "application/zip", "application/x-zip-compressed"
    };
    
    @Override
    public String parseSbomFile(MultipartFile file) {
        try {
            // Create upload directory if it doesn't exist
            Path uploadPath = Paths.get(uploadDirectory);
            if (!Files.exists(uploadPath)) {
                Files.createDirectories(uploadPath);
            }
            
            // Save uploaded file temporarily
            String fileName = UUID.randomUUID().toString() + "_" + file.getOriginalFilename();
            Path filePath = uploadPath.resolve(fileName);
            Files.copy(file.getInputStream(), filePath);
            
            try {
                // Parse the file
                String result = parseSbomFile(filePath.toString());
                return result;
            } finally {
                // Clean up temporary file
                Files.deleteIfExists(filePath);
            }
            
        } catch (IOException e) {
            logger.error("Error processing SBOM file: {}", e.getMessage());
            throw new RuntimeException("Failed to process SBOM file", e);
        }
    }
    
    @Override
    public String parseSbomFile(String filePath) {
        try {
            // Validate file exists
            File file = new File(filePath);
            if (!file.exists()) {
                throw new RuntimeException("SBOM file not found: " + filePath);
            }
            
            // Execute Go parser
            ProcessBuilder processBuilder = new ProcessBuilder(goParserExecutable, filePath);
            processBuilder.redirectErrorStream(true);
            
            Process process = processBuilder.start();
            
            // Read output
            String output = new String(process.getInputStream().readAllBytes());
            
            // Wait for completion with timeout
            boolean completed = process.waitFor(parserTimeout, java.util.concurrent.TimeUnit.MILLISECONDS);
            if (!completed) {
                process.destroyForcibly();
                throw new RuntimeException("Parser execution timed out after " + parserTimeout + "ms");
            }
            
            int exitCode = process.exitValue();
            if (exitCode != 0) {
                logger.error("Go parser failed with exit code: {} and output: {}", exitCode, output);
                throw new RuntimeException("SBOM parsing failed with exit code: " + exitCode);
            }
            
            logger.info("Successfully parsed SBOM file: {}", filePath);
            return output;
            
        } catch (IOException | InterruptedException e) {
            logger.error("Error executing Go parser: {}", e.getMessage());
            throw new RuntimeException("Failed to parse SBOM with Go parser", e);
        }
    }
    
    @Override
    public boolean validateSbomFormat(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            return false;
        }
        
        String originalFilename = file.getOriginalFilename();
        String contentType = file.getContentType();
        
        // Check file extension
        if (originalFilename != null) {
            String lowerFilename = originalFilename.toLowerCase();
            for (String format : SUPPORTED_FORMATS) {
                if (lowerFilename.endsWith(format)) {
                    return true;
                }
            }
        }
        
        // Check content type
        if (contentType != null) {
            String lowerContentType = contentType.toLowerCase();
            for (String format : SUPPORTED_FORMATS) {
                if (lowerContentType.contains(format)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    @Override
    public String[] getSupportedFormats() {
        return Arrays.copyOf(SUPPORTED_FORMATS, SUPPORTED_FORMATS.length);
    }
    
    /**
     * Test if the Go parser executable is available and working
     */
    public boolean testParserAvailability() {
        try {
            ProcessBuilder processBuilder = new ProcessBuilder(goParserExecutable, "--help");
            Process process = processBuilder.start();
            
            int exitCode = process.waitFor();
            return exitCode == 0;
            
        } catch (IOException | InterruptedException e) {
            logger.warn("Go parser executable not available: {}", e.getMessage());
            return false;
        }
    }
    
    /**
     * Get parser version information
     */
    public String getParserVersion() {
        try {
            ProcessBuilder processBuilder = new ProcessBuilder(goParserExecutable, "--version");
            Process process = processBuilder.start();
            
            String output = new String(process.getInputStream().readAllBytes());
            int exitCode = process.waitFor();
            
            if (exitCode == 0) {
                return output.trim();
            } else {
                return "Version information not available";
            }
            
        } catch (IOException | InterruptedException e) {
            logger.warn("Could not get parser version: {}", e.getMessage());
            return "Version information not available";
        }
    }
} 