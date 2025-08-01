"""
Comprehensive examples of SBOMAI Engine analysis with different formats and scenarios.
"""

import json
import re
from datetime import datetime
from pprint import pprint

# Example 1: CycloneDX Format with Container Image
cyclonedx_container_example = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.4",
    "version": 1,
    "metadata": {
        "timestamp": "2024-03-15T08:30:00Z",
        "tools": [
            {
                "vendor": "Example",
                "name": "container-scanner",
                "version": "1.0.0"
            }
        ],
        "component": {
            "type": "container",
            "name": "example/web-app",
            "version": "1.2.3"
        }
    },
    "components": [
        {
            "type": "library",
            "name": "nginx",
            "version": "1.18.0",
            "purl": "pkg:deb/nginx@1.18.0",
            "properties": [
                {
                    "name": "layer",
                    "value": "sha256:a123..."
                }
            ]
        },
        {
            "type": "library",
            "name": "openssl",
            "version": "1.1.1k",
            "purl": "pkg:deb/openssl@1.1.1k",
            "properties": [
                {
                    "name": "layer",
                    "value": "sha256:b456..."
                }
            ]
        }
    ],
    "vulnerabilities": [
        {
            "id": "CVE-2021-3449",
            "source": {
                "name": "NVD",
                "url": "https://nvd.nist.gov/vuln/detail/CVE-2021-3449"
            },
            "ratings": [
                {
                    "source": {
                        "name": "NVD"
                    },
                    "score": 7.5,
                    "severity": "HIGH",
                    "method": "CVSSv3.1",
                    "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"
                }
            ],
            "affects": [
                {
                    "ref": "pkg:deb/openssl@1.1.1k"
                }
            ]
        }
    ]
}

# Example 2: SPDX Format with NPM Dependencies
spdx_npm_example = {
    "SPDXID": "SPDXRef-DOCUMENT",
    "spdxVersion": "SPDX-2.3",
    "creationInfo": {
        "created": "2024-03-15T08:30:00Z",
        "creators": ["Tool: npm-audit-resolver-1.0.0"]
    },
    "name": "example-node-app",
    "packages": [
        {
            "SPDXID": "SPDXRef-Package-express",
            "name": "express",
            "versionInfo": "4.17.1",
            "downloadLocation": "https://registry.npmjs.org/express/-/express-4.17.1.tgz",
            "licenseConcluded": "MIT",
            "externalRefs": [
                {
                    "referenceCategory": "SECURITY",
                    "referenceType": "cpe23Type",
                    "referenceLocator": "cpe:2.3:a:expressjs:express:4.17.1:*:*:*:*:node.js:*:*"
                }
            ]
        },
        {
            "SPDXID": "SPDXRef-Package-lodash",
            "name": "lodash",
            "versionInfo": "4.17.15",
            "downloadLocation": "https://registry.npmjs.org/lodash/-/lodash-4.17.15.tgz",
            "licenseConcluded": "MIT",
            "externalRefs": [
                {
                    "referenceCategory": "SECURITY",
                    "referenceType": "cpe23Type",
                    "referenceLocator": "cpe:2.3:a:lodash:lodash:4.17.15:*:*:*:*:node.js:*:*"
                }
            ]
        }
    ],
    "relationships": [
        {
            "spdxElementId": "SPDXRef-DOCUMENT",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": "SPDXRef-Package-express"
        },
        {
            "spdxElementId": "SPDXRef-DOCUMENT",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": "SPDXRef-Package-lodash"
        }
    ]
}

# Example 3: GitHub Advisory Format
github_advisory_example = {
    "data": {
        "securityAdvisories": {
            "nodes": [
                {
                    "ghsaId": "GHSA-93q8-gq69-wqmw",
                    "summary": "Prototype Pollution in lodash",
                    "severity": "HIGH",
                    "cvss": {
                        "score": 7.4,
                        "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"
                    },
                    "identifiers": [
                        {
                            "type": "CVE",
                            "value": "CVE-2020-8203"
                        }
                    ],
                    "references": [
                        {
                            "url": "https://github.com/advisories/GHSA-93q8-gq69-wqmw"
                        }
                    ],
                    "publishedAt": "2020-07-15T18:00:00Z",
                    "updatedAt": "2020-07-16T14:00:00Z"
                }
            ]
        }
    }
}

