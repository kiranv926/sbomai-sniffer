"""
Test suite for SBOMAI Engine dependency analysis.
"""

import unittest
import json
from datetime import datetime

# Test data
TEST_DEPENDENCY_CHAIN = {
    'name': 'root-app',
    'version': '1.0.0',
    'dependencies': [
        {
            'name': 'spring-boot-starter-web',
            'version': '2.6.1',
            'dependencies': [
                {
                    'name': 'spring-web',
                    'version': '5.3.13',
                    'vulnerabilities': [
                        {
                            'cve_id': 'CVE-2022-22965',
                            'severity': 'CRITICAL',
                            'cvss_score': 9.8,
                            'description': 'Spring4Shell RCE vulnerability'
                        }
                    ]
                },
                {
                    'name': 'tomcat-embed-core',
                    'version': '9.0.55',
                    'vulnerabilities': [
                        {
                            'cve_id': 'CVE-2022-23181',
                            'severity': 'HIGH',
                            'cvss_score': 8.2,
                            'description': 'HTTP Request Smuggling'
                        }
                    ]
                }
            ]
        },
        {
            'name': 'log4j-core',
            'version': '2.14.1',
            'vulnerabilities': [
                {
                    'cve_id': 'CVE-2021-44228',
                    'severity': 'CRITICAL',
                    'cvss_score': 10.0,
                    'description': 'Log4Shell RCE vulnerability'
                }
            ]
        }
    ]
}

