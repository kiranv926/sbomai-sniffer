"""
Compare analysis results with and without enhanced threat intelligence.
"""

import json
from datetime import datetime
from pprint import pprint

from sbomai_ai.models.vulnerability_intelligence import VulnerabilityIntelligence
from sbomai_ai.models.threat_intelligence import ThreatContextEmbedding
from sbomai_ai.models.threat_patterns import ExploitPatternDetector, VulnerabilityCorrelation
from sbomai_ai.models.exploit_prediction import ExploitPredictor

def analyze_basic(component_data):
    """Basic vulnerability analysis without enhanced threat intelligence"""
    analyzer = VulnerabilityIntelligence()
    
    if 'vulnerability_data' in component_data:
        vuln_data = component_data['vulnerability_data']
        result = analyzer.analyze_vulnerability(vuln_data['cve_id'])
        return result
    return None

def analyze_enhanced(component_data):
    """Enhanced analysis with threat intelligence"""
    threat_analyzer = ThreatContextEmbedding()
    pattern_detector = ExploitPatternDetector()
    exploit_predictor = ExploitPredictor()
    
    results = {
        'threat_context': threat_analyzer.embed_component(component_data),
        'patterns': pattern_detector.analyze_component(component_data)
    }
    
    if 'vulnerability_data' in component_data:
        results['exploit_prediction'] = exploit_predictor.predict_exploit_likelihood(
            component_data['vulnerability_data']
        )
    
    return results

def compare_analysis(component_data):
    """Compare basic and enhanced analysis"""
    print(f"\n=== Analyzing {component_data['name']} {component_data['version']} ===")
    
    print("\n--- Basic Analysis ---")
    basic_result = analyze_basic(component_data)
    pprint(basic_result)
    
    print("\n--- Enhanced Analysis ---")
    enhanced_result = analyze_enhanced(component_data)
    pprint(enhanced_result)
    
    print("\n--- Key Differences ---")
    
    if basic_result and enhanced_result.get('exploit_prediction'):
        print("\nRisk Assessment:")
        print(f"Basic: {basic_result['criticality_score']:.2f}")
        print(f"Enhanced: {enhanced_result['exploit_prediction']['exploit_probability']:.2f}")
        
        print("\nExplanation Detail:")
        print("Basic:", len(basic_result.get('risk_explanation', {}).get('contributing_factors', [])), "factors")
        print("Enhanced:", len(enhanced_result['patterns']['risk_factors']), "factors")
        
        print("\nAdditional Enhanced Features:")
        print("- Code Pattern Analysis:", bool(enhanced_result['patterns'].get('code_analysis')))
        print("- Anomaly Detection:", bool(enhanced_result['patterns'].get('anomaly_score')))
        print("- Model Confidence:", enhanced_result['exploit_prediction']['confidence_score'])

# Example payload: Remote Code Execution vulnerability
rce_payload = {
    'name': 'com.example:remote-executor',
    'version': '1.0.0',
    'description': 'Remote command execution service',
    'source_code': '''
    @RestController
    public class CommandController {
        @PostMapping("/execute")
        public String executeCommand(@RequestParam String cmd) {
            try {
                // Critical: Remote Code Execution vulnerability
                Process p = Runtime.getRuntime().exec(cmd);
                BufferedReader reader = new BufferedReader(
                    new InputStreamReader(p.getInputStream())
                );
                return reader.lines().collect(Collectors.joining("\\n"));
            } catch (Exception e) {
                return "Error: " + e.getMessage();
            }
        }
    }
    ''',
    'metadata': {
        'ecosystem': 'maven',
        'latest_version': '1.0.0',
        'usage_count': 100,
        'stars': 5
    },
    'vulnerability_data': {
        'cve_id': 'CVE-2023-12345',
        'cvss_score': 9.8,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
        'description': 'Remote code execution vulnerability in command execution endpoint allows attackers to execute arbitrary system commands.',
        'attack_vector': 'remote',
        'requires_authentication': False,
        'has_proof_of_concept': True,
        'has_known_exploit': False,
        'affects_latest_version': True,
        'proof_of_concept': '; cat /etc/passwd #'
    }
}

