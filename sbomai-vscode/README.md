# SBOMAI VSCode Extension

A Visual Studio Code extension for AI-powered SBOM analysis with real-time vulnerability scanning and policy enforcement.

## Features

- **File Analysis**: Analyze individual SBOM files directly from the editor
- **Workspace Scanning**: Scan entire workspaces for SBOM files and analyze them
- **Real-time Results**: View analysis results in a dedicated sidebar panel
- **Quick Actions**: Right-click context menu for quick SBOM analysis
- **Configuration**: Easy setup and configuration through VSCode settings
- **Integration**: Seamless integration with SBOMAI core services

## Installation

### From VSIX Package
1. Download the latest `.vsix` package from releases
2. In VSCode, go to Extensions (Ctrl+Shift+X)
3. Click the "..." menu and select "Install from VSIX..."
4. Select the downloaded package

### From Source
```bash
git clone <repository-url>
cd sbomai-vscode
npm install
npm run compile
npm run package
```

## Quick Start

1. **Install the Extension**: Install the SBOMAI VSCode extension
2. **Configure Connection**: Set the SBOMAI server URL in settings
3. **Analyze a File**: Right-click on an SBOM file and select "SBOMAI: Analyze File"
4. **View Results**: Check the SBOMAI Analysis Results panel in the explorer

## Usage

### Command Palette Commands

- `SBOMAI: Analyze Current File` - Analyze the currently open file
- `SBOMAI: Analyze Workspace` - Scan and analyze all SBOM files in the workspace
- `SBOMAI: Show Results` - Open the analysis results panel
- `SBOMAI: Configure` - Open configuration settings

### Context Menu Actions

Right-click on any file in the explorer to access:
- **SBOMAI: Analyze File** - Analyze the selected file
- **SBOMAI: Analyze Directory** - Analyze all SBOM files in the directory

### Results Panel

The SBOMAI Analysis Results panel shows:
- **Summary**: Overall analysis status and key metrics
- **Vulnerabilities**: List of found vulnerabilities with severity
- **Policy Violations**: Policy violations and recommendations
- **AI Insights**: AI-generated risk analysis and recommendations
- **Components**: Detailed component analysis

## Configuration

### Settings

Configure the extension through VSCode settings:

```json
{
  "sbomai.serverUrl": "http://localhost:8080",
  "sbomai.apiKey": "your-api-key",
  "sbomai.autoAnalyze": false,
  "sbomai.showNotifications": true,
  "sbomai.defaultFormat": "auto"
}
```

### Environment Variables

- `SBOMAI_SERVER_URL` - SBOMAI core service URL
- `SBOMAI_API_KEY` - API key for authentication

## Supported SBOM Formats

- **SPDX** (.spdx, .spdx.json, .spdx.xml, .spdx.yaml)
- **CycloneDX** (.cdx, .cdx.json, .cdx.xml, .cdx.yaml)
- **SWID** (.swid, .swid.xml)

## Features in Detail

### File Analysis
- Automatic format detection
- Real-time analysis feedback
- Detailed vulnerability reporting
- Policy violation highlighting

### Workspace Scanning
- Recursive directory scanning
- Batch analysis capabilities
- Progress tracking
- Summary reporting

### Integration Features
- REST API communication with SBOMAI core
- Error handling and retry logic
- Offline mode support
- Caching for performance

## Development

### Prerequisites
- Node.js 16+
- TypeScript 4.5+
- VSCode Extension Development Host

### Setup
```bash
npm install
npm run compile
```

### Testing
```bash
npm run test
npm run test:integration
```

### Building
```bash
npm run compile
npm run package
```

### Debugging
1. Open the project in VSCode
2. Press F5 to launch the Extension Development Host
3. Use the debug console for logging

## Architecture

### Extension Structure
```
src/
├── extension.ts          # Main extension entry point
├── commands/             # Command implementations
├── services/             # Business logic services
├── views/                # UI components and panels
├── types/                # TypeScript type definitions
└── utils/                # Utility functions
```

### Key Components
- **Extension Manager**: Main extension lifecycle management
- **Analysis Service**: Handles SBOM analysis requests
- **Results Provider**: Manages analysis results display
- **Configuration Manager**: Handles settings and configuration
- **API Client**: Communicates with SBOMAI core services

## Troubleshooting

### Common Issues

**Connection Failed**
- Verify SBOMAI core service is running
- Check server URL configuration
- Ensure network connectivity

**Analysis Fails**
- Verify SBOM file format is supported
- Check file permissions
- Review error logs in Output panel

**Results Not Displaying**
- Refresh the results panel
- Check VSCode console for errors
- Verify extension is properly activated

### Debug Mode
Enable debug logging:
```json
{
  "sbomai.debug": true
}
```

### Logs
View extension logs in VSCode:
1. Open Command Palette (Ctrl+Shift+P)
2. Type "Developer: Show Logs"
3. Select "Extension Host" and look for "SBOMAI"

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style
- Follow TypeScript best practices
- Use ESLint and Prettier
- Write comprehensive tests
- Document new features

## License

This extension is licensed under the same license as the main SBOMAI project.

## Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: See the main SBOMAI documentation
- **Community**: Join our community discussions

## Changelog

### 1.0.0
- Initial release
- Basic file analysis functionality
- Results panel implementation
- Configuration management 