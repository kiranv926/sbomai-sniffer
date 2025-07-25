package com.sbomai.core.ports;

/**
 * Exception thrown when AI analysis fails.
 */
public class AiAnalysisException extends Exception {

    public AiAnalysisException(String message) {
        super(message);
    }

    public AiAnalysisException(String message, Throwable cause) {
        super(message, cause);
    }

    public AiAnalysisException(Throwable cause) {
        super(cause);
    }
} 