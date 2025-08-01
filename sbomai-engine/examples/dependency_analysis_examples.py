"""
Examples of dependency chain analysis using SBOMAI Engine.
"""

import json
from datetime import datetime
from pprint import pprint

from sbomai_ai.models.threat_intelligence import ThreatContextEmbedding
from sbomai_ai.models.threat_patterns import ExploitPatternDetector, VulnerabilityCorrelation
from sbomai_ai.models.exploit_prediction import ExploitPredictor

# Initialize analyzers
threat_analyzer = ThreatContextEmbedding()
pattern_detector = ExploitPatternDetector()
vuln_correlator = VulnerabilityCorrelation()
exploit_predictor = ExploitPredictor()

# Example 1: Spring Boot Application with Transitive Dependencies
spring_boot_example = {
    'name': 'com.example:web-app',
    'version': '1.0.0',
    'description': 'Spring Boot web application',
    'dependencies': [
        {
            'name': 'org.springframework.boot:spring-boot-starter-web',
            'version': '2.6.1',
            'direct': True,
            'dependencies': [
                {
                    'name': 'org.springframework:spring-web',
                    'version': '5.3.13',
                    'vulnerabilities': [
                        {
                            'cve_id': 'CVE-2022-22965',
                            'severity': 'CRITICAL',
                            'description': 'Spring4Shell RCE vulnerability'
                        }
                    ]
                },
                {
                    'name': 'org.apache.tomcat.embed:tomcat-embed-core',
                    'version': '9.0.55',
                    'vulnerabilities': [
                        {
                            'cve_id': 'CVE-2022-23181',
                            'severity': 'HIGH',
                            'description': 'HTTP Request Smuggling'
                        }
                    ]
                }
            ]
        },
        {
            'name': 'com.fasterxml.jackson.core:jackson-databind',
            'version': '2.13.0',
            'direct': True,
            'vulnerabilities': [
                {
                    'cve_id': 'CVE-2022-42003',
                    'severity': 'HIGH',
                    'description': 'Denial of Service'
                }
            ]
        }
    ]
}

# Example 2: Node.js Application with npm Dependencies
nodejs_example = {
    'name': 'my-node-app',
    'version': '1.0.0',
    'description': 'Node.js web application',
    'dependencies': [
        {
            'name': 'express',
            'version': '4.17.1',
            'direct': True,
            'dependencies': [
                {
                    'name': 'body-parser',
                    'version': '1.19.0',
                    'vulnerabilities': []
                },
                {
                    'name': 'debug',
                    'version': '2.6.9',
                    'vulnerabilities': [
                        {
                            'cve_id': 'CVE-2017-16137',
                            'severity': 'MEDIUM',
                            'description': 'Regular Expression Denial of Service'
                        }
                    ]
                }
            ]
        },
        {
            'name': 'lodash',
            'version': '4.17.15',
            'direct': True,
            'vulnerabilities': [
                {
                    'cve_id': 'CVE-2020-8203',
                    'severity': 'HIGH',
                    'description': 'Prototype Pollution'
                }
            ]
        },
        {
            'name': 'axios',
            'version': '0.21.1',
            'direct': True,
            'vulnerabilities': [
                {
                    'cve_id': 'CVE-2021-3749',
                    'severity': 'HIGH',
                    'description': 'Server-Side Request Forgery'
                }
            ]
        }
    ]
}

# Example 3: Python Application with Complex Dependencies
python_example = {
    'name': 'my-python-app',
    'version': '1.0.0',
    'description': 'Python web application',
    'dependencies': [
        {
            'name': 'django',
            'version': '3.2.10',
            'direct': True,
            'dependencies': [
                {
                    'name': 'sqlparse',
                    'version': '0.4.1',
                    'vulnerabilities': [
                        {
                            'cve_id': 'CVE-2021-32839',
                            'severity': 'MEDIUM',
                            'description': 'SQL Injection via crafted SQL statements'
                        }
                    ]
                }
            ]
        },
        {
            'name': 'pillow',
            'version': '8.3.2',
            'direct': True,
            'vulnerabilities': [
                {
                    'cve_id': 'CVE-2021-23437',
                    'severity': 'HIGH',
                    'description': 'Buffer Overflow'
                }
            ]
        },
        {
            'name': 'requests',
            'version': '2.26.0',
            'direct': True,
            'dependencies': [
                {
                    'name': 'urllib3',
                    'version': '1.26.7',
                    'vulnerabilities': [
                        {
                            'cve_id': 'CVE-2021-33503',
                            'severity': 'MEDIUM',
                            'description': 'CRLF injection'
                        }
                    ]
                }
            ]
        }
    ]
}

