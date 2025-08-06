package models

import (
	"time"
)

// SBOM represents a Software Bill of Materials in CycloneDX format
type SBOM struct {
	BOMFormat    string       `json:"bomFormat"`
	SpecVersion  string       `json:"specVersion"`
	Version      int          `json:"version"`
	Metadata     Metadata     `json:"metadata"`
	Components   []Component  `json:"components"`
	Dependencies []Dependency `json:"dependencies,omitempty"`
}

// Metadata contains information about the SBOM
type Metadata struct {
	Timestamp time.Time `json:"timestamp"`
	// The `tools` field in the JSON is an object, not an array.
	// We need a nested struct to correctly unmarshal it.
	Tools     struct {
		Components []Tool `json:"components"`
	} `json:"tools"`
	Component Component `json:"component"`
}

// Tool represents a tool used to generate the SBOM
type Tool struct {
	Vendor  string `json:"vendor,omitempty"`
	Name    string `json:"name"`
	Version string `json:"version,omitempty"`
	Hashes  []Hash `json:"hashes,omitempty"`
}

// Component represents a software component
type Component struct {
	Type            string          `json:"type"`
	BOMRef          string          `json:"bom-ref"`
	Name            string          `json:"name"`
	Version         string          `json:"version"`
	Description     string          `json:"description,omitempty"`
	Hashes          []Hash          `json:"hashes,omitempty"`
	Licenses        []License       `json:"licenses,omitempty"`
	PURL            string          `json:"purl,omitempty"`
	CPE             string          `json:"cpe,omitempty"`
	Properties      []Property      `json:"properties,omitempty"`
	Vulnerabilities []Vulnerability `json:"vulnerabilities,omitempty"`
}

// Hash represents a cryptographic hash
type Hash struct {
	Alg     string `json:"alg"`
	Content string `json:"content"`
}

// License represents a software license
type License struct {
	ID   string `json:"id,omitempty"`
	Name string `json:"name,omitempty"`
	URL  string `json:"url,omitempty"`
}

// Property represents a key-value property
type Property struct {
	Name  string `json:"name"`
	Value string `json:"value"`
}

// Vulnerability represents a security vulnerability
type Vulnerability struct {
	ID          string     `json:"id"`
	Source      Source     `json:"source"`
	Ratings     []Rating   `json:"ratings,omitempty"`
	Description string     `json:"description,omitempty"`
	Advisories  []Advisory `json:"advisories,omitempty"`
}

// Source represents the source of vulnerability information
type Source struct {
	Name string `json:"name"`
	URL  string `json:"url,omitempty"`
}

// Rating represents a vulnerability rating
type Rating struct {
	Source   Source  `json:"source"`
	Score    float64 `json:"score,omitempty"`
	Severity string  `json:"severity,omitempty"`
	Method   string  `json:"method,omitempty"`
	Vector   string  `json:"vector,omitempty"`
}

// Advisory represents a security advisory
type Advisory struct {
	Title string `json:"title"`
	URL   string `json:"url"`
}

// Dependency represents a dependency relationship
type Dependency struct {
	Ref       string   `json:"ref"`
	DependsOn []string `json:"dependsOn,omitempty"`
}
