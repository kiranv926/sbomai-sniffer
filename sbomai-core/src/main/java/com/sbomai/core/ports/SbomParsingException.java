package com.sbomai.core.ports;

/**
 * Exception thrown when SBOM parsing fails.
 */
public class SbomParsingException extends Exception {

    public SbomParsingException(String message) {
        super(message);
    }

    public SbomParsingException(String message, Throwable cause) {
        super(message, cause);
    }

    public SbomParsingException(Throwable cause) {
        super(cause);
    }
} 