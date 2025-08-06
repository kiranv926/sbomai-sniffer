import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';

interface NetworkScanResult {
  id: string;
  target: string;
  status: 'scanning' | 'completed' | 'failed';
  vulnerabilities: number;
  openPorts: number;
  services: string[];
  riskLevel: 'Critical' | 'High' | 'Medium' | 'Low';
  lastScan: string;
}

interface WebScanResult {
  id: string;
  url: string;
  status: 'scanning' | 'completed' | 'failed';
  vulnerabilities: number;
  securityHeaders: number;
  sslScore: number;
  riskLevel: 'Critical' | 'High' | 'Medium' | 'Low';
  lastScan: string;
}

interface DirectoryScanResult {
  id: string;
  path: string;
  status: 'scanning' | 'completed' | 'failed';
  filesFound: number;
  sensitiveFiles: number;
  exposedData: number;
  riskLevel: 'Critical' | 'High' | 'Medium' | 'Low';
  lastScan: string;
}

interface OSDetectionResult {
  id: string;
  host: string;
  os: string;
  version: string;
  kernel: string;
  vulnerabilities: number;
  patches: number;
  riskLevel: 'Critical' | 'High' | 'Medium' | 'Low';
  lastUpdate: string;
}

interface IoTVulnerability {
  id: string;
  device: string;
  type: string;
  vulnerability: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  status: 'open' | 'fixed' | 'in-progress';
  lastDetected: string;
}

interface ConfigVulnerability {
  id: string;
  component: string;
  configType: string;
  issue: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  status: 'open' | 'fixed' | 'in-progress';
  lastDetected: string;
}

interface AppVulnerability {
  id: string;
  application: string;
  vulnerability: string;
  cveId?: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  status: 'open' | 'fixed' | 'in-progress';
  lastDetected: string;
}

interface HumanVulnerability {
  id: string;
  type: string;
  description: string;
  riskLevel: 'Critical' | 'High' | 'Medium' | 'Low';
  affectedUsers: number;
  lastDetected: string;
}

