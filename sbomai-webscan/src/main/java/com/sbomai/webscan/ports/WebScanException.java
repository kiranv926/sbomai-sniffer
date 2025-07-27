package com.sbomai.webscan.ports;

/**
 * Exception thrown when web scanning operations fail.
 */
public class WebScanException extends Exception {

    public WebScanException(String message) {
        super(message);
    }

    public WebScanException(String message, Throwable cause) {
        super(message, cause);
    }

    public WebScanException(Throwable cause) {
        super(cause);
    }
} 