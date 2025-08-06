import React, { useState, useEffect } from 'react';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell, PieChart, Pie } from 'recharts';
import PageHeader from '../components/PageHeader';

interface ScanTarget {
  id: string;
  domain: string;
  lastScanned: string;
  technologies: string[];
  sbomAvailable: boolean;
  vulnerabilities: number;
  cveSeverity: 'low' | 'medium' | 'high' | 'critical';
  aiRiskScore: number;
  status: 'active' | 'scanning' | 'error';
  screenshot?: string;
  components: Component[];
  externalScripts: ExternalScript[];
  securityHeaders: SecurityHeader[];
}

interface Component {
  name: string;
  version: string;
  type: 'library' | 'framework' | 'cdn';
  cves: string[];
  risk: 'low' | 'medium' | 'high' | 'critical';
}

interface ExternalScript {
  url: string;
  domain: string;
  purpose: string;
  risk: 'low' | 'medium' | 'high' | 'critical';
  dataExposure: boolean;
}

interface SecurityHeader {
  name: string;
  value: string;
  status: 'present' | 'missing' | 'weak';
  recommendation: string;
}

const WebScan: React.FC = () => {
  const [scanTargets, setScanTargets] = useState<ScanTarget[]>([]);
  const [selectedTarget, setSelectedTarget] = useState<ScanTarget | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState<string>('all');
  const [filterTech, setFilterTech] = useState<string>('all');

  const [scanning, setScanning] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);

  // Mock data
  const mockScanTargets: ScanTarget[] = [
    {
      id: '1',
      domain: 'example.com',
      lastScanned: '2025-01-15T10:30:00Z',
      technologies: ['React', 'Node.js', 'Express'],
      sbomAvailable: true,
      vulnerabilities: 3,
      cveSeverity: 'medium',
      aiRiskScore: 45,
      status: 'active',
      components: [
        { name: 'jQuery', version: '3.4.0', type: 'library', cves: ['CVE-2023-1234'], risk: 'medium' },
        { name: 'Bootstrap', version: '5.1.0', type: 'framework', cves: [], risk: 'low' }
      ],
      externalScripts: [
        { url: 'https://cdn.example.com/analytics.js', domain: 'cdn.example.com', purpose: 'Analytics', risk: 'low', dataExposure: false }
      ],
      securityHeaders: [
        { name: 'HSTS', value: 'max-age=31536000', status: 'present', recommendation: 'Good configuration' },
        { name: 'CSP', value: 'default-src \'self\'', status: 'weak', recommendation: 'Strengthen policy' }
      ]
    },
    {
      id: '2',
      domain: 'test-app.com',
      lastScanned: '2025-01-14T15:45:00Z',
      technologies: ['Vue.js', 'Laravel', 'MySQL'],
      sbomAvailable: false,
      vulnerabilities: 7,
      cveSeverity: 'high',
      aiRiskScore: 78,
      status: 'active',
      components: [
        { name: 'Log4j', version: '2.14.0', type: 'library', cves: ['CVE-2021-44228'], risk: 'critical' },
        { name: 'Vue', version: '2.6.0', type: 'framework', cves: ['CVE-2022-1234'], risk: 'high' }
      ],
      externalScripts: [
        { url: 'https://third-party.com/tracker.js', domain: 'third-party.com', purpose: 'Tracking', risk: 'high', dataExposure: true }
      ],
      securityHeaders: [
        { name: 'HSTS', value: '', status: 'missing', recommendation: 'Enable HSTS' },
        { name: 'CSP', value: '', status: 'missing', recommendation: 'Implement CSP' }
      ]
    },
    {
      id: '3',
      domain: 'demo-site.org',
      lastScanned: '2025-01-13T09:20:00Z',
      technologies: ['Angular', 'Spring Boot', 'PostgreSQL'],
      sbomAvailable: true,
      vulnerabilities: 1,
      cveSeverity: 'low',
      aiRiskScore: 22,
      status: 'active',
      components: [
        { name: 'Angular', version: '15.0.0', type: 'framework', cves: [], risk: 'low' },
        { name: 'Spring', version: '3.0.0', type: 'framework', cves: [], risk: 'low' }
      ],
      externalScripts: [],
      securityHeaders: [
        { name: 'HSTS', value: 'max-age=31536000; includeSubDomains', status: 'present', recommendation: 'Excellent configuration' },
        { name: 'CSP', value: 'default-src \'self\'; script-src \'self\' \'unsafe-inline\'', status: 'present', recommendation: 'Good configuration' }
      ]
    }
  ];

  const summaryData = {
    totalDomains: scanTargets.length,
    componentsDiscovered: scanTargets.reduce((sum, target) => sum + target.components.length, 0),
    criticalExposures: scanTargets.filter(target => target.cveSeverity === 'critical').length,
    riskyScripts: scanTargets.reduce((sum, target) => sum + target.externalScripts.filter(script => script.risk === 'high' || script.risk === 'critical').length, 0),
    lastScanStatus: scanTargets.length > 0 ? 'All systems operational' : 'No scans performed'
  };

  const cveSeverityData = [
    { name: 'Low', value: scanTargets.filter(t => t.cveSeverity === 'low').length, color: '#10B981' },
    { name: 'Medium', value: scanTargets.filter(t => t.cveSeverity === 'medium').length, color: '#F59E0B' },
    { name: 'High', value: scanTargets.filter(t => t.cveSeverity === 'high').length, color: '#EF4444' },
    { name: 'Critical', value: scanTargets.filter(t => t.cveSeverity === 'critical').length, color: '#7C2D12' }
  ];

  const techStackData = scanTargets.reduce((acc, target) => {
    target.technologies.forEach(tech => {
      acc[tech] = (acc[tech] || 0) + 1;
    });
    return acc;
  }, {} as Record<string, number>);

  const techChartData = Object.entries(techStackData).map(([tech, count]) => ({
    name: tech,
    count
  }));

  useEffect(() => {
    setScanTargets(mockScanTargets);
  }, []);



  const handleTargetDetails = (target: ScanTarget) => {
    setSelectedTarget(target);
    setShowDetailModal(true);
  };

  const closeDetailModal = () => {
    setSelectedTarget(null);
    setShowDetailModal(false);
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'critical': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300';
      case 'high': return 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-300';
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300';
      case 'low': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-300';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return '#7C2D12';
      case 'high': return '#EF4444';
      case 'medium': return '#F59E0B';
      case 'low': return '#10B981';
      default: return '#6B7280';
    }
  };

  const filteredTargets = scanTargets.filter(target => {
    const matchesSearch = target.domain.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRisk = filterRisk === 'all' || target.cveSeverity === filterRisk;
    const matchesTech = filterTech === 'all' || target.technologies.includes(filterTech);
    return matchesSearch && matchesRisk && matchesTech;
  });

  return (
    <div className="w-full h-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
                    <div className="px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <PageHeader
          title="Web Application Security Scan"
          description="Scan your live website for vulnerabilities and risks in real-time."
          icon={
            <svg className="w-6 h-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
          }
          actions={
            <div className="flex flex-col sm:flex-row gap-3 lg:gap-4">
              <button 
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-all duration-200 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105"
                title="Register a new URL for scanning"
              >
                <span className="text-xl">➕</span>
                <span>Add Website</span>
              </button>
              <button 
                className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105 ${
                  scanning 
                    ? 'bg-yellow-600 hover:bg-yellow-700 text-white' 
                    : 'bg-green-600 hover:bg-green-700 text-white'
                }`}
                title="Trigger a scan for selected website(s)"
                disabled={scanning}
              >
                <span className="text-xl">{scanning ? '⏳' : '🔄'}</span>
                <span>{scanning ? 'Scanning...' : 'Scan Now'}</span>
              </button>
            </div>
          }
        />

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Domains</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">{summaryData.totalDomains}</p>
              </div>
              <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl">🌐</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Components</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">{summaryData.componentsDiscovered}</p>
              </div>
              <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl">🧬</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Critical Exposures</p>
                <p className="text-3xl font-bold text-red-600">{summaryData.criticalExposures}</p>
              </div>
              <div className="w-12 h-12 bg-red-500 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl">🔓</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Risky Scripts</p>
                <p className="text-3xl font-bold text-orange-600">{summaryData.riskyScripts}</p>
              </div>
              <div className="w-12 h-12 bg-orange-500 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl">🚨</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Last Scan</p>
                <p className="text-sm font-bold text-gray-900 dark:text-white">{summaryData.lastScanStatus}</p>
              </div>
              <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl">🔄</span>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 gap-8 mb-8">
          {/* AI Exposure Map */}
          <div>
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white">🧠 AI-Powered Exposure Map</h2>
                  <div className="flex space-x-2">
                    <select 
                      value={filterRisk} 
                      onChange={(e) => setFilterRisk(e.target.value)}
                      className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg text-sm border border-gray-300 dark:border-gray-600"
                    >
                      <option value="all">All Risk Levels</option>
                      <option value="low">Low Risk</option>
                      <option value="medium">Medium Risk</option>
                      <option value="high">High Risk</option>
                      <option value="critical">Critical Risk</option>
                    </select>
                    <select 
                      value={filterTech} 
                      onChange={(e) => setFilterTech(e.target.value)}
                      className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg text-sm border border-gray-300 dark:border-gray-600"
                    >
                      <option value="all">All Technologies</option>
                      {Array.from(new Set(scanTargets.flatMap(t => t.technologies))).map(tech => (
                        <option key={tech} value={tech}>{tech}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {filteredTargets.map((target) => (
                    <div 
                      key={target.id}
                      className="p-4 border rounded-lg cursor-pointer hover:shadow-md transition-all duration-200"
                      style={{ borderColor: getSeverityColor(target.cveSeverity) }}
                      onClick={() => setSelectedTarget(target)}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold text-gray-900 dark:text-white">{target.domain}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(target.cveSeverity)}`}>
                          {target.cveSeverity.toUpperCase()}
                        </span>
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                        <p>Risk Score: {target.aiRiskScore}/100</p>
                        <p>Vulnerabilities: {target.vulnerabilities}</p>
                        <p>Components: {target.components.length}</p>
                        <p>Last Scan: {new Date(target.lastScanned).toLocaleDateString()}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>


        </div>

        {/* Scan Results Table */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 mb-8">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">🗃️ Scan Results</h2>
              <div className="flex space-x-4">
                <input
                  type="text"
                  placeholder="Search domains..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  onClick={() => setScanning(true)}
                  disabled={scanning}
                  className="px-6 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors duration-200"
                >
                  {scanning ? 'Scanning...' : '🔄 Scan Now'}
                </button>
              </div>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Domain</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Last Scanned</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Technologies</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">SBOM</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Vulnerabilities</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Risk Score</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {filteredTargets.map((target) => (
                  <tr key={target.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center mr-3">
                          <span className="text-white text-sm">🌐</span>
                        </div>
                        <div>
                          <div className="text-sm font-medium text-gray-900 dark:text-white">{target.domain}</div>
                          <div className="text-sm text-gray-500 dark:text-gray-400">{target.status}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {new Date(target.lastScanned).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex flex-wrap gap-1">
                        {target.technologies.slice(0, 2).map((tech, index) => (
                          <span key={index} className="px-2 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-300 rounded-full text-xs">
                            {tech}
                          </span>
                        ))}
                        {target.technologies.length > 2 && (
                          <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full text-xs">
                            +{target.technologies.length - 2}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        target.sbomAvailable 
                          ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300'
                          : 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300'
                      }`}>
                        {target.sbomAvailable ? 'Available' : 'Missing'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(target.cveSeverity)}`}>
                          {target.vulnerabilities}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-16 bg-gray-200 dark:bg-gray-700 rounded-full h-2 mr-2">
                          <div 
                            className="h-2 rounded-full transition-all duration-300"
                            style={{ 
                              width: `${target.aiRiskScore}%`,
                              backgroundColor: target.aiRiskScore > 70 ? '#EF4444' : target.aiRiskScore > 40 ? '#F59E0B' : '#10B981'
                            }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-900 dark:text-white">{target.aiRiskScore}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button 
                          onClick={() => handleTargetDetails(target)}
                          className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm font-medium transition-colors duration-200"
                        >
                          View
                        </button>
                        <button className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-sm font-medium transition-colors duration-200">
                          Re-scan
                        </button>
                        <button className="px-3 py-1 bg-purple-600 hover:bg-purple-700 text-white rounded text-sm font-medium transition-colors duration-200">
                          SBOM
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">CVE Severity Breakdown</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={cveSeverityData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                                     label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {cveSeverityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Technology Stack Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={techChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Below Results Panel: Secondary Action Panel */}
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div className="text-center lg:text-left">
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">📊 Scan Results Actions</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Review, export, and share your scan findings with your team
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-3 lg:gap-4">
              <button 
                className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-all duration-200 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105"
                title="Use AI to analyze risks and prioritize action"
              >
                <span className="text-xl">🧠</span>
                <span>AI Review Risks</span>
              </button>
              <button 
                className="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-all duration-200 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105"
                title="Download full report in CSV or PDF format"
              >
                <span className="text-xl">🧾</span>
                <span>Export Findings</span>
              </button>
              <button 
                className="px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-medium transition-all duration-200 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105"
                title="Send report via email, webhook, or public link"
              >
                <span className="text-xl">📤</span>
                <span>Share Report</span>
              </button>
            </div>
          </div>
        </div>

       </div>

       {/* Scan Detail Modal */}
       {showDetailModal && selectedTarget && (
         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
           <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl max-w-6xl w-full max-h-[90vh] overflow-y-auto">
             <div className="p-6">
               {/* Modal Header */}
               <div className="flex items-center justify-between mb-6">
                 <div className="flex items-center space-x-3">
                   <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center">
                     <span className="text-white text-xl">🌐</span>
                   </div>
                   <div>
                     <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                       Scan Details: {selectedTarget.domain}
                     </h2>
                     <p className="text-sm text-gray-600 dark:text-gray-300">
                       Last scanned: {new Date(selectedTarget.lastScanned).toLocaleString()}
                     </p>
                   </div>
                 </div>
                 <button
                   onClick={closeDetailModal}
                   className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
                 >
                   <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                   </svg>
                 </button>
               </div>

               {/* Basic Information */}
               <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                 <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                   <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">📋 Basic Information</h3>
                   <div className="space-y-2">
                     <div className="flex justify-between">
                       <span className="text-sm text-gray-600 dark:text-gray-400">Domain:</span>
                       <span className="text-sm font-medium text-gray-900 dark:text-white">{selectedTarget.domain}</span>
                     </div>
                     <div className="flex justify-between">
                       <span className="text-sm text-gray-600 dark:text-gray-400">Status:</span>
                       <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                         selectedTarget.status === 'active' ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300' :
                         selectedTarget.status === 'scanning' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300' :
                         'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300'
                       }`}>
                         {selectedTarget.status.toUpperCase()}
                       </span>
                     </div>
                     <div className="flex justify-between">
                       <span className="text-sm text-gray-600 dark:text-gray-400">Risk Score:</span>
                       <span className="text-sm font-medium text-gray-900 dark:text-white">{selectedTarget.aiRiskScore}/100</span>
                     </div>
                     <div className="flex justify-between">
                       <span className="text-sm text-gray-600 dark:text-gray-400">Vulnerabilities:</span>
                       <span className="text-sm font-medium text-gray-900 dark:text-white">{selectedTarget.vulnerabilities}</span>
                     </div>
                     <div className="flex justify-between">
                       <span className="text-sm text-gray-600 dark:text-gray-400">SBOM Available:</span>
                       <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                         selectedTarget.sbomAvailable 
                           ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300'
                           : 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300'
                       }`}>
                         {selectedTarget.sbomAvailable ? 'YES' : 'NO'}
                       </span>
                     </div>
                   </div>
                 </div>

                 <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                   <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">🛡️ Security Overview</h3>
                   <div className="space-y-3">
                     <div className="flex items-center justify-between">
                       <span className="text-sm text-gray-600 dark:text-gray-400">CVE Severity:</span>
                       <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getRiskColor(selectedTarget.cveSeverity)}`}>
                         {selectedTarget.cveSeverity.toUpperCase()}
                       </span>
                     </div>
                     <div className="flex items-center justify-between">
                       <span className="text-sm text-gray-600 dark:text-gray-400">Components:</span>
                       <span className="text-sm font-medium text-gray-900 dark:text-white">{selectedTarget.components.length}</span>
                     </div>
                     <div className="flex items-center justify-between">
                       <span className="text-sm text-gray-600 dark:text-gray-400">External Scripts:</span>
                       <span className="text-sm font-medium text-gray-900 dark:text-white">{selectedTarget.externalScripts.length}</span>
                     </div>
                     <div className="flex items-center justify-between">
                       <span className="text-sm text-gray-600 dark:text-gray-400">Security Headers:</span>
                       <span className="text-sm font-medium text-gray-900 dark:text-white">{selectedTarget.securityHeaders.length}</span>
                     </div>
                   </div>
                 </div>
               </div>

               {/* Technologies */}
               <div className="mb-6">
                 <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">🔧 Technologies Detected</h3>
                 <div className="flex flex-wrap gap-2">
                   {selectedTarget.technologies.map((tech, index) => (
                     <span key={index} className="px-3 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-300 rounded-full text-sm font-medium">
                       {tech}
                     </span>
                   ))}
                 </div>
               </div>

               {/* Components */}
               <div className="mb-6">
                 <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">📦 Detected Components</h3>
                 <div className="space-y-3">
                   {selectedTarget.components.map((component, index) => (
                     <div key={index} className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
                       <div className="flex items-center justify-between mb-2">
                         <div className="flex items-center space-x-2">
                           <span className="text-yellow-600 dark:text-yellow-400">📦</span>
                           <span className="font-medium text-yellow-800 dark:text-yellow-300">{component.name} v{component.version}</span>
                         </div>
                         <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(component.risk)}`}>
                           {component.risk.toUpperCase()}
                         </span>
                       </div>
                       <div className="text-sm text-yellow-700 dark:text-yellow-200">
                         <p>Type: {component.type}</p>
                         {component.cves.length > 0 && (
                           <p>CVEs: {component.cves.join(', ')}</p>
                         )}
                       </div>
                     </div>
                   ))}
                 </div>
               </div>

               {/* External Scripts */}
               {selectedTarget.externalScripts.length > 0 && (
                 <div className="mb-6">
                   <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">🚨 External Scripts</h3>
                   <div className="space-y-3">
                     {selectedTarget.externalScripts.map((script, index) => (
                       <div key={index} className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
                         <div className="flex items-center justify-between mb-2">
                           <div className="flex items-center space-x-2">
                             <span className="text-red-600 dark:text-red-400">🌐</span>
                             <span className="font-medium text-red-800 dark:text-red-300">{script.domain}</span>
                           </div>
                           <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(script.risk)}`}>
                             {script.risk.toUpperCase()}
                           </span>
                         </div>
                         <div className="text-sm text-red-700 dark:text-red-200 space-y-1">
                           <p><strong>URL:</strong> {script.url}</p>
                           <p><strong>Purpose:</strong> {script.purpose}</p>
                           <p><strong>Data Exposure:</strong> {script.dataExposure ? 'YES' : 'NO'}</p>
                         </div>
                       </div>
                     ))}
                   </div>
                 </div>
               )}

               {/* Security Headers */}
               <div className="mb-6">
                 <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">🔒 Security Headers</h3>
                 <div className="space-y-3">
                   {selectedTarget.securityHeaders.map((header, index) => (
                     <div key={index} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                       <div className="flex items-center justify-between mb-2">
                         <span className="font-medium text-gray-900 dark:text-white">{header.name}</span>
                         <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                           header.status === 'present' ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300' :
                           header.status === 'weak' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300' :
                           'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300'
                         }`}>
                           {header.status.toUpperCase()}
                         </span>
                       </div>
                       <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                         <p><strong>Value:</strong> {header.value || 'Not set'}</p>
                         <p><strong>Recommendation:</strong> {header.recommendation}</p>
                       </div>
                     </div>
                   ))}
                 </div>
               </div>

               {/* Action Buttons */}
               <div className="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
                 <div className="flex items-center space-x-4">
                   <button className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors duration-200">
                     🔄 Re-scan Domain
                   </button>
                   <button className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200">
                     📊 Generate Report
                   </button>
                   <button className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors duration-200">
                     📦 Download SBOM
                   </button>
                 </div>
                 <div className="flex items-center space-x-4">
                   <button className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors duration-200">
                     🔗 View Website
                   </button>
                   <button className="px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-medium transition-colors duration-200">
                     🚨 Report Issue
                   </button>
                 </div>
               </div>
             </div>
           </div>
         </div>
       )}
     </div>
   );
 };

export default WebScan; 