const SecurityInsights: React.FC = () => {
  const [activeTab, setActiveTab] = useState('network');
  const [timeFilter, setTimeFilter] = useState('30');

  // Mock data functions
  const getNetworkScanResults = (): NetworkScanResult[] => {
    const days = parseInt(timeFilter);
    const timeMultiplier = days / 30;
    
    return [
      {
        id: '1',
        target: '192.168.1.1',
        status: 'completed',
        vulnerabilities: Math.round(12 * timeMultiplier),
        openPorts: 8,
        services: ['SSH', 'HTTP', 'HTTPS', 'FTP', 'SMTP'],
        riskLevel: 'High',
        lastScan: '2 hours ago'
      },
      {
        id: '2',
        target: '10.0.0.50',
        status: 'scanning',
        vulnerabilities: Math.round(5 * timeMultiplier),
        openPorts: 3,
        services: ['HTTP', 'HTTPS', 'DNS'],
        riskLevel: 'Medium',
        lastScan: 'In progress'
      },
      {
        id: '3',
        target: '172.16.0.100',
        status: 'completed',
        vulnerabilities: Math.round(18 * timeMultiplier),
        openPorts: 12,
        services: ['SSH', 'HTTP', 'HTTPS', 'FTP', 'SMTP', 'POP3', 'IMAP'],
        riskLevel: 'Critical',
        lastScan: '1 hour ago'
      }
    ];
  };

  const getWebScanResults = (): WebScanResult[] => {
    const days = parseInt(timeFilter);
    const timeMultiplier = days / 30;
    
    return [
      {
        id: '1',
        url: 'https://example.com',
        status: 'completed',
        vulnerabilities: Math.round(8 * timeMultiplier),
        securityHeaders: 6,
        sslScore: 85,
        riskLevel: 'Medium',
        lastScan: '1 hour ago'
      },
      {
        id: '2',
        url: 'https://api.example.com',
        status: 'completed',
        vulnerabilities: Math.round(15 * timeMultiplier),
        securityHeaders: 3,
        sslScore: 92,
        riskLevel: 'High',
        lastScan: '2 hours ago'
      },
      {
        id: '3',
        url: 'https://admin.example.com',
        status: 'scanning',
        vulnerabilities: Math.round(22 * timeMultiplier),
        securityHeaders: 8,
        sslScore: 78,
        riskLevel: 'Critical',
        lastScan: 'In progress'
      }
    ];
  };

  const getDirectoryScanResults = (): DirectoryScanResult[] => {
    const days = parseInt(timeFilter);
    const timeMultiplier = days / 30;
    
    return [
      {
        id: '1',
        path: '/var/www/html',
        status: 'completed',
        filesFound: Math.round(1250 * timeMultiplier),
        sensitiveFiles: Math.round(8 * timeMultiplier),
        exposedData: Math.round(3 * timeMultiplier),
        riskLevel: 'High',
        lastScan: '1 hour ago'
      },
      {
        id: '2',
        path: '/home/user/documents',
        status: 'completed',
        filesFound: Math.round(850 * timeMultiplier),
        sensitiveFiles: Math.round(15 * timeMultiplier),
        exposedData: Math.round(7 * timeMultiplier),
        riskLevel: 'Critical',
        lastScan: '30 minutes ago'
      }
    ];
  };

  const getOSDetectionResults = (): OSDetectionResult[] => {
    const days = parseInt(timeFilter);
    const timeMultiplier = days / 30;
    
    return [
      {
        id: '1',
        host: 'web-server-01',
        os: 'Ubuntu',
        version: '20.04 LTS',
        kernel: '5.4.0-74-generic',
        vulnerabilities: Math.round(12 * timeMultiplier),
        patches: Math.round(45 * timeMultiplier),
        riskLevel: 'Medium',
        lastUpdate: '2 hours ago'
      },
      {
        id: '2',
        host: 'db-server-01',
        os: 'CentOS',
        version: '7.9',
        kernel: '3.10.0-1160.el7.x86_64',
        vulnerabilities: Math.round(25 * timeMultiplier),
        patches: Math.round(18 * timeMultiplier),
        riskLevel: 'High',
        lastUpdate: '1 hour ago'
      }
    ];
  };

  const getIoTVulnerabilities = (): IoTVulnerability[] => {
    return [
      {
        id: '1',
        device: 'Security Camera - Floor 1',
        type: 'IoT Device',
        vulnerability: 'Default credentials not changed',
        severity: 'High',
        status: 'open',
        lastDetected: '1 hour ago'
      },
      {
        id: '2',
        device: 'Smart Thermostat - Office',
        type: 'IoT Device',
        vulnerability: 'Outdated firmware',
        severity: 'Medium',
        status: 'in-progress',
        lastDetected: '3 hours ago'
      }
    ];
  };

  const getConfigVulnerabilities = (): ConfigVulnerability[] => {
    return [
      {
        id: '1',
        component: 'Database Server',
        configType: 'Security Configuration',
        issue: 'Weak password policy',
        severity: 'High',
        status: 'open',
        lastDetected: '2 hours ago'
      },
      {
        id: '2',
        component: 'Web Server',
        configType: 'SSL Configuration',
        issue: 'TLS 1.0 enabled',
        severity: 'Medium',
        status: 'fixed',
        lastDetected: '1 day ago'
      }
    ];
  };

  const getAppVulnerabilities = (): AppVulnerability[] => {
    return [
      {
        id: '1',
        application: 'Web Application',
        vulnerability: 'SQL Injection vulnerability',
        cveId: 'CVE-2023-1234',
        severity: 'Critical',
        status: 'open',
        lastDetected: '30 minutes ago'
      },
      {
        id: '2',
        application: 'API Gateway',
        vulnerability: 'Cross-site scripting (XSS)',
        cveId: 'CVE-2023-5678',
        severity: 'High',
        status: 'in-progress',
        lastDetected: '2 hours ago'
      }
    ];
  };

  const getHumanVulnerabilities = (): HumanVulnerability[] => {
    const days = parseInt(timeFilter);
    const timeMultiplier = days / 30;
    
    return [
      {
        id: '1',
        type: 'Social Engineering',
        description: 'Phishing attempt detected',
        riskLevel: 'High',
        affectedUsers: Math.round(5 * timeMultiplier),
        lastDetected: '1 hour ago'
      },
      {
        id: '2',
        type: 'Password Policy',
        description: 'Weak passwords detected',
        riskLevel: 'Medium',
        affectedUsers: Math.round(12 * timeMultiplier),
        lastDetected: '3 hours ago'
      }
    ];
  };

  const networkScanResults = getNetworkScanResults();
  const webScanResults = getWebScanResults();
  const directoryScanResults = getDirectoryScanResults();
  const osDetectionResults = getOSDetectionResults();
  const iotVulnerabilities = getIoTVulnerabilities();
  const configVulnerabilities = getConfigVulnerabilities();
  const appVulnerabilities = getAppVulnerabilities();
  const humanVulnerabilities = getHumanVulnerabilities();

  // Helper functions
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return '#22c55e';
      case 'scanning': return '#f59e0b';
      case 'failed': return '#dc2626';
      case 'open': return '#dc2626';
      case 'fixed': return '#22c55e';
      case 'in-progress': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  const getRiskLevelColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'Critical': return '#dc2626';
      case 'High': return '#f97316';
      case 'Medium': return '#eab308';
      case 'Low': return '#22c55e';
      default: return '#6b7280';
    }
  };

  const tabs = [
    { id: 'network', name: 'Network Scanning', icon: '🌐', count: networkScanResults.length },
    { id: 'web', name: 'Web Applications', icon: '🌍', count: webScanResults.length },
    { id: 'directory', name: 'Directory Scanning', icon: '📁', count: directoryScanResults.length },
    { id: 'os', name: 'OS Detection', icon: '💻', count: osDetectionResults.length },
    { id: 'iot', name: 'IoT Vulnerabilities', icon: '📱', count: iotVulnerabilities.length },
    { id: 'config', name: 'Configuration', icon: '⚙️', count: configVulnerabilities.length },
    { id: 'app', name: 'Application', icon: '🔧', count: appVulnerabilities.length },
    { id: 'human', name: 'Human Factors', icon: '👥', count: humanVulnerabilities.length }
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'network':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {networkScanResults.map((scan) => (
              <div key={scan.id} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-gray-900 dark:text-white">{scan.target}</span>
                    <span 
                      className="px-2 py-1 rounded-full text-xs font-medium text-white"
                      style={{ backgroundColor: getStatusColor(scan.status) }}
                    >
                      {scan.status}
                    </span>
                  </div>
                  <span 
                    className="px-2 py-1 rounded-full text-xs font-medium text-white"
                    style={{ backgroundColor: getRiskLevelColor(scan.riskLevel) }}
                  >
                    {scan.riskLevel}
                  </span>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Vulnerabilities:</span>
                    <span className="font-medium text-red-600 dark:text-red-400">{scan.vulnerabilities}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Open Ports:</span>
                    <span className="font-medium text-blue-600 dark:text-blue-400">{scan.openPorts}</span>
                  </div>
                </div>
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    Services: {scan.services.slice(0, 3).join(', ')}{scan.services.length > 3 ? '...' : ''}
                  </div>
                  <div className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                    Last scan: {scan.lastScan}
                  </div>
                </div>
              </div>
            ))}
          </div>
        );

      case 'web':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {webScanResults.map((scan) => (
              <div key={scan.id} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-gray-900 dark:text-white text-sm">{scan.url}</span>
                    <span 
                      className="px-2 py-1 rounded-full text-xs font-medium text-white"
                      style={{ backgroundColor: getStatusColor(scan.status) }}
                    >
                      {scan.status}
                    </span>
                  </div>
                  <span 
                    className="px-2 py-1 rounded-full text-xs font-medium text-white"
                    style={{ backgroundColor: getRiskLevelColor(scan.riskLevel) }}
                  >
                    {scan.riskLevel}
                  </span>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Vulnerabilities:</span>
                    <span className="font-medium text-red-600 dark:text-red-400">{scan.vulnerabilities}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Security Headers:</span>
                    <span className="font-medium text-green-600 dark:text-green-400">{scan.securityHeaders}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">SSL Score:</span>
                    <span className="font-medium text-blue-600 dark:text-blue-400">{scan.sslScore}</span>
                  </div>
                </div>
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                  <div className="text-xs text-gray-400 dark:text-gray-500">
                    Last scan: {scan.lastScan}
                  </div>
                </div>
              </div>
            ))}
          </div>
        );

      case 'directory':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {directoryScanResults.map((scan) => (
              <div key={scan.id} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-gray-900 dark:text-white text-sm">{scan.path}</span>
                    <span 
                      className="px-2 py-1 rounded-full text-xs font-medium text-white"
                      style={{ backgroundColor: getStatusColor(scan.status) }}
                    >
                      {scan.status}
                    </span>
                  </div>
                  <span 
                    className="px-2 py-1 rounded-full text-xs font-medium text-white"
                    style={{ backgroundColor: getRiskLevelColor(scan.riskLevel) }}
                  >
                    {scan.riskLevel}
                  </span>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Files Found:</span>
                    <span className="font-medium text-blue-600 dark:text-blue-400">{scan.filesFound}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Sensitive Files:</span>
                    <span className="font-medium text-orange-600 dark:text-orange-400">{scan.sensitiveFiles}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Exposed Data:</span>
                    <span className="font-medium text-red-600 dark:text-red-400">{scan.exposedData}</span>
                  </div>
                </div>
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                  <div className="text-xs text-gray-400 dark:text-gray-500">
                    Last scan: {scan.lastScan}
                  </div>
                </div>
              </div>
            ))}
          </div>
        );

      case 'os':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {osDetectionResults.map((host) => (
              <div key={host.id} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-gray-900 dark:text-white text-sm">{host.host}</span>
                    <span 
                      className="px-2 py-1 rounded-full text-xs font-medium text-white"
                      style={{ backgroundColor: getRiskLevelColor(host.riskLevel) }}
                    >
                      {host.riskLevel}
                    </span>
                  </div>
                </div>
                <div className="text-sm mb-3">
                  <span className="text-gray-600 dark:text-gray-300">{host.os} {host.version}</span>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Vulnerabilities:</span>
                    <span className="font-medium text-red-600 dark:text-red-400">{host.vulnerabilities}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Patches:</span>
                    <span className="font-medium text-green-600 dark:text-green-400">{host.patches}</span>
                  </div>
                </div>
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                  <div className="text-xs text-gray-400 dark:text-gray-500">
                    Last update: {host.lastUpdate}
                  </div>
                </div>
              </div>
            ))}
          </div>
        );

      case 'iot':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {iotVulnerabilities.map((vuln) => (
              <div key={vuln.id} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-gray-900 dark:text-white text-sm">{vuln.device}</span>
                    <span 
                      className="px-2 py-1 rounded-full text-xs font-medium text-white"
                      style={{ backgroundColor: getStatusColor(vuln.status) }}
                    >
                      {vuln.status}
                    </span>
                  </div>
                  <span 
                    className="px-2 py-1 rounded-full text-xs font-medium text-white"
                    style={{ backgroundColor: getRiskLevelColor(vuln.severity) }}
                  >
                    {vuln.severity}
                  </span>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="text-gray-600 dark:text-gray-300">
                    <span className="font-medium">Type:</span> {vuln.type}
                  </div>
                  <div className="text-gray-600 dark:text-gray-300">
                    <span className="font-medium">Issue:</span> {vuln.vulnerability}
                  </div>
                </div>
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                  <div className="text-xs text-gray-400 dark:text-gray-500">
                    Last detected: {vuln.lastDetected}
                  </div>
                </div>
              </div>
            ))}
          </div>
        );

      case 'config':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {configVulnerabilities.map((vuln) => (
              <div key={vuln.id} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-gray-900 dark:text-white text-sm">{vuln.component}</span>
                    <span 
                      className="px-2 py-1 rounded-full text-xs font-medium text-white"
                      style={{ backgroundColor: getStatusColor(vuln.status) }}
                    >
                      {vuln.status}
                    </span>
                  </div>
                  <span 
                    className="px-2 py-1 rounded-full text-xs font-medium text-white"
                    style={{ backgroundColor: getRiskLevelColor(vuln.severity) }}
                  >
                    {vuln.severity}
                  </span>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="text-gray-600 dark:text-gray-300">
                    <span className="font-medium">Config Type:</span> {vuln.configType}
                  </div>
                  <div className="text-gray-600 dark:text-gray-300">
                    <span className="font-medium">Issue:</span> {vuln.issue}
                  </div>
                </div>
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                  <div className="text-xs text-gray-400 dark:text-gray-500">
                    Last detected: {vuln.lastDetected}
                  </div>
                </div>
              </div>
            ))}
          </div>
        );

      case 'app':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {appVulnerabilities.map((vuln) => (
              <div key={vuln.id} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-gray-900 dark:text-white text-sm">{vuln.application}</span>
                    <span 
                      className="px-2 py-1 rounded-full text-xs font-medium text-white"
                      style={{ backgroundColor: getStatusColor(vuln.status) }}
                    >
                      {vuln.status}
                    </span>
                  </div>
                  <span 
                    className="px-2 py-1 rounded-full text-xs font-medium text-white"
                    style={{ backgroundColor: getRiskLevelColor(vuln.severity) }}
                  >
                    {vuln.severity}
                  </span>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="text-gray-600 dark:text-gray-300">
                    <span className="font-medium">Vulnerability:</span> {vuln.vulnerability}
                  </div>
                  {vuln.cveId && (
                    <div className="text-gray-600 dark:text-gray-300">
                      <span className="font-medium">CVE:</span> {vuln.cveId}
                    </div>
                  )}
                </div>
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                  <div className="text-xs text-gray-400 dark:text-gray-500">
                    Last detected: {vuln.lastDetected}
                  </div>
                </div>
              </div>
            ))}
          </div>
        );

      case 'human':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {humanVulnerabilities.map((vuln) => (
              <div key={vuln.id} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-gray-900 dark:text-white text-sm">{vuln.type}</span>
                    <span 
                      className="px-2 py-1 rounded-full text-xs font-medium text-white"
                      style={{ backgroundColor: getRiskLevelColor(vuln.riskLevel) }}
                    >
                      {vuln.riskLevel}
                    </span>
                  </div>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="text-gray-600 dark:text-gray-300">
                    <span className="font-medium">Description:</span> {vuln.description}
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Affected Users:</span>
                    <span className="font-medium text-orange-600 dark:text-orange-400">{vuln.affectedUsers}</span>
                  </div>
                </div>
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                  <div className="text-xs text-gray-400 dark:text-gray-500">
                    Last detected: {vuln.lastDetected}
                  </div>
                </div>
              </div>
            ))}
          </div>
        );

      default:
        return <div>Select a tab to view content</div>;
    }
  };

  return (
    <div className="w-full h-full bg-gray-50 dark:bg-gray-900">
      <div className="w-full space-y-6 p-4 lg:p-6">
        {/* Page Header */}
        <PageHeader
          title="Security Insights"
          description="Comprehensive vulnerability analysis across all security domains"
          icon={
            <svg className="w-6 h-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          }
          actions={
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Time Range:</label>
                <select
                  value={timeFilter}
                  onChange={(e) => setTimeFilter(e.target.value)}
                  className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="7">Last 7 days</option>
                  <option value="30">Last 30 days</option>
                  <option value="90">Last 90 days</option>
                  <option value="180">Last 6 months</option>
                </select>
              </div>
            </div>
          }
        />

        {/* Tab Navigation */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="flex space-x-8 px-6 overflow-x-auto" aria-label="Tabs">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`border-b-2 py-4 px-1 text-sm font-medium whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                      : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <span>{tab.icon}</span>
                    <span>{tab.name}</span>
                    <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                      activeTab === tab.id
                        ? 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
                    }`}>
                      {tab.count}
                    </span>
                  </div>
                </button>
              ))}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {renderTabContent()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SecurityInsights; 