# Example payload: SQL Injection with encryption bypass
sql_payload = {
    'name': 'com.example:user-auth',
    'version': '2.0.0',
    'description': 'User authentication service',
    'source_code': '''
    @Service
    public class AuthService {
        @Autowired
        private JdbcTemplate jdbc;
        
        public User authenticate(String username, String password) {
            // Multiple vulnerabilities:
            // 1. SQL Injection
            // 2. Weak encryption
            // 3. Hardcoded key
            String key = "1234567890abcdef";
            String encPassword = encrypt(password, key);
            
            // Critical: SQL Injection vulnerability
            String sql = "SELECT * FROM users WHERE username = '" + username + 
                        "' AND password = '" + encPassword + "'";
            return jdbc.queryForObject(sql, User.class);
        }
        
        private String encrypt(String data, String key) {
            // Weak encryption implementation
            return Base64.encode(data.getBytes());
        }
    }
    ''',
    'metadata': {
        'ecosystem': 'maven',
        'latest_version': '2.0.0',
        'usage_count': 500,
        'stars': 25
    },
    'vulnerability_data': {
        'cve_id': 'CVE-2023-67890',
        'cvss_score': 8.5,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L',
        'description': 'SQL injection vulnerability in authentication service combined with weak encryption allows attackers to bypass authentication.',
        'attack_vector': 'remote',
        'requires_authentication': False,
        'has_proof_of_concept': True,
        'has_known_exploit': True,
        'affects_latest_version': True,
        'proof_of_concept': "' OR '1'='1' --"
    }
}

