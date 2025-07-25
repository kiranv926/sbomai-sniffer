package com.sbomai.parser.ports;

import com.sbomai.parser.domain.SbomDocument;
import com.sbomai.parser.domain.SbomFormat;

import java.io.InputStream;
import java.util.List;

/**
 * Port interface for SBOM parsing operations.
 * This defines the contract for parsing SBOM documents from various formats.
 */
public interface SbomParser {
    
    /**
     * Parse an SBOM document from an input stream.
     * 
     * @param inputStream The input stream containing the SBOM data
     * @param format The expected format of the SBOM
     * @return The parsed SBOM document
     * @throws SbomParsingException if parsing fails
     */
    SbomDocument parse(InputStream inputStream, SbomFormat format) throws SbomParsingException;
    
    /**
     * Parse an SBOM document from a string content.
     * 
     * @param content The string content of the SBOM
     * @param format The expected format of the SBOM
     * @return The parsed SBOM document
     * @throws SbomParsingException if parsing fails
     */
    SbomDocument parse(String content, SbomFormat format) throws SbomParsingException;
    
    /**
     * Parse an SBOM document from a file path.
     * 
     * @param filePath The path to the SBOM file
     * @param format The expected format of the SBOM
     * @return The parsed SBOM document
     * @throws SbomParsingException if parsing fails
     */
    SbomDocument parseFromFile(String filePath, SbomFormat format) throws SbomParsingException;
    
    /**
     * Auto-detect the format of an SBOM document from its content.
     * 
     * @param content The string content of the SBOM
     * @return The detected format, or null if detection fails
     */
    SbomFormat detectFormat(String content);
    
    /**
     * Auto-detect the format of an SBOM document from an input stream.
     * 
     * @param inputStream The input stream containing the SBOM data
     * @return The detected format, or null if detection fails
     */
    SbomFormat detectFormat(InputStream inputStream);
    
    /**
     * Validate an SBOM document against its format specification.
     * 
     * @param document The SBOM document to validate
     * @return True if the document is valid, false otherwise
     */
    boolean validate(SbomDocument document);
    
    /**
     * Get the list of supported SBOM formats.
     * 
     * @return List of supported formats
     */
    List<SbomFormat> getSupportedFormats();
    
    /**
     * Check if a specific format is supported.
     * 
     * @param format The format to check
     * @return True if the format is supported, false otherwise
     */
    boolean isFormatSupported(SbomFormat format);
} 