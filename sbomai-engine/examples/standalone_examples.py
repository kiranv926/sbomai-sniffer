"""
Standalone examples of SBOMAI Engine analysis capabilities.
"""

import json
import re
from datetime import datetime
from pprint import pprint

# Example 1: Log4j vulnerability
log4j_example = {
    'name': 'log4j-core',
    'version': '2.14.1',
    'description': 'Apache Log4j 2 Core',
    'source_code': '''
    public class Log4jExample {
        static Logger logger = LogManager.getLogger(Log4jExample.class);
        
        public void processRequest(String input) {
            logger.info("Received input: {}", input);  // Potential JNDI injection
            try {
                Context ctx = new InitialContext();
                ctx.lookup(input);  // Vulnerable JNDI lookup
            } catch (Exception e) {
                logger.error("Error processing request", e);
            }
        }
    }
    ''',
    'vulnerability_data': {
        'cve_id': 'CVE-2021-44228',
        'severity': 'CRITICAL',
        'cvss_score': 10.0,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H',
        'description': 'Remote code execution vulnerability in Log4j',
        'attack_vector': 'remote',
        'exploit_maturity': 'HIGH',
        'patch_status': 'AVAILABLE',
        'remediation': 'Upgrade to version 2.15.0 or later'
    }
}

# Example 2: Spring4Shell vulnerability
spring_example = {
    'name': 'spring-core',
    'version': '5.3.17',
    'description': 'Spring Framework Core',
    'source_code': '''
    @RequestMapping("/users")
    public class UserController {
        @PostMapping
        public String createUser(@ModelAttribute User user) {
            // Vulnerable to class property manipulation
            return userService.createUser(user);
        }
    }
    ''',
    'vulnerability_data': {
        'cve_id': 'CVE-2022-22965',
        'severity': 'CRITICAL',
        'cvss_score': 9.8,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
        'description': 'Spring Framework RCE via Data Binding',
        'attack_vector': 'remote',
        'exploit_maturity': 'HIGH',
        'patch_status': 'AVAILABLE',
        'remediation': 'Upgrade to version 5.3.18 or later'
    }
}

# Example 3: SQL Injection vulnerability
sql_example = {
    'name': 'custom-service',
    'version': '1.0.0',
    'description': 'Custom User Service',
    'source_code': '''
    @Service
    public class UserService {
        @Autowired
        private JdbcTemplate jdbc;
        
        public User findUser(String username) {
            // Vulnerable to SQL injection
            String sql = "SELECT * FROM users WHERE username = '" + username + "'";
            return jdbc.queryForObject(sql, User.class);
        }
    }
    ''',
    'vulnerability_data': {
        'cve_id': None,
        'severity': 'HIGH',
        'cvss_score': 8.5,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H',
        'description': 'SQL Injection in User Service',
        'attack_vector': 'remote',
        'exploit_maturity': 'MEDIUM',
        'patch_status': 'NOT_AVAILABLE',
        'remediation': 'Use parameterized queries'
    }
}

def analyze_code_patterns(source_code):
    """Analyze code for security patterns"""
    patterns = []
    
    # Define vulnerability patterns
    vulnerability_patterns = [
        {
            'type': 'sql_injection',
            'regex': r'.*\+.*\bWHERE\b.*=.*',
            'severity': 'HIGH',
            'description': 'String concatenation in SQL query'
        },
        {
            'type': 'jndi_injection',
            'regex': r'ctx\.lookup\(.*\)',
            'severity': 'CRITICAL',
            'description': 'Unsafe JNDI lookup'
        },
        {
            'type': 'unsafe_deserialization',
            'regex': r'@ModelAttribute',
            'severity': 'HIGH',
            'description': 'Unsafe model binding'
        },
        {
            'type': 'logging_injection',
            'regex': r'logger\.(info|error|debug|warn)\(.*\{.*\}.*\)',
            'severity': 'MEDIUM',
            'description': 'Potential log injection'
        }
    ]
    
    # Check each line for patterns
    lines = source_code.split('\n')
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
            
        for pattern in vulnerability_patterns:
            if re.search(pattern['regex'], line):
                patterns.append({
                    'type': pattern['type'],
                    'severity': pattern['severity'],
                    'description': pattern['description'],
                    'line': i,
                    'code': line
                })
    
    return patterns