class TestDependencyAnalysis(unittest.TestCase):
    """Test dependency analysis functionality"""
    
    def analyze_dependency_chain(self, dependency_data):
        """Analyze dependency chain for vulnerabilities"""
        results = {
            'vulnerable_components': [],
            'max_depth': 0,
            'total_components': 0,
            'risk_score': 0.0
        }
        
        def process_dependencies(deps, depth=0, parent=None):
            for dep in deps:
                if parent is None:  # Only count if it's not the root
                    results['total_components'] += 1
                results['max_depth'] = max(results['max_depth'], depth)
                
                # Check for vulnerabilities
                if 'vulnerabilities' in dep:
                    for vuln in dep['vulnerabilities']:
                        results['vulnerable_components'].append({
                            'component': f"{dep['name']}:{dep['version']}",
                            'vulnerability': vuln,
                            'depth': depth
                        })
                
                # Process nested dependencies
                if 'dependencies' in dep:
                    process_dependencies(dep['dependencies'], depth + 1, dep)
        
        process_dependencies([dependency_data])
        
        # Calculate risk score
        if results['vulnerable_components']:
            max_cvss = max(
                v['vulnerability']['cvss_score']
                for v in results['vulnerable_components']
            )
            vuln_density = len(results['vulnerable_components']) / results['total_components']
            results['risk_score'] = (0.7 * (max_cvss / 10.0)) + (0.3 * vuln_density)
        
        return results
    
    def find_critical_paths(self, dependency_data):
        """Find paths to critical vulnerabilities"""
        critical_paths = []
        
        def traverse_dependencies(deps, current_path=[]):
            for dep in deps:
                path = current_path + [f"{dep['name']}:{dep['version']}"]
                
                # Check for critical vulnerabilities
                if 'vulnerabilities' in dep:
                    for vuln in dep['vulnerabilities']:
                        if vuln['severity'] == 'CRITICAL':
                            critical_paths.append({
                                'path': path,
                                'vulnerability': vuln
                            })
                
                # Traverse nested dependencies
                if 'dependencies' in dep:
                    traverse_dependencies(dep['dependencies'], path)
        
        traverse_dependencies([dependency_data])
        return critical_paths
    
    def calculate_component_metrics(self, dependency_data):
        """Calculate component-level security metrics"""
        metrics = {
            'total_components': 0,
            'vulnerable_components': 0,
            'severity_counts': {
                'CRITICAL': 0,
                'HIGH': 0,
                'MEDIUM': 0,
                'LOW': 0
            },
            'max_cvss_score': 0.0,
            'avg_cvss_score': 0.0,
            'total_cvss_score': 0.0,
            'vulnerability_count': 0
        }
        
        def process_component(component):
            metrics['total_components'] += 1
            
            if 'vulnerabilities' in component:
                if component['vulnerabilities']:
                    metrics['vulnerable_components'] += 1
                
                for vuln in component['vulnerabilities']:
                    metrics['vulnerability_count'] += 1
                    metrics['severity_counts'][vuln['severity']] += 1
                    metrics['max_cvss_score'] = max(
                        metrics['max_cvss_score'],
                        vuln['cvss_score']
                    )
                    metrics['total_cvss_score'] += vuln['cvss_score']
            
            if 'dependencies' in component:
                for dep in component['dependencies']:
                    process_component(dep)
        
        process_component(dependency_data)
        
        if metrics['vulnerability_count'] > 0:
            metrics['avg_cvss_score'] = round(
                metrics['total_cvss_score'] / metrics['vulnerability_count'],
                1
            )
        
        return metrics
    
    def test_dependency_chain_analysis(self):
        """Test dependency chain analysis"""
        results = self.analyze_dependency_chain(TEST_DEPENDENCY_CHAIN)
        
        # Verify total components
        self.assertEqual(results['total_components'], 4)  # root + 3 dependencies
        
        # Verify vulnerable components
        self.assertEqual(len(results['vulnerable_components']), 3)
        
        # Verify max depth
        self.assertEqual(results['max_depth'], 1)  # One level of nested dependencies
        
        # Verify risk score is high due to critical vulnerabilities
        self.assertGreater(results['risk_score'], 0.8)
    
    def test_critical_path_detection(self):
        """Test detection of paths to critical vulnerabilities"""
        critical_paths = self.find_critical_paths(TEST_DEPENDENCY_CHAIN)
        
        # Should find two critical paths (Log4Shell and Spring4Shell)
        self.assertEqual(len(critical_paths), 2)
        
        # Verify Log4Shell path
        log4shell_path = next(
            p for p in critical_paths
            if p['vulnerability']['cve_id'] == 'CVE-2021-44228'
        )
        self.assertEqual(len(log4shell_path['path']), 2)  # root -> log4j
        
        # Verify Spring4Shell path
        spring4shell_path = next(
            p for p in critical_paths
            if p['vulnerability']['cve_id'] == 'CVE-2022-22965'
        )
        self.assertEqual(len(spring4shell_path['path']), 3)  # root -> starter -> spring-web
    
    def test_component_metrics(self):
        """Test component security metrics calculation"""
        metrics = self.calculate_component_metrics(TEST_DEPENDENCY_CHAIN)
        
        # Verify component counts
        self.assertEqual(metrics['total_components'], 4)
        self.assertEqual(metrics['vulnerable_components'], 3)
        
        # Verify severity counts
        self.assertEqual(metrics['severity_counts']['CRITICAL'], 2)  # Log4Shell + Spring4Shell
        self.assertEqual(metrics['severity_counts']['HIGH'], 1)     # Tomcat
        
        # Verify CVSS scores
        self.assertEqual(metrics['max_cvss_score'], 10.0)  # Log4Shell
        self.assertGreater(metrics['avg_cvss_score'], 9.0)  # Average of 10.0, 9.8, and 8.2

def print_test_results(result):
    """Print detailed test results"""
    print("\n=== SBOMAI Engine Dependency Analysis Test Results ===")
    
    # Print summary
    print(f"\nRan {result.testsRun} tests")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    # Print failures
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"\n{test.id()}")
            print(traceback)
    
    # Print errors
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"\n{test.id()}")
            print(traceback)

def main():
    """Run test suite"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDependencyAnalysis)
    
    # Run tests and capture results
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print detailed results
    print_test_results(result)

if __name__ == '__main__':
    main()