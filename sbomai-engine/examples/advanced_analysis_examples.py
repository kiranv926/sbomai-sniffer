"""
Advanced examples of SBOMAI Engine's threat intelligence capabilities.
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

# Example 1: Path Traversal Vulnerability
path_traversal_example = {
    'name': 'com.example:file-service',
    'version': '1.1.0',
    'description': 'File management service',
    'source_code': '''
    @RestController
    @RequestMapping("/files")
    public class FileController {
        private static final String BASE_DIR = "/var/data/files/";
        
        @GetMapping("/{path}")
        public ResponseEntity<Resource> getFile(@PathVariable String path) {
            // Vulnerable to path traversal
            File file = new File(BASE_DIR + path);
            
            if (file.exists()) {
                return ResponseEntity.ok()
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .body(new FileSystemResource(file));
            }
            return ResponseEntity.notFound().build();
        }
        
        @PostMapping("/upload/{path}")
        public ResponseEntity<String> uploadFile(
            @PathVariable String path,
            @RequestParam("file") MultipartFile file
        ) {
            // Multiple vulnerabilities:
            // 1. Path traversal
            // 2. No file type validation
            // 3. No size limits
            File dest = new File(BASE_DIR + path);
            file.transferTo(dest);
            return ResponseEntity.ok("File uploaded");
        }
    }
    ''',
    'metadata': {
        'ecosystem': 'maven',
        'latest_version': '1.1.0',
        'usage_count': 150,
        'stars': 8
    },
    'vulnerability_data': {
        'cvss_score': 7.5,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N',
        'description': 'Path traversal vulnerability allows reading arbitrary files',
        'attack_vector': 'remote',
        'requires_authentication': False,
        'has_proof_of_concept': True,
        'proof_of_concept': '../../../etc/passwd'
    }
}

# Example 2: XXE Vulnerability
xxe_example = {
    'name': 'com.example:xml-processor',
    'version': '2.0.1',
    'description': 'XML processing service',
    'source_code': '''
    @Service
    public class XmlProcessor {
        public Document parseXml(String xmlInput) {
            try {
                // Vulnerable to XXE
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder = factory.newDocumentBuilder();
                return builder.parse(new InputSource(new StringReader(xmlInput)));
            } catch (Exception e) {
                throw new RuntimeException("Error parsing XML", e);
            }
        }
        
        @PostMapping("/process")
        public ResponseEntity<String> processXml(@RequestBody String xml) {
            Document doc = parseXml(xml);
            // Process the document
            return ResponseEntity.ok("Processed");
        }
    }
    ''',
    'metadata': {
        'ecosystem': 'maven',
        'latest_version': '2.0.1',
        'usage_count': 300,
        'stars': 15
    },
    'vulnerability_data': {
        'cvss_score': 8.8,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
        'description': 'XML External Entity (XXE) vulnerability allows reading local files and SSRF',
        'attack_vector': 'remote',
        'requires_authentication': False,
        'has_proof_of_concept': True,
        'proof_of_concept': '''
            <?xml version="1.0" encoding="ISO-8859-1"?>
            <!DOCTYPE foo [
                <!ELEMENT foo ANY >
                <!ENTITY xxe SYSTEM "file:///etc/passwd" >
            ]>
            <foo>&xxe;</foo>
        '''
    }
}

# Example 3: Prototype Pollution in JavaScript
proto_pollution_example = {
    'name': 'lodash',
    'version': '4.17.15',
    'description': 'Modern JavaScript utility library',
    'source_code': '''
    function merge(object, sources) {
        const isObject = (obj) => obj && typeof obj === 'object';
        
        function customizer(objValue, srcValue) {
            return isObject(srcValue) ? merge(objValue, srcValue) : srcValue;
        }
        
        if (!isObject(object)) {
            return object;
        }
        
        for (const source of sources) {
            if (isObject(source)) {
                for (const key in source) {
                    // Vulnerable to prototype pollution
                    const objValue = object[key];
                    const srcValue = source[key];
                    
                    object[key] = customizer(objValue, srcValue);
                }
            }
        }
        
        return object;
    }
    ''',
    'metadata': {
        'ecosystem': 'npm',
        'latest_version': '4.17.21',
        'usage_count': 1500000,
        'stars': 25600
    },
    'vulnerability_data': {
        'cve_id': 'CVE-2020-8203',
        'cvss_score': 7.4,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N',
        'description': 'Prototype pollution in lodash allows attackers to modify object properties',
        'attack_vector': 'package',
        'requires_authentication': False,
        'has_proof_of_concept': True,
        'proof_of_concept': '''
            const payload = {
                "__proto__": {
                    "polluted": "yes"
                }
            };
            merge({}, [payload]);
            console.log({}.polluted); // Outputs: "yes"
        '''
    }
}

# Example 4: Server-Side Template Injection
ssti_example = {
    'name': 'com.example:template-engine',
    'version': '1.0.0',
    'description': 'Custom template engine',
    'source_code': '''
    @Service
    public class TemplateService {
        private final Velocity velocity;
        
        @PostMapping("/render")
        public String renderTemplate(@RequestParam String template) {
            try {
                // Vulnerable to SSTI
                VelocityContext context = new VelocityContext();
                context.put("math", Math.class);
                context.put("runtime", Runtime.class);
                
                StringWriter writer = new StringWriter();
                velocity.evaluate(context, writer, "template", template);
                return writer.toString();
            } catch (Exception e) {
                return "Error: " + e.getMessage();
            }
        }
    }
    ''',
    'metadata': {
        'ecosystem': 'maven',
        'latest_version': '1.0.0',
        'usage_count': 50,
        'stars': 3
    },
    'vulnerability_data': {
        'cvss_score': 9.8,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
        'description': 'Server-Side Template Injection allows remote code execution',
        'attack_vector': 'remote',
        'requires_authentication': False,
        'has_proof_of_concept': True,
        'proof_of_concept': '#set($runtime = $runtime.getRuntime())\n#set($cmd = $runtime.exec("id"))'
    }
}

# Example 5: GraphQL Injection
graphql_example = {
    'name': 'com.example:graphql-api',
    'version': '1.2.0',
    'description': 'GraphQL API service',
    'source_code': '''
    @Controller
    public class GraphQLController {
        @Autowired
        private DataSource dataSource;
        
        public List<User> getUsers(String filter) {
            // Vulnerable to SQL injection via GraphQL
            String sql = "SELECT * FROM users WHERE " + filter;
            
            try (Connection conn = dataSource.getConnection();
                 Statement stmt = conn.createStatement()) {
                ResultSet rs = stmt.executeQuery(sql);
                return convertToUsers(rs);
            }
        }
        
        @QueryMapping
        public List<User> searchUsers(@Argument String filter) {
            // Multiple vulnerabilities:
            // 1. SQL injection
            // 2. No depth limiting
            // 3. No rate limiting
            return getUsers(filter);
        }
    }
    ''',
    'metadata': {
        'ecosystem': 'maven',
        'latest_version': '1.2.0',
        'usage_count': 200,
        'stars': 12
    },
    'vulnerability_data': {
        'cvss_score': 8.5,
        'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H',
        'description': 'GraphQL API vulnerable to SQL injection and resource exhaustion',
        'attack_vector': 'remote',
        'requires_authentication': True,
        'has_proof_of_concept': True,
        'proof_of_concept': '''
            query {
                searchUsers(filter: "1=1 UNION SELECT username,password FROM users--") {
                    id
                    username
                    email
                }
            }
        '''
    }
}

def analyze_vulnerability(name, data):
    """Perform comprehensive vulnerability analysis"""
    print(f"\n=== Analyzing {name} ===")
    
    # 1. Threat Context Analysis
    print("\nThreat Context:")
    context = threat_analyzer.embed_component(data)
    pprint({
        'name_similarity': context.get('name_similarity', 0),
        'description_match': context.get('description_match', []),
        'code_patterns': context.get('code_patterns', [])
    })
    
    # 2. Pattern Detection
    print("\nPattern Detection:")
    patterns = pattern_detector.analyze_component(data)
    pprint({
        'detected_patterns': patterns.get('pattern_matches', []),
        'risk_level': patterns.get('risk_level', 'unknown'),
        'code_analysis': patterns.get('code_analysis', {})
    })
    
    # 3. Exploit Prediction
    if 'vulnerability_data' in data:
        print("\nExploit Prediction:")
        prediction = exploit_predictor.predict_exploit_likelihood(
            data['vulnerability_data']
        )
        pprint({
            'probability': prediction['exploit_probability'],
            'confidence': prediction['confidence_score'],
            'key_factors': prediction.get('exploit_factors', [])[:3]
        })
    
    # 4. Security Recommendations
    print("\nSecurity Recommendations:")
    if patterns.get('risk_factors'):
        for factor in patterns['risk_factors']:
            print(f"- {factor['description']}")
            if 'mitigation' in factor:
                print(f"  Mitigation: {factor['mitigation']}")

def main():
    """Run analysis on all examples"""
    examples = [
        ('Path Traversal', path_traversal_example),
        ('XXE', xxe_example),
        ('Prototype Pollution', proto_pollution_example),
        ('SSTI', ssti_example),
        ('GraphQL Injection', graphql_example)
    ]
    
    for name, data in examples:
        analyze_vulnerability(name, data)
        print("\n" + "="*80)

if __name__ == '__main__':
    main()