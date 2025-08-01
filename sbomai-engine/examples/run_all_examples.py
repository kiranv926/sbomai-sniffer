"""
Run all SBOMAI Engine examples.
"""

import json
from datetime import datetime
from pprint import pprint

# Import example data
from threat_analysis_examples import (
    log4j_component,
    spring_component,
    minimist_component,
    custom_component,
    shell_component
)
from comparison_analysis import (
    rce_payload,
    sql_payload,
    deserial_payload
)
from gnn_risk_propagation import (
    complex_dependency_chain
)

def analyze_component_security(component_data):
    """Analyze component security using multiple methods"""
    print(f"\n=== Analyzing {component_data['name']} {component_data['version']} ===")
    
    # Basic security metrics
    vulnerabilities = component_data.get('vulnerability_data', {}).get('vulnerabilities', [])
    max_cvss = max([v.get('cvss_score', 0.0) for v in vulnerabilities], default=0.0)
    
    print("\nBasic Security Metrics:")
    print(f"- CVSS Max Score: {max_cvss}")
    print(f"- Vulnerability Count: {len(vulnerabilities)}")
    
    # Code Analysis
    if 'source_code' in component_data:
        print("\nCode Analysis:")
        code_patterns = analyze_code_patterns(component_data['source_code'])
        for pattern in code_patterns:
            print(f"- {pattern['type']}: {pattern['description']}")
            print(f"  Line {pattern['line']}: {pattern['snippet']}")
    
    # Vulnerability Analysis
    if vulnerabilities:
        print("\nVulnerability Analysis:")
        for vuln in vulnerabilities:
            print(f"\n- {vuln.get('cve_id', 'Unknown CVE')}:")
            print(f"  Severity: {vuln.get('severity', 'Unknown')}")
            print(f"  Description: {vuln.get('description', 'No description')}")
            print(f"  Attack Vector: {vuln.get('attack_vector', 'Unknown')}")
            if 'exploit_maturity' in vuln:
                print(f"  Exploit Maturity: {vuln['exploit_maturity']}")

def analyze_code_patterns(source_code):
    """Analyze code for security patterns"""
    patterns = []
    
    # Common vulnerability patterns
    pattern_checks = [
        {
            'type': 'command_injection',
            'regex': r'Runtime\.getRuntime\(\)\.exec\(',
            'description': 'Potential command injection vulnerability'
        },
        {
            'type': 'sql_injection',
            'regex': r'executeQuery\(.*\+',
            'description': 'Potential SQL injection vulnerability'
        },
        {
            'type': 'path_traversal',
            'regex': r'new File\(.*\+',
            'description': 'Potential path traversal vulnerability'
        },
        {
            'type': 'unsafe_deserialization',
            'regex': r'ObjectInputStream.*readObject',
            'description': 'Unsafe deserialization'
        },
        {
            'type': 'xxe',
            'regex': r'DocumentBuilder.*parse',
            'description': 'Potential XXE vulnerability'
        }
    ]
    
    import re
    lines = source_code.split('\n')
    for i, line in enumerate(lines, 1):
        for check in pattern_checks:
            if re.search(check['regex'], line):
                patterns.append({
                    'type': check['type'],
                    'description': check['description'],
                    'line': i,
                    'snippet': line.strip()
                })
    
    return patterns

def analyze_dependency_chain(dependency_data):
    """Analyze dependency chain for security risks"""
    print(f"\n=== Analyzing Dependency Chain ===")
    
    def process_dependencies(deps, level=0):
        risks = []
        for dep in deps:
            # Check for vulnerabilities
            vulns = dep.get('vulnerabilities', [])
            if vulns:
                for vuln in vulns:
                    risks.append({
                        'component': dep['name'],
                        'version': dep['version'],
                        'level': level,
                        'vulnerability': vuln
                    })
            
            # Process nested dependencies
            if 'dependencies' in dep:
                risks.extend(process_dependencies(dep['dependencies'], level + 1))
        return risks
    
    # Analyze risks
    risks = process_dependencies([dependency_data])
    
    # Print results
    print("\nIdentified Risks:")
    for risk in risks:
        print(f"\nComponent: {risk['component']} {risk['version']}")
        print(f"Dependency Level: {risk['level']}")
        vuln = risk['vulnerability']
        print(f"- {vuln.get('cve_id', 'Unknown CVE')}:")
        print(f"  Severity: {vuln.get('severity', 'Unknown')}")
        print(f"  CVSS Score: {vuln.get('cvss_score', 'N/A')}")
        print(f"  Description: {vuln.get('description', 'No description')}")

def main():
    """Run all examples"""
    print("\n=== Running SBOMAI Engine Examples ===")
    
    # 1. Component Security Analysis
    print("\n=== Component Security Analysis ===")
    components = [
        log4j_component,
        spring_component,
        minimist_component,
        custom_component,
        shell_component
    ]
    
    for component in components:
        analyze_component_security(component)
    
    # 2. Advanced Vulnerability Analysis
    print("\n=== Advanced Vulnerability Analysis ===")
    payloads = [
        rce_payload,
        sql_payload,
        deserial_payload
    ]
    
    for payload in payloads:
        analyze_component_security(payload)
    
    # 3. Dependency Chain Analysis
    print("\n=== Dependency Chain Analysis ===")
    analyze_dependency_chain(complex_dependency_chain)

if __name__ == '__main__':
    main()