def analyze_dependencies(name, data):
    """Analyze dependency chain for vulnerabilities"""
    print(f"\n=== Analyzing Dependencies for {name} ===")
    
    # 1. Build Dependency Graph
    print("\nDependency Graph Analysis:")
    graph = build_dependency_graph(data['dependencies'])
    pprint({
        'total_dependencies': len(graph['nodes']),
        'direct_dependencies': len([n for n in graph['nodes'] if n['direct']]),
        'vulnerable_dependencies': len([n for n in graph['nodes'] if n['vulnerabilities']])
    })
    
    # 2. Vulnerability Impact Analysis
    print("\nVulnerability Impact Analysis:")
    impact = analyze_vulnerability_impact(graph)
    pprint({
        'critical_components': impact['critical_components'],
        'risk_paths': impact['risk_paths'][:3],
        'overall_risk_score': impact['risk_score']
    })
    
    # 3. Update Recommendations
    print("\nUpdate Recommendations:")
    recommendations = generate_update_recommendations(graph)
    for rec in recommendations[:5]:
        print(f"- {rec['component']}: {rec['current_version']} → {rec['target_version']}")
        print(f"  Impact: {rec['impact']}")
        print(f"  Risk: {rec['risk_level']}")
    
    # 4. Security Metrics
    print("\nSecurity Metrics:")
    metrics = calculate_security_metrics(graph)
    pprint({
        'vulnerability_density': metrics['vulnerability_density'],
        'mean_time_to_update': metrics['mean_time_to_update'],
        'dependency_health_score': metrics['health_score']
    })

def build_dependency_graph(dependencies, direct=True, depth=0):
    """Recursively build dependency graph"""
    nodes = []
    edges = []
    
    for dep in dependencies:
        # Add node
        node = {
            'name': dep['name'],
            'version': dep['version'],
            'direct': direct,
            'depth': depth,
            'vulnerabilities': dep.get('vulnerabilities', [])
        }
        nodes.append(node)
        
        # Process child dependencies
        if 'dependencies' in dep:
            child_graph = build_dependency_graph(
                dep['dependencies'],
                direct=False,
                depth=depth + 1
            )
            nodes.extend(child_graph['nodes'])
            edges.extend(child_graph['edges'])
            
            # Add edges to children
            for child in dep['dependencies']:
                edges.append({
                    'from': dep['name'],
                    'to': child['name'],
                    'type': 'depends_on'
                })
    
    return {'nodes': nodes, 'edges': edges}

def analyze_vulnerability_impact(graph):
    """Analyze vulnerability impact in dependency chain"""
    # Find critical components
    critical_components = []
    for node in graph['nodes']:
        if any(v['severity'] in ['CRITICAL', 'HIGH'] for v in node['vulnerabilities']):
            critical_components.append({
                'name': node['name'],
                'version': node['version'],
                'vulnerabilities': node['vulnerabilities'],
                'dependents': count_dependents(node['name'], graph['edges'])
            })
    
    # Find risk paths
    risk_paths = find_risk_paths(graph)
    
    # Calculate overall risk score
    risk_score = calculate_risk_score(graph)
    
    return {
        'critical_components': critical_components,
        'risk_paths': risk_paths,
        'risk_score': risk_score
    }

def generate_update_recommendations(graph):
    """Generate prioritized update recommendations"""
    recommendations = []
    
    for node in graph['nodes']:
        if node['vulnerabilities']:
            # Get latest safe version
            latest_version = get_latest_safe_version(node['name'])
            
            # Calculate update impact
            impact = calculate_update_impact(node, graph)
            
            recommendations.append({
                'component': node['name'],
                'current_version': node['version'],
                'target_version': latest_version,
                'vulnerabilities': len(node['vulnerabilities']),
                'impact': impact['description'],
                'risk_level': impact['risk_level'],
                'priority': calculate_update_priority(node, impact)
            })
    
    return sorted(recommendations, key=lambda x: x['priority'], reverse=True)

def calculate_security_metrics(graph):
    """Calculate security metrics for the dependency chain"""
    total_deps = len(graph['nodes'])
    total_vulns = sum(len(n['vulnerabilities']) for n in graph['nodes'])
    
    return {
        'vulnerability_density': total_vulns / total_deps if total_deps > 0 else 0,
        'mean_time_to_update': calculate_mean_time_to_update(graph),
        'health_score': calculate_health_score(graph)
    }

def main():
    """Run analysis on all examples"""
    examples = [
        ('Spring Boot Application', spring_boot_example),
        ('Node.js Application', nodejs_example),
        ('Python Application', python_example)
    ]
    
    for name, data in examples:
        analyze_dependencies(name, data)
        print("\n" + "="*80)

if __name__ == '__main__':
    main()