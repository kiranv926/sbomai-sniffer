package com.sbomai.cli.output;

import com.sbomai.cli.commands.AnalysisResult;

/**
 * Interface for formatting analysis results to different output formats.
 */
public interface OutputFormatter {
    
    /**
     * Format the analysis result to the specified output format.
     * 
     * @param result The analysis result to format
     * @return Formatted string representation
     */
    String format(AnalysisResult result);
    
    /**
     * Get the file extension for this output format.
     * 
     * @return File extension (e.g., "json", "txt", "html")
     */
    String getFileExtension();
} 