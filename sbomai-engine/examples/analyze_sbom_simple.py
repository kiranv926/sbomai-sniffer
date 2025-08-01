"""
Simplified SBOM analysis example.
"""

import json
from datetime import datetime
from pprint import pprint

def analyze_component(component):
    """Analyze a single component"""
    
    # Known vulnerability data (for demonstration)
    vulnerability_data = {
        'log4j-core': {
            '2.14.1': {
                'vulnerabilities': [
                    {
                        'cve_id': 'CVE-2021-44228',
                        'severity': 'CRITICAL',
                        'cvss_score': 10.0,
                        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H',
                        'description': 'Remote code execution vulnerability in Log4j',
                        'attack_complexity': 'LOW',
                        'privileges_required': 'NONE',
                        'user_interaction': 'NONE',
                        'exploit_status': 'ACTIVE',
                        'patch_status': 'AVAILABLE',
                        'exploit_maturity': 'HIGH',
                        'remediation': 'Upgrade to version 2.15.0 or later'
                    }
                ],
                'risk_factors': [
                    {
                        'type': 'code_pattern',
                        'severity': 'critical',
                        'description': 'JNDI lookup vulnerability',
                        'impact': 'Remote code execution'
                    },
                    {
                        'type': 'exploit_availability',
                        'severity': 'critical',
                        'description': 'Multiple public exploits available',
                        'impact': 'Easy to exploit'
                    }
                ],
                'threat_intel': {
                    'exploit_count': 15,
                    'attack_types': ['remote_code_execution', 'data_theft'],
                    'targeted_systems': ['web_servers', 'application_servers'],
                    'observed_campaigns': 3,
                    'threat_level': 'CRITICAL'
                }
            }
        },
        'guava': {
            '30.0-jre': {
                'vulnerabilities': [
                    {
                        'cve_id': 'CVE-2020-8908',
                        'severity': 'MEDIUM',
                        'cvss_score': 5.5,
                        'cvss_vector': 'CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N',
                        'description': 'Information disclosure in Guava Temporary Directory Creation',
                        'attack_complexity': 'LOW',
                        'privileges_required': 'NONE',
                        'user_interaction': 'REQUIRED',
                        'exploit_status': 'POC',
                        'patch_status': 'AVAILABLE',
                        'exploit_maturity': 'LOW',
                        'remediation': 'Upgrade to version 30.1 or later'
                    }
                ],
                'risk_factors': [
                    {
                        'type': 'code_pattern',
                        'severity': 'medium',
                        'description': 'Insecure temporary file creation',
                        'impact': 'Information disclosure'
                    }
                ],
                'threat_intel': {
                    'exploit_count': 1,
                    'attack_types': ['information_disclosure'],
                    'targeted_systems': ['local_applications'],
                    'observed_campaigns': 0,
                    'threat_level': 'MEDIUM'
                }
            }
        }
    }
    
    # Get vulnerability data for component
    comp_vulns = vulnerability_data.get(component['name'], {}).get(component['version'], {})
    
    if not comp_vulns:
        return {
            'name': component['name'],
            'version': component['version'],
            'analysis': {
                'risk_score': 0.0,
                'vulnerabilities': [],
                'risk_factors': [],
                'threat_intel': None
            }
        }
    
    # Calculate risk score
    max_cvss = max([v['cvss_score'] for v in comp_vulns.get('vulnerabilities', [])], default=0.0)
    risk_factors = len(comp_vulns.get('risk_factors', []))
    threat_level = {
        'CRITICAL': 1.0,
        'HIGH': 0.8,
        'MEDIUM': 0.5,
        'LOW': 0.2
    }.get(comp_vulns.get('threat_intel', {}).get('threat_level', 'LOW'), 0.0)
    
    risk_score = (
        0.4 * (max_cvss / 10.0) +
        0.3 * min(risk_factors / 5.0, 1.0) +
        0.3 * threat_level
    )
    
    return {
        'name': component['name'],
        'version': component['version'],
        'analysis': {
            'risk_score': risk_score,
            'vulnerabilities': comp_vulns.get('vulnerabilities', []),
            'risk_factors': comp_vulns.get('risk_factors', []),
            'threat_intel': comp_vulns.get('threat_intel')
        }
    }

