package com.sbomai.cli.commands;

import java.io.File;

/**
 * Request object for CLI SBOM analysis.
 */
public class AnalysisRequest {
    private File sbomFile;
    private String format;
    private String outputFormat;
    private boolean useRemote;
    private String remoteUrl;
    private boolean verbose;
    private boolean skipAiAnalysis;
    private boolean skipVulnerabilityScan;
    private boolean skipPolicyCheck;

    // Getters and Setters
    public File getSbomFile() { return sbomFile; }
    public void setSbomFile(File sbomFile) { this.sbomFile = sbomFile; }

    public String getFormat() { return format; }
    public void setFormat(String format) { this.format = format; }

    public String getOutputFormat() { return outputFormat; }
    public void setOutputFormat(String outputFormat) { this.outputFormat = outputFormat; }

    public boolean isUseRemote() { return useRemote; }
    public void setUseRemote(boolean useRemote) { this.useRemote = useRemote; }

    public String getRemoteUrl() { return remoteUrl; }
    public void setRemoteUrl(String remoteUrl) { this.remoteUrl = remoteUrl; }

    public boolean isVerbose() { return verbose; }
    public void setVerbose(boolean verbose) { this.verbose = verbose; }

    public boolean isSkipAiAnalysis() { return skipAiAnalysis; }
    public void setSkipAiAnalysis(boolean skipAiAnalysis) { this.skipAiAnalysis = skipAiAnalysis; }

    public boolean isSkipVulnerabilityScan() { return skipVulnerabilityScan; }
    public void setSkipVulnerabilityScan(boolean skipVulnerabilityScan) { this.skipVulnerabilityScan = skipVulnerabilityScan; }

    public boolean isSkipPolicyCheck() { return skipPolicyCheck; }
    public void setSkipPolicyCheck(boolean skipPolicyCheck) { this.skipPolicyCheck = skipPolicyCheck; }
} 