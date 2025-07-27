package com.sbomai.webscan.ports;

/**
 * Information about the web scanner.
 */
public class ScannerInfo {
    private final String name;
    private final String version;
    private final String description;
    private final String vendor;
    private final boolean isAvailable;

    public ScannerInfo(String name, String version, String description, String vendor, boolean isAvailable) {
        this.name = name;
        this.version = version;
        this.description = description;
        this.vendor = vendor;
        this.isAvailable = isAvailable;
    }

    public String getName() { return name; }
    public String getVersion() { return version; }
    public String getDescription() { return description; }
    public String getVendor() { return vendor; }
    public boolean isAvailable() { return isAvailable; }

    public static ScannerInfo defaultInfo() {
        return new ScannerInfo(
            "SBOMAI Web Scanner",
            "1.0.0",
            "Comprehensive website security scanner for detecting outdated libraries, security headers, and exposed metadata",
            "SBOMAI",
            true
        );
    }

    @Override
    public String toString() {
        return "ScannerInfo{" +
                "name='" + name + '\'' +
                ", version='" + version + '\'' +
                ", vendor='" + vendor + '\'' +
                ", isAvailable=" + isAvailable +
                '}';
    }
} 