# Example 4: OSV Format
osv_example = {
    "id": "GHSA-93q8-gq69-wqmw",
    "summary": "Prototype Pollution in lodash",
    "details": "Prototype pollution vulnerability in lodash <4.17.19 allows attackers to modify object properties via crafted payloads.",
    "modified": "2020-07-16T14:00:00Z",
    "published": "2020-07-15T18:00:00Z",
    "references": [
        {
            "type": "ADVISORY",
            "url": "https://github.com/advisories/GHSA-93q8-gq69-wqmw"
        }
    ],
    "affected": [
        {
            "package": {
                "name": "lodash",
                "ecosystem": "npm"
            },
            "ranges": [
                {
                    "type": "SEMVER",
                    "events": [
                        {
                            "introduced": "0"
                        },
                        {
                            "fixed": "4.17.19"
                        }
                    ]
                }
            ],
            "versions": [
                "4.17.15",
                "4.17.16",
                "4.17.17",
                "4.17.18"
            ]
        }
    ],
    "schema_version": "1.4.0"
}

def analyze_cyclonedx(sbom_data):
    """Analyze CycloneDX format SBOM"""
    print("\n=== Analyzing CycloneDX SBOM ===")
    print(f"Container Image: {sbom_data['metadata']['component']['name']}:{sbom_data['metadata']['component']['version']}")
    
    # Analyze components
    print("\nComponents:")
    for component in sbom_data['components']:
        print(f"\n- {component['name']} {component['version']}")
        print(f"  Type: {component['type']}")
        print(f"  PURL: {component['purl']}")
        if 'properties' in component:
            for prop in component['properties']:
                print(f"  {prop['name']}: {prop['value']}")
    
    # Analyze vulnerabilities
    print("\nVulnerabilities:")
    for vuln in sbom_data.get('vulnerabilities', []):
        print(f"\n- {vuln['id']}")
        for rating in vuln['ratings']:
            print(f"  Severity: {rating['severity']}")
            print(f"  CVSS Score: {rating['score']}")
            print(f"  CVSS Vector: {rating['vector']}")
        print("  Affects:")
        for affected in vuln['affects']:
            print(f"    - {affected['ref']}")

def analyze_spdx(sbom_data):
    """Analyze SPDX format SBOM"""
    print("\n=== Analyzing SPDX SBOM ===")
    print(f"Package: {sbom_data['name']}")
    print(f"SPDX Version: {sbom_data['spdxVersion']}")
    
    # Analyze packages
    print("\nPackages:")
    for package in sbom_data['packages']:
        print(f"\n- {package['name']} {package['versionInfo']}")
        print(f"  SPDX ID: {package['SPDXID']}")
        print(f"  License: {package['licenseConcluded']}")
        print("  External References:")
        for ref in package['externalRefs']:
            print(f"    - {ref['referenceType']}: {ref['referenceLocator']}")
    
    # Analyze relationships
    print("\nRelationships:")
    for rel in sbom_data['relationships']:
        print(f"- {rel['spdxElementId']} {rel['relationshipType']} {rel['relatedSpdxElement']}")

def analyze_github_advisory(advisory_data):
    """Analyze GitHub Security Advisory"""
    print("\n=== Analyzing GitHub Security Advisory ===")
    
    for advisory in advisory_data['data']['securityAdvisories']['nodes']:
        print(f"\nAdvisory: {advisory['ghsaId']}")
        print(f"Summary: {advisory['summary']}")
        print(f"Severity: {advisory['severity']}")
        print(f"CVSS Score: {advisory['cvss']['score']}")
        print(f"CVSS Vector: {advisory['cvss']['vectorString']}")
        print("\nIdentifiers:")
        for identifier in advisory['identifiers']:
            print(f"- {identifier['type']}: {identifier['value']}")
        print("\nReferences:")
        for ref in advisory['references']:
            print(f"- {ref['url']}")
        print(f"\nPublished: {advisory['publishedAt']}")
        print(f"Updated: {advisory['updatedAt']}")

