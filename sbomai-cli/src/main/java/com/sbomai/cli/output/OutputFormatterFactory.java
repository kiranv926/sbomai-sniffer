package com.sbomai.cli.output;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * Factory for creating output formatters based on format type.
 */
@Component
public class OutputFormatterFactory {

    private final Map<String, OutputFormatter> formatters;

    @Autowired
    public OutputFormatterFactory(TextOutputFormatter textFormatter, 
                                 JsonOutputFormatter jsonFormatter) {
        this.formatters = Map.of(
            "TEXT", textFormatter,
            "JSON", jsonFormatter
        );
    }

    /**
     * Get an output formatter for the specified format.
     * 
     * @param format The output format (TEXT, JSON, HTML)
     * @return The appropriate output formatter
     * @throws IllegalArgumentException if format is not supported
     */
    public OutputFormatter getFormatter(String format) {
        String upperFormat = format.toUpperCase();
        OutputFormatter formatter = formatters.get(upperFormat);
        
        if (formatter == null) {
            throw new IllegalArgumentException("Unsupported output format: " + format + 
                ". Supported formats: " + String.join(", ", formatters.keySet()));
        }
        
        return formatter;
    }

    /**
     * Get the list of supported output formats.
     * 
     * @return Array of supported format names
     */
    public String[] getSupportedFormats() {
        return formatters.keySet().toArray(new String[0]);
    }
} 