# Example payload: Deserialization vulnerability
deserial_payload = {
    'name': 'com.example:data-processor',
    'version': '3.0.0',
    'description': 'Data processing service',
    'source_code': '''
    @Service
    public class DataProcessor {
        public Object processData(byte[] data) {
            try {
                // Critical: Unsafe deserialization
                ByteArrayInputStream bis = new ByteArrayInputStream(data);
                ObjectInputStream ois = new ObjectInputStream(bis);
                return ois.readObject();  // Vulnerable to deserialization attacks
            } catch (Exception e) {
                throw new RuntimeException("Error processing data", e);
            }
        }
        
        @PostMapping("/process")
        public ResponseEntity<?> handleData(@RequestBody byte[] data) {
            return ResponseEntity.ok(processData(data));
        }
    }
    ''',
    'metadata': {
        'ecosystem': 'maven',
        'latest_version': '3.0.0',
        'usage_count': 300,
        'stars': 15
    },
    'vulnerability_data': {
        'cve_id': 'CVE-2023-24680',
        'cvss_score': 8.1,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L',
        'description': 'Unsafe deserialization of user-supplied data can lead to remote code execution.',
        'attack_vector': 'remote',
        'requires_authentication': False,
        'has_proof_of_concept': True,
        'has_known_exploit': False,
        'affects_latest_version': True,
        'proof_of_concept': '''
            {
                "rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAABdwQAAAABc3IAOmNvbS5zdW4ub3JnLmFwYWNoZS54YWxhbi5pbnRlcm5hbC54c2x0Yy50cmF4LlRlbXBsYXRlc0ltcGwJV0/BbqyrMwMACEkADV9pbmRlbnROdW1iZXJJAA5fdHJhbnNsZXRJbmRleFsAC19ieXRlY29kZXN0AANbW0JbAAZfY2xhc3N0ABJbTGphdmEvbGFuZy9DbGFzcztMAAVfbmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO0wAEV9vdXRwdXRQcm9wZXJ0aWVzdAAWTGphdmEvdXRpbC9Qcm9wZXJ0aWVzO0wACl9hdXhDbGFzc2VzdAAfTGphdmEvbGFuZy9DbGFzcy9BdXhDbGFzc0xvYWRlcjtMABNfYXV4Q2xhc3NBY2Nlc3NGbGFndAASTGphdmEvbGFuZy9TdHJpbmc7eHIANmNvbS5zdW4ub3JnLmFwYWNoZS54YWxhbi5pbnRlcm5hbC54c2x0Yy50cmF4LlRlbXBsYXRlc5hBQqZXqaCrAwAGSQAOX2luZGVudE51bWJlckkADl90cmFuc2xldEluZGV4WwALX2J5dGVjb2Rlc3QAA1tbQlsABl9jbGFzc3QAEltMamF2YS9sYW5nL0NsYXNzO0wABV9uYW1ldAASTGphdmEvbGFuZy9TdHJpbmc7TAAQbmFtZXNwYWNlSGFuZGxlcnQAG0xqYXZhL3htbC9uYW1lc3BhY2UvUVJlc3VsdDt4cAAAAAAAAAAAAAB1cgADW1tCS/tW7CJoa0wCAAB4cAAAAAJ1cgACW0Ks8xf4BghU4AIAAHhwAAAGxyv+ur4AAAAyADkKAAMAIgcANwcAJQcAJgEAEHNlcmlhbFZlcnNpb25VSUQBAAFKAQANQ29uc3RhbnRWYWx1ZQWtIJPzkd3vPgEABjxpbml0PgEAAygpVgEABENvZGUBAA9MaW5lTnVtYmVyVGFibGUBABJMb2NhbFZhcmlhYmxlVGFibGUBAAR0aGlzAQATU3R1YlRyYW5zbGV0UGF5bG9hZAEADElubmVyQ2xhc3NlcwEANUx5c29zZXJpYWwvcGF5bG9hZHMvdXRpbC9HYWRnZXRzJFN0dWJUcmFuc2xldFBheWxvYWQ7AQAJdHJhbnNmb3JtAQByKExjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvRE9NO1tMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOylWAQAIZG9jdW1lbnQBAC1MY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL0RPTTsBAAhoYW5kbGVycwEAQltMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOwEACkV4Y2VwdGlvbnMHACcBAKYoTGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ET007TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvZHRtL0RUTUF4aXNJdGVyYXRvcjtMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOylWAQAIaXRlcmF0b3IBADVMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9kdG0vRFRNQXhpc0l0ZXJhdG9yOwEAB2hhbmRsZXIBAEFMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOwEAClNvdXJjZUZpbGUBAAxHYWRnZXRzLmphdmEMAAoACwcAKAEAM3lzb3NlcmlhbC9wYXlsb2Fkcy91dGlsL0dhZGdldHMkU3R1YlRyYW5zbGV0UGF5bG9hZAEAQGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ydW50aW1lL0Fic3RyYWN0VHJhbnNsZXQBABRqYXZhL2lvL1NlcmlhbGl6YWJsZQEAOWNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9UcmFuc2xldEV4Y2VwdGlvbgEAH3lzb3NlcmlhbC9wYXlsb2Fkcy91dGlsL0dhZGdldHMBAAg8Y2xpbml0PgEAEWphdmEvbGFuZy9SdW50aW1lBwAqAQAKZ2V0UnVudGltZQEAFSgpTGphdmEvbGFuZy9SdW50aW1lOwwALAAtCgArAC4BAARjYWxjDAAwAAsKACsAMQEABENvZGUBABJMb2NhbFZhcmlhYmxlVGFibGUBAA9MaW5lTnVtYmVyVGFibGUBAApTb3VyY2VGaWxlAQAMR2FkZ2V0cy5qYXZhAQAXU3R1YlRyYW5zbGV0UGF5bG9hZC5qYXZhDAAKAAsHADIBADN5c29zZXJpYWwvcGF5bG9hZHMvdXRpbC9HYWRnZXRzJFN0dWJUcmFuc2xldFBheWxvYWQBAEBjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvcnVudGltZS9BYnN0cmFjdFRyYW5zbGV0AQAUamF2YS9pby9TZXJpYWxpemFibGUBADljb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvVHJhbnNsZXRFeGNlcHRpb24BAB95c29zZXJpYWwvcGF5bG9hZHMvdXRpbC9HYWRnZXRzAQAIPGNsaW5pdD4BABFqYXZhL2xhbmcvUnVudGltZQcAKgEACmdldFJ1bnRpbWUBABUoKUxqYXZhL2xhbmcvUnVudGltZTsMAC0ALgoAKwAuAQAEY2FsYwwAMAAvCgArADEBAA9MaW5lTnVtYmVyVGFibGUBAApTb3VyY2VGaWxlAQAMR2FkZ2V0cy5qYXZhDAAKAAsBABN5c29zZXJpYWwvR2VuZXJhdGVkAQAUamF2YS9pby9TZXJpYWxpemFibGUBADljb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvVHJhbnNsZXRFeGNlcHRpb24BAB95c29zZXJpYWwvcGF5bG9hZHMvdXRpbC9HYWRnZXRzACEAAgADAAEABAABABoABQAGAAEABwAAAAIACAAEAAEACgALAAEADAAAAC8AAQABAAAABSq3AAGxAAAAAgANAAAABgABAAAALwAOAAAADAABAAAABQAPABIAAAABABMAFAABAAwAAAAvAAEAAQAAAAUqtw
        '''
    }
}

def main():
    """Run comparison analysis on example payloads"""
    payloads = [
        rce_payload,
        sql_payload,
        deserial_payload
    ]
    
    for payload in payloads:
        compare_analysis(payload)

if __name__ == '__main__':
    main()