def analyze_sbom(sbom_data):
    """Analyze SBOM data"""
    print("\n=== SBOMAI Engine Analysis ===")
    print(f"Analyzing SBOM generated by {sbom_data['metadata']['tool']}")
    print(f"Timestamp: {sbom_data['metadata']['timestamp']}")
    
    results = {
        'components': [],
        'overall_risk_score': 0.0,
        'critical_components': [],
        'security_recommendations': []
    }
    
    # Analyze each component
    for component in sbom_data['components']:
        print(f"\n--- Analyzing {component['name']} {component['version']} ---")
        analysis = analyze_component(component)
        results['components'].append(analysis)
        
        # Track critical components
        if analysis['analysis']['risk_score'] > 0.7:
            results['critical_components'].append({
                'name': component['name'],
                'version': component['version'],
                'risk_score': analysis['analysis']['risk_score'],
                'critical_vulnerabilities': [
                    v for v in analysis['analysis']['vulnerabilities']
                    if v['severity'] == 'CRITICAL'
                ]
            })
    
    # Calculate overall risk score
    if results['components']:
        results['overall_risk_score'] = max(
            c['analysis']['risk_score'] for c in results['components']
        )
    
    # Generate recommendations
    for component in results['components']:
        if component['analysis']['vulnerabilities']:
            for vuln in component['analysis']['vulnerabilities']:
                results['security_recommendations'].append({
                    'component': f"{component['name']}:{component['version']}",
                    'severity': vuln['severity'],
                    'cve_id': vuln['cve_id'],
                    'recommendation': vuln['remediation']
                })
    
    return results

def main():
    """Run analysis on test SBOM"""
    # Load test SBOM
    with open('sbomai-engine/examples/test_sbom.json') as f:
        test_sbom = json.load(f)
    
    # Run analysis
    results = analyze_sbom(test_sbom)
    
    # Print results
    print("\n=== Analysis Results ===")
    print(f"\nOverall Risk Score: {results['overall_risk_score']:.2f}")
    
    print("\nCritical Components:")
    for comp in results['critical_components']:
        print(f"\n- {comp['name']} {comp['version']}")
        print(f"  Risk Score: {comp['risk_score']:.2f}")
        print("  Critical Vulnerabilities:")
        for vuln in comp['critical_vulnerabilities']:
            print(f"    - {vuln['cve_id']}: {vuln['description']}")
            print(f"      CVSS Score: {vuln['cvss_score']}")
            print(f"      Attack Vector: {vuln['cvss_vector']}")
            print(f"      Exploit Status: {vuln['exploit_status']}")
    
    print("\nDetailed Component Analysis:")
    for comp in results['components']:
        print(f"\n{comp['name']} {comp['version']}:")
        print(f"  Risk Score: {comp['analysis']['risk_score']:.2f}")
        
        if comp['analysis']['vulnerabilities']:
            print("  Vulnerabilities:")
            for vuln in comp['analysis']['vulnerabilities']:
                print(f"    - {vuln['cve_id']} ({vuln['severity']})")
                print(f"      Description: {vuln['description']}")
                print(f"      CVSS Score: {vuln['cvss_score']}")
                print(f"      Attack Complexity: {vuln['attack_complexity']}")
                print(f"      Exploit Maturity: {vuln['exploit_maturity']}")
        
        if comp['analysis']['threat_intel']:
            print("  Threat Intelligence:")
            ti = comp['analysis']['threat_intel']
            print(f"    - Known Exploits: {ti['exploit_count']}")
            print(f"    - Attack Types: {', '.join(ti['attack_types'])}")
            print(f"    - Targeted Systems: {', '.join(ti['targeted_systems'])}")
            print(f"    - Observed Campaigns: {ti['observed_campaigns']}")
            print(f"    - Threat Level: {ti['threat_level']}")
    
    print("\nSecurity Recommendations:")
    for i, rec in enumerate(results['security_recommendations'], 1):
        print(f"\n{i}. [{rec['severity']}] {rec['component']}")
        print(f"   CVE: {rec['cve_id']}")
        print(f"   Recommendation: {rec['recommendation']}")

if __name__ == '__main__':
    main()