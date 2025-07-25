package com.sbomai.core.ports;

import com.sbomai.core.domain.SbomDocument;
import com.sbomai.core.domain.SbomFormat;

import java.io.InputStream;
import java.util.Optional;

/**
 * Core interface for SBOM parsing operations.
 * 
 * This interface defines the contract for parsing SBOM documents
 * from various formats (SPDX, CycloneDX, etc.) into the internal
 * domain model.
 */
public interface SbomParser {

    /**
     * Parses an SBOM document from the given input stream.
     * 
     * @param inputStream The input stream containing the SBOM data
     * @param format The expected format of the SBOM
     * @return Optional containing the parsed SBOM document, or empty if parsing fails
     * @throws SbomParsingException if parsing fails due to invalid format or data
     */
    Optional<SbomDocument> parse(InputStream inputStream, SbomFormat format) throws SbomParsingException;

    /**
     * Parses an SBOM document from a string content.
     * 
     * @param content The string content of the SBOM
     * @param format The expected format of the SBOM
     * @return Optional containing the parsed SBOM document, or empty if parsing fails
     * @throws SbomParsingException if parsing fails due to invalid format or data
     */
    Optional<SbomDocument> parse(String content, SbomFormat format) throws SbomParsingException;

    /**
     * Parses an SBOM document from a file path.
     * 
     * @param filePath The path to the SBOM file
     * @param format The expected format of the SBOM
     * @return Optional containing the parsed SBOM document, or empty if parsing fails
     * @throws SbomParsingException if parsing fails due to invalid format or data
     */
    Optional<SbomDocument> parseFromFile(String filePath, SbomFormat format) throws SbomParsingException;

    /**
     * Validates if the given content can be parsed as the specified format.
     * 
     * @param content The content to validate
     * @param format The format to validate against
     * @return true if the content is valid for the specified format, false otherwise
     */
    boolean isValidFormat(String content, SbomFormat format);

    /**
     * Gets the supported formats for this parser.
     * 
     * @return Array of supported SBOM formats
     */
    SbomFormat[] getSupportedFormats();
} 