def calculate_risk_score(component):
    """Calculate risk score for a component"""
    vuln_data = component.get('vulnerability_data', {})
    
    # Base score from CVSS
    base_score = vuln_data.get('cvss_score', 0.0) / 10.0
    
    # Exploit maturity factor
    exploit_factors = {
        'HIGH': 1.0,
        'MEDIUM': 0.7,
        'LOW': 0.4,
        None: 0.0
    }
    exploit_score = exploit_factors.get(vuln_data.get('exploit_maturity'))
    
    # Code patterns factor
    if 'source_code' in component:
        patterns = analyze_code_patterns(component['source_code'])
        pattern_score = min(len(patterns) / 5.0, 1.0)
    else:
        pattern_score = 0.0
    
    # Patch status factor
    patch_factors = {
        'NOT_AVAILABLE': 1.0,
        'IN_PROGRESS': 0.7,
        'AVAILABLE': 0.4,
        None: 0.5
    }
    patch_score = patch_factors.get(vuln_data.get('patch_status'))
    
    # Calculate weighted score
    weights = {
        'base': 0.4,
        'exploit': 0.3,
        'patterns': 0.2,
        'patch': 0.1
    }
    
    risk_score = (
        weights['base'] * base_score +
        weights['exploit'] * exploit_score +
        weights['patterns'] * pattern_score +
        weights['patch'] * patch_score
    )
    
    return min(risk_score, 1.0)

def analyze_component(component):
    """Perform comprehensive component analysis"""
    print(f"\n=== Analyzing {component['name']} {component['version']} ===")
    
    # 1. Code Analysis
    if 'source_code' in component:
        print("\nCode Analysis:")
        patterns = analyze_code_patterns(component['source_code'])
        for pattern in patterns:
            print(f"\n- {pattern['type']} ({pattern['severity']})")
            print(f"  Description: {pattern['description']}")
            print(f"  Line {pattern['line']}: {pattern['code']}")
    
    # 2. Vulnerability Analysis
    if 'vulnerability_data' in component:
        vuln = component['vulnerability_data']
        print("\nVulnerability Analysis:")
        print(f"- CVE: {vuln.get('cve_id', 'N/A')}")
        print(f"- Severity: {vuln['severity']}")
        print(f"- CVSS Score: {vuln['cvss_score']}")
        print(f"- CVSS Vector: {vuln['cvss_vector']}")
        print(f"- Description: {vuln['description']}")
        print(f"- Attack Vector: {vuln['attack_vector']}")
        print(f"- Exploit Maturity: {vuln.get('exploit_maturity', 'Unknown')}")
        print(f"- Patch Status: {vuln.get('patch_status', 'Unknown')}")
    
    # 3. Risk Assessment
    risk_score = calculate_risk_score(component)
    risk_level = 'CRITICAL' if risk_score > 0.8 else 'HIGH' if risk_score > 0.6 else 'MEDIUM' if risk_score > 0.4 else 'LOW'
    
    print("\nRisk Assessment:")
    print(f"- Risk Score: {risk_score:.2f}")
    print(f"- Risk Level: {risk_level}")
    
    # 4. Remediation
    if 'vulnerability_data' in component and 'remediation' in component['vulnerability_data']:
        print("\nRemediation:")
        print(f"- {component['vulnerability_data']['remediation']}")

def main():
    """Run all examples"""
    print("\n=== SBOMAI Engine Analysis Examples ===")
    
    examples = [
        log4j_example,
        spring_example,
        sql_example
    ]
    
    for example in examples:
        analyze_component(example)
        print("\n" + "="*80)

if __name__ == '__main__':
    main()