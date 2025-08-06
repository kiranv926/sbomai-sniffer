package scanner

import (
	"bytes" // New import for the bytes.Buffer
	"context"
	"encoding/json"
	"fmt"
	"path/filepath"

	"github.com/anchore/syft/syft"
	"github.com/anchore/syft/syft/format/cyclonedxjson"
	"github.com/anchore/syft/syft/sbom"
	"github.com/sbomai/sbomai-parser-go/pkg/models"
	"github.com/sirupsen/logrus"
)

// SyftScanner represents a scanner that uses Syft to generate SBOMs
type SyftScanner struct {
	config *syft.CreateSBOMConfig
}

// NewSyftScanner creates a new SyftScanner instance
func NewSyftScanner() *SyftScanner {
	return &SyftScanner{
		config: syft.DefaultCreateSBOMConfig(),
	}
}

// Scan scans a target and returns the SBOM as JSON
func (s *SyftScanner) Scan(target string) (string, error) {
	logrus.Infof("Scanning target with Syft: %s", target)

	ctx := context.Background()

	// Get source from target
	src, err := syft.GetSource(ctx, target, syft.DefaultGetSourceConfig())
	if err != nil {
		return "", fmt.Errorf("failed to get source from target: %w", err)
	}
	defer src.Close()

	// Generate SBOM using Syft
	sbomResult, err := syft.CreateSBOM(ctx, src, s.config)
	if err != nil {
		return "", fmt.Errorf("failed to create SBOM: %w", err)
	}

	// Convert to CycloneDX JSON format
	encoder, err := cyclonedxjson.NewFormatEncoderWithConfig(cyclonedxjson.DefaultEncoderConfig())
	if err != nil {
		return "", fmt.Errorf("failed to create CycloneDX encoder: %w", err)
	}

	// Create a buffer to write the encoded output to.
	var outputBuffer bytes.Buffer
	// The Encode method now takes an io.Writer and the SBOM object.
	// It returns only an error.
	if err := encoder.Encode(&outputBuffer, *sbomResult); err != nil {
		return "", fmt.Errorf("failed to format as CycloneDX JSON: %w", err)
	}

	// Get the bytes from the buffer after encoding.
	cyclonedxBytes := outputBuffer.Bytes()

	// For debugging, let's log the raw JSON structure
	logrus.Infof("Raw CycloneDX JSON length: %d bytes", len(cyclonedxBytes))
	
	// Parse the output to validate it is valid JSON
	var sbom models.SBOM
	if err := json.Unmarshal(cyclonedxBytes, &sbom); err != nil {
		// Log the first 500 characters of the JSON for debugging
		jsonPreview := string(cyclonedxBytes)
		if len(jsonPreview) > 500 {
			jsonPreview = jsonPreview[:500] + "..."
		}
		logrus.Errorf("JSON parsing failed. Preview: %s", jsonPreview)
		return "", fmt.Errorf("failed to parse syft output as JSON: %w", err)
	}

	logrus.Infof("Successfully scanned target. Found %d components", len(sbom.Components))

	return string(cyclonedxBytes), nil
}

// ScanDirectory scans a directory and returns the SBOM
func (s *SyftScanner) ScanDirectory(dirPath string) (string, error) {
	absPath, err := filepath.Abs(dirPath)
	if err != nil {
		return "", fmt.Errorf("failed to get absolute path: %w", err)
	}
	return s.Scan(absPath)
}

// ScanImage scans a Docker image and returns the SBOM
func (s *SyftScanner) ScanImage(imageName string) (string, error) {
	return s.Scan(imageName)
}

// GetSBOM returns the raw SBOM object
func (s *SyftScanner) GetSBOM(target string) (*sbom.SBOM, error) {
	logrus.Infof("Getting SBOM for target: %s", target)

	ctx := context.Background()

	// Get source from target
	src, err := syft.GetSource(ctx, target, syft.DefaultGetSourceConfig())
	if err != nil {
		return nil, fmt.Errorf("failed to get source from target: %w", err)
	}
	defer src.Close()

	// Generate SBOM using Syft
	sbomResult, err := syft.CreateSBOM(ctx, src, s.config)
	if err != nil {
		return nil, fmt.Errorf("failed to create SBOM: %w", err)
	}

	return sbomResult, nil
}

// GetVersion returns the version of Syft being used
func (s *SyftScanner) GetVersion() string {
	return "v1.29.0"
}

// IsAvailable checks if Syft is available (always true when using library)
func (s *SyftScanner) IsAvailable() bool {
	return true
}


