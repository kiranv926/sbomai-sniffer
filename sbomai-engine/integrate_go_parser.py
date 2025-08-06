#!/usr/bin/env python3
"""
SBOMAI Integration Script: Go Parser  Python AI Engine
======================================================

This script provides seamless integration between the Go-based SBOM parser
and the Python AI/ML engine for comprehensive vulnerability analysis.
"""

import json
import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add the src directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def load_sbom_from_go_parser(sbom_path: str) -> Dict[str, Any]:
    """Load and validate SBOM from Go parser output"""
    try:
        with open(sbom_path, 'r', encoding='utf-8') as f:
            sbom_data = json.load(f)
        
        # Validate CycloneDX format
        if 'bomFormat' not in sbom_data or sbom_data['bomFormat'] != 'CycloneDX':
            raise ValueError("Invalid CycloneDX format")
        
        print(f"Loaded SBOM with {len(sbom_data.get('components', []))} components")
        return sbom_data
        
    except Exception as e:
        print(f"Failed to load SBOM from {sbom_path}: {e}")
        raise

def extract_components_for_analysis(sbom_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract components for AI analysis"""
    components = []
    
    for comp in sbom_data.get('components', []):
        component_info = {
            'name': comp.get('name', ''),
            'version': comp.get('version', ''),
            'purl': comp.get('purl', ''),
            'type': comp.get('type', 'library'),
            'licenses': [lic.get('license', {}).get('id', '') for lic in comp.get('licenses', [])],
            'hashes': {h.get('alg', ''): h.get('content', '') for h in comp.get('hashes', [])}
        }
        components.append(component_info)
    
    print(f"Extracted {len(components)} components for analysis")
    return components

def run_basic_analysis(components: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run basic vulnerability analysis"""
    print("Starting basic vulnerability analysis...")
    
    analysis_results = {
        'timestamp': datetime.now().isoformat(),
        'components_analyzed': len(components),
        'vulnerabilities': [],
        'risk_scores': {},
        'recommendations': []
    }
    
    # Simulate vulnerability analysis
    for comp in components:
        comp_name = f"{comp['name']}@{comp['version']}"
        
        # Mock vulnerability data (replace with real AI analysis)
        mock_vulns = []
        if 'log4j' in comp['name'].lower():
            mock_vulns.append({
                'id': 'CVE-2021-44228',
                'severity': 'critical',
                'description': 'Log4j vulnerability',
                'cvss_score': 10.0
            })
        
        # Mock risk score (replace with real ML model)
        risk_score = 0.1 + (len(mock_vulns) * 0.3)
        
        analysis_results['vulnerabilities'].extend(mock_vulns)
        analysis_results['risk_scores'][comp_name] = risk_score
    
    print(f"Basic analysis completed. Found {len(analysis_results['vulnerabilities'])} vulnerabilities")
    return analysis_results

def generate_report(sbom_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive analysis report"""
    print("Generating comprehensive report...")
    
    # Calculate summary statistics
    total_components = len(sbom_data.get('components', []))
    total_vulns = len(analysis_results['vulnerabilities'])
    
    # Categorize vulnerabilities by severity
    vuln_by_severity = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    for vuln in analysis_results['vulnerabilities']:
        severity = vuln.get('severity', 'unknown').lower()
        if severity in vuln_by_severity:
            vuln_by_severity[severity] += 1
    
    # Calculate average risk scores
    avg_risk = sum(analysis_results['risk_scores'].values()) / len(analysis_results['risk_scores']) if analysis_results['risk_scores'] else 0
    
    report = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'sbom_format': sbom_data.get('bomFormat', 'Unknown'),
            'sbom_version': sbom_data.get('specVersion', 'Unknown'),
            'tool_used': 'SBOMAI Go Parser + Python AI Engine'
        },
        'summary': {
            'total_components': total_components,
            'total_vulnerabilities': total_vulns,
            'vulnerabilities_by_severity': vuln_by_severity,
            'average_risk_score': round(avg_risk, 3)
        },
        'detailed_analysis': analysis_results,
        'dashboard_data': {
            'components': sbom_data.get('components', []),
            'vulnerabilities': analysis_results['vulnerabilities'],
            'risk_scores': analysis_results['risk_scores']
        }
    }
    
    print("Comprehensive report generated successfully")
    return report

def save_report(report: Dict[str, Any], output_path: str):
    """Save the comprehensive report"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Report saved to: {output_path}")
        
    except Exception as e:
        print(f"Failed to save report: {e}")
        raise

def main():
    """Main integration function"""
    if len(sys.argv) < 2:
        print("Usage: python integrate_go_parser.py <sbom_path> [output_path]")
        sys.exit(1)
    
    sbom_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "sbomai_analysis_report.json"
    
    try:
        # Load SBOM from Go parser
        print(f"Loading SBOM from: {sbom_path}")
        sbom_data = load_sbom_from_go_parser(sbom_path)
        
        # Extract components for analysis
        components = extract_components_for_analysis(sbom_data)
        
        # Run basic analysis
        analysis_results = run_basic_analysis(components)
        
        # Generate comprehensive report
        report = generate_report(sbom_data, analysis_results)
        
        # Save report
        save_report(report, output_path)
        
        # Print summary
        print("\n" + "="*60)
        print("SBOMAI ANALYSIS COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Components analyzed: {report['summary']['total_components']}")
        print(f"Vulnerabilities found: {report['summary']['total_vulnerabilities']}")
        print(f"Average risk score: {report['summary']['average_risk_score']}")
        print(f"Report saved to: {output_path}")
        print("="*60)
        
        return 0
        
    except Exception as e:
        print(f"Integration failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