def analyze_osv(osv_data):
    """Analyze OSV vulnerability data"""
    print("\n=== Analyzing OSV Vulnerability ===")
    
    print(f"ID: {osv_data['id']}")
    print(f"Summary: {osv_data['summary']}")
    print(f"Details: {osv_data['details']}")
    print(f"Published: {osv_data['published']}")
    print(f"Modified: {osv_data['modified']}")
    
    print("\nAffected Packages:")
    for affected in osv_data['affected']:
        print(f"\n- Package: {affected['package']['name']}")
        print(f"  Ecosystem: {affected['package']['ecosystem']}")
        print("  Version Ranges:")
        for range_info in affected['ranges']:
            print(f"  - Type: {range_info['type']}")
            for event in range_info['events']:
                if 'introduced' in event:
                    print(f"    Introduced: {event['introduced']}")
                if 'fixed' in event:
                    print(f"    Fixed: {event['fixed']}")
        print("  Affected Versions:")
        for version in affected['versions']:
            print(f"    - {version}")
    
    print("\nReferences:")
    for ref in osv_data['references']:
        print(f"- [{ref['type']}] {ref['url']}")

def calculate_severity_metrics(data):
    """Calculate severity metrics across different formats"""
    metrics = {
        'total_components': 0,
        'vulnerable_components': 0,
        'max_cvss_score': 0.0,
        'severity_counts': {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
    }
    
    # CycloneDX metrics
    if isinstance(data, dict) and data.get('bomFormat') == 'CycloneDX':
        metrics['total_components'] = len(data.get('components', []))
        for vuln in data.get('vulnerabilities', []):
            metrics['vulnerable_components'] += 1
            for rating in vuln.get('ratings', []):
                metrics['max_cvss_score'] = max(metrics['max_cvss_score'], rating.get('score', 0.0))
                metrics['severity_counts'][rating.get('severity', 'LOW')] += 1
    
    # SPDX metrics
    elif isinstance(data, dict) and data.get('SPDXID'):
        metrics['total_components'] = len(data.get('packages', []))
        # Note: SPDX doesn't include vulnerability info directly
    
    # GitHub Advisory metrics
    elif isinstance(data, dict) and 'data' in data and 'securityAdvisories' in data['data']:
        for advisory in data['data']['securityAdvisories']['nodes']:
            metrics['vulnerable_components'] += 1
            metrics['max_cvss_score'] = max(metrics['max_cvss_score'], advisory['cvss']['score'])
            metrics['severity_counts'][advisory['severity']] += 1
    
    # OSV metrics
    elif isinstance(data, dict) and 'affected' in data:
        for affected in data['affected']:
            metrics['vulnerable_components'] += len(affected.get('versions', []))
    
    return metrics

def main():
    """Run analysis on all example formats"""
    print("\n=== SBOMAI Engine Comprehensive Analysis ===")
    
    # 1. Analyze CycloneDX container example
    analyze_cyclonedx(cyclonedx_container_example)
    metrics_cyclonedx = calculate_severity_metrics(cyclonedx_container_example)
    print("\nCycloneDX Metrics:")
    pprint(metrics_cyclonedx)
    
    # 2. Analyze SPDX NPM example
    analyze_spdx(spdx_npm_example)
    metrics_spdx = calculate_severity_metrics(spdx_npm_example)
    print("\nSPDX Metrics:")
    pprint(metrics_spdx)
    
    # 3. Analyze GitHub Advisory example
    analyze_github_advisory(github_advisory_example)
    metrics_github = calculate_severity_metrics(github_advisory_example)
    print("\nGitHub Advisory Metrics:")
    pprint(metrics_github)
    
    # 4. Analyze OSV example
    analyze_osv(osv_example)
    metrics_osv = calculate_severity_metrics(osv_example)
    print("\nOSV Metrics:")
    pprint(metrics_osv)

if __name__ == '__main__':
    main()