# SBOMAI GitHub Action

GitHub Action for SBOMAI - provides automated SBOM analysis in CI/CD pipelines with GitHub integration and automated reporting.

## Features

- **Automated Analysis**: Integrate SBOM analysis into your CI/CD pipeline
- **GitHub Integration**: Create issues, comments, and status checks
- **Flexible Configuration**: Customize analysis parameters and failure conditions
- **Multiple Formats**: Support for SPDX, CycloneDX, and SWID formats
- **Policy Enforcement**: Automated policy violation detection and reporting
- **AI Insights**: AI-powered risk analysis and recommendations

## Quick Start

### Basic Usage

```yaml
name: SBOM Analysis

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  sbom-analysis:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Generate SBOM
      run: |
        # Generate your SBOM here
        echo "Generating SBOM..."
    
    - name: Analyze SBOM
      uses: your-org/sbomai-action@v1
      with:
        sbom-file: 'bom.spdx'
        sbom-format: 'SPDX'
        fail-on-critical: 'true'
        fail-on-high: 'false'
```

### Advanced Usage

```yaml
name: Comprehensive SBOM Analysis

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  sbom-analysis:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Generate SBOM
      run: |
        # Generate your SBOM here
        echo "Generating SBOM..."
    
    - name: Analyze SBOM
      uses: your-org/sbomai-action@v1
      with:
        sbom-file: 'bom.spdx'
        sbom-format: 'AUTO'
        sbomai-url: 'https://sbomai.company.com'
        fail-on-critical: 'true'
        fail-on-high: 'true'
        create-issue: 'true'
        issue-labels: 'security,sbom,vulnerability,automated'
        output-format: 'JSON'
        verbose: 'true'
      id: sbom-analysis
    
    - name: Process Results
      run: |
        echo "Vulnerabilities found: ${{ steps.sbom-analysis.outputs.vulnerabilities-found }}"
        echo "Critical vulnerabilities: ${{ steps.sbom-analysis.outputs.critical-vulnerabilities }}"
        echo "Analysis status: ${{ steps.sbom-analysis.outputs.analysis-status }}"
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `sbom-file` | Path to the SBOM file to analyze | Yes | `bom.spdx` |
| `sbom-format` | SBOM format (SPDX, CYCLONEDX, SWID, AUTO) | No | `AUTO` |
| `sbomai-url` | SBOMAI core service URL | No | `http://localhost:8080` |
| `fail-on-critical` | Fail the action if critical vulnerabilities are found | No | `true` |
| `fail-on-high` | Fail the action if high severity vulnerabilities are found | No | `false` |
| `create-issue` | Create GitHub issue for policy violations | No | `false` |
| `issue-labels` | Labels to add to created issues | No | `security,sbom,vulnerability` |
| `output-format` | Output format for results (JSON, TEXT, HTML) | No | `TEXT` |
| `verbose` | Enable verbose output | No | `false` |

## Outputs

| Output | Description |
|--------|-------------|
| `vulnerabilities-found` | Number of vulnerabilities found |
| `critical-vulnerabilities` | Number of critical vulnerabilities found |
| `high-vulnerabilities` | Number of high severity vulnerabilities found |
| `policy-violations` | Number of policy violations found |
| `analysis-status` | Status of the analysis (SUCCESS, FAILED, WARNING) |
| `results-file` | Path to the detailed results file |

## Examples

### Basic Security Check

```yaml
- name: Security SBOM Analysis
  uses: your-org/sbomai-action@v1
  with:
    sbom-file: 'security-bom.spdx'
    fail-on-critical: 'true'
    fail-on-high: 'true'
```

### Compliance Check

```yaml
- name: Compliance SBOM Analysis
  uses: your-org/sbomai-action@v1
  with:
    sbom-file: 'compliance-bom.spdx'
    create-issue: 'true'
    issue-labels: 'compliance,license,security'
    output-format: 'JSON'
```

### Custom SBOMAI Service

```yaml
- name: Custom SBOMAI Analysis
  uses: your-org/sbomai-action@v1
  with:
    sbom-file: 'bom.spdx'
    sbomai-url: 'https://sbomai.internal.company.com'
    verbose: 'true'
```

## Integration Examples

### With Syft (for generating SBOMs)

```yaml
name: SBOM Generation and Analysis

on:
  push:
    branches: [ main ]

jobs:
  sbom-analysis:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Generate SBOM with Syft
      run: |
        syft packages . -o spdx-json > bom.spdx.json
    
    - name: Analyze SBOM
      uses: your-org/sbomai-action@v1
      with:
        sbom-file: 'bom.spdx.json'
        sbom-format: 'SPDX'
```

### With CycloneDX

```yaml
name: CycloneDX SBOM Analysis

on:
  push:
    branches: [ main ]

jobs:
  sbom-analysis:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Generate CycloneDX SBOM
      run: |
        # Generate CycloneDX SBOM
        cyclonedx-bom -o bom.xml
    
    - name: Analyze SBOM
      uses: your-org/sbomai-action@v1
      with:
        sbom-file: 'bom.xml'
        sbom-format: 'CYCLONEDX'
```

### With Multiple SBOMs

```yaml
name: Multi-SBOM Analysis

on:
  push:
    branches: [ main ]

jobs:
  sbom-analysis:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Generate Multiple SBOMs
      run: |
        # Generate different SBOMs
        syft packages . -o spdx-json > bom.spdx.json
        cyclonedx-bom -o bom.xml
    
    - name: Analyze SPDX SBOM
      uses: your-org/sbomai-action@v1
      with:
        sbom-file: 'bom.spdx.json'
        sbom-format: 'SPDX'
      id: spdx-analysis
    
    - name: Analyze CycloneDX SBOM
      uses: your-org/sbomai-action@v1
      with:
        sbom-file: 'bom.xml'
        sbom-format: 'CYCLONEDX'
      id: cyclonedx-analysis
```

## GitHub Integration Features

### Automatic Issue Creation

When `create-issue` is enabled, the action will automatically create GitHub issues for policy violations:

```yaml
- name: Analyze with Issue Creation
  uses: your-org/sbomai-action@v1
  with:
    sbom-file: 'bom.spdx'
    create-issue: 'true'
    issue-labels: 'security,automated'
```

### Status Checks

The action automatically creates status checks for your commits and pull requests, showing:

- Overall analysis status
- Number of vulnerabilities found
- Policy violation summary
- AI risk assessment

### Comments on Pull Requests

For pull requests, the action can add comments with:

- Summary of findings
- Links to detailed reports
- Recommendations for remediation

## Configuration

### Environment Variables

You can configure the action using environment variables:

```yaml
env:
  SBOMAI_API_KEY: ${{ secrets.SBOMAI_API_KEY }}
  SBOMAI_TIMEOUT: 300000
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Secrets

Recommended secrets to configure:

- `GITHUB_TOKEN`: For GitHub API access (automatically provided)
- `SBOMAI_API_KEY`: For SBOMAI service authentication
- `SBOMAI_URL`: For custom SBOMAI service URL

## Error Handling

The action handles various error scenarios:

- **SBOM File Not Found**: Fails with clear error message
- **Invalid SBOM Format**: Attempts auto-detection, fails if unsuccessful
- **Network Issues**: Retries with exponential backoff
- **Service Unavailable**: Graceful degradation with warnings

## Troubleshooting

### Common Issues

1. **SBOM File Not Found**
   ```yaml
   # Ensure the SBOM file exists before analysis
   - name: Check SBOM File
     run: |
       if [ ! -f "bom.spdx" ]; then
         echo "SBOM file not found!"
         exit 1
       fi
   ```

2. **Network Connectivity**
   ```yaml
   # Test connectivity to SBOMAI service
   - name: Test Connectivity
     run: |
       curl -f ${{ inputs.sbomai-url }}/api/v1/sbom/health
   ```

3. **Permission Issues**
   ```yaml
   # Ensure proper permissions
   permissions:
     contents: read
     issues: write
     pull-requests: write
   ```

### Debug Mode

Enable verbose output for debugging:

```yaml
- name: Debug Analysis
  uses: your-org/sbomai-action@v1
  with:
    sbom-file: 'bom.spdx'
    verbose: 'true'
```

## Contributing

1. Follow the existing code style
2. Add comprehensive tests for new features
3. Update documentation for new inputs/outputs
4. Ensure backward compatibility

## License

This project is licensed under the MIT License - see the LICENSE file for details. 