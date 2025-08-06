import React, { useState, useCallback } from 'react';
import { XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, Cell, Area, AreaChart } from 'recharts';

interface SummaryData {
  totalSboms: number;
  openVulnerabilities: {
    critical: number;
    total: number;
  };
  policyViolations: number;
  aiSuggestions: number;
}

interface TrendData {
  date: string;
  critical: number;
  high: number;
  medium: number;
  predicted: number;
}

interface ProjectCoverage {
  name: string;
  coverage: number;
  outdatedPackages: number;
  riskScore: number;
}

interface AtRiskRepo {
  name: string;
  riskScore: number;
  criticalVulns: number;
  aiNote: string;
}

interface AIRecommendation {
  id: string;
  title: string;
  description: string;
  impact: 'High' | 'Medium' | 'Low';
  affectedProjects: number;
}

interface SecurityMetrics {
  networkScans: number;
  webScans: number;
  directoryScans: number;
  osDetections: number;
  totalVulnerabilities: number;
  remediationProgress: number;
  complianceScore: number;
  threatIntelligence: number;
}

const Dashboard: React.FC = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [dragActive, setDragActive] = useState(false);
  const [selectedSeverity, setSelectedSeverity] = useState<string>('all');
  const [timeFilter, setTimeFilter] = useState<string>('30');

  // Mock data for summary cards - will be filtered based on time range
  const getSummaryData = (): SummaryData => {
    const days = parseInt(timeFilter);
    
    // Adjust summary data based on time filter
    const timeMultiplier = days / 30; // Base on 30 days
    
    return {
      totalSboms: Math.round(1202 * timeMultiplier),
      openVulnerabilities: {
        critical: Math.round(342 * timeMultiplier),
        total: Math.round(1040 * timeMultiplier)
      },
      policyViolations: Math.round(58 * timeMultiplier),
      aiSuggestions: Math.round(214 * timeMultiplier)
    };
  };

  const summaryData = getSummaryData();

  // Generate dynamic trend data based on current date
  const generateTrendData = (): TrendData[] => {
    const data: TrendData[] = [];
    const today = new Date();
    
    // Generate data for the last 90 days
    for (let i = 90; i >= 0; i -= 15) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      
      // Create realistic vulnerability data with some variation
      const baseCritical = 45 + Math.floor(Math.random() * 20);
      const baseHigh = 120 + Math.floor(Math.random() * 30);
      const baseMedium = 85 + Math.floor(Math.random() * 20);
      
      // Add some spikes for realism
      let critical = baseCritical;
      let high = baseHigh;
      let medium = baseMedium;
      let predicted = 0;
      
      // Create a spike around 30 days ago
      if (i === 30) {
        critical = 342;
        high = 180;
        medium = 105;
        predicted = 380;
      }
      
      // Add some future predictions
      if (i < 0) {
        predicted = 420 + Math.floor(Math.random() * 50);
      }
      
      data.push({
        date: date.toISOString().split('T')[0],
        critical,
        high,
        medium,
        predicted
      });
    }
    
    return data;
  };

  const allTrendData: TrendData[] = generateTrendData();

  // Filter trend data based on time filter
  const getFilteredTrendData = () => {
    const days = parseInt(timeFilter);
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    return allTrendData.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate >= cutoffDate;
    });
  };

  const trendData = getFilteredTrendData();

  // Mock data for SBOM coverage by project - filtered based on time range
  const getProjectCoverage = (): ProjectCoverage[] => {
    const days = parseInt(timeFilter);
    const timeMultiplier = days / 30;
    
    // Base coverage data - coverage percentages should remain realistic
    const baseData = [
      { name: 'Frontend API', baseCoverage: 87, baseOutdated: 12, baseRisk: 23 },
      { name: 'Backend Service', baseCoverage: 92, baseOutdated: 8, baseRisk: 15 },
      { name: 'Mobile App', baseCoverage: 78, baseOutdated: 18, baseRisk: 34 },
      { name: 'Admin Dashboard', baseCoverage: 95, baseOutdated: 5, baseRisk: 8 },
      { name: 'Data Pipeline', baseCoverage: 83, baseOutdated: 15, baseRisk: 28 }
    ];
    
    return baseData.map(project => {
      // Coverage should remain realistic (not scaled by time)
      const coverage = Math.min(100, project.baseCoverage + (days > 30 ? Math.floor(Math.random() * 5) : 0));
      
      // Outdated packages and risk scores can scale with time
      const outdatedPackages = Math.max(1, Math.round(project.baseOutdated * timeMultiplier));
      const riskScore = Math.min(100, Math.round(project.baseRisk * timeMultiplier));
      
      return {
        name: project.name,
        coverage,
        outdatedPackages,
        riskScore
      };
    });
  };

  const projectCoverage = getProjectCoverage();

  // Mock data for most at-risk repos - filtered based on time range
  const getAtRiskRepos = (): AtRiskRepo[] => {
    const days = parseInt(timeFilter);
    const timeMultiplier = days / 30; // Base on 30 days
    
    return [
      { 
        name: 'payment-service', 
        riskScore: Math.min(100, Math.round(92 * timeMultiplier)), 
        criticalVulns: Math.round(8 * timeMultiplier), 
        aiNote: 'High transitive risk due to log4j-core' 
      },
      { 
        name: 'user-auth-api', 
        riskScore: Math.min(100, Math.round(87 * timeMultiplier)), 
        criticalVulns: Math.round(6 * timeMultiplier), 
        aiNote: 'Multiple outdated Spring dependencies' 
      },
      { 
        name: 'data-processor', 
        riskScore: Math.min(100, Math.round(78 * timeMultiplier)), 
        criticalVulns: Math.round(4 * timeMultiplier), 
        aiNote: 'Apache Commons vulnerabilities detected' 
      },
      { 
        name: 'notification-service', 
        riskScore: Math.min(100, Math.round(65 * timeMultiplier)), 
        criticalVulns: Math.round(3 * timeMultiplier), 
        aiNote: 'Express.js path traversal risk' 
      },
      { 
        name: 'analytics-engine', 
        riskScore: Math.min(100, Math.round(58 * timeMultiplier)), 
        criticalVulns: Math.round(2 * timeMultiplier), 
        aiNote: 'Lodash prototype pollution detected' 
      }
    ];
  };

  const atRiskRepos = getAtRiskRepos();

  // Mock data for AI recommendations - filtered based on time range
  const getAIRecommendations = (): AIRecommendation[] => {
    const days = parseInt(timeFilter);
    const timeMultiplier = days / 30; // Base on 30 days
    
    return [
      { 
        id: '1', 
        title: 'Upgrade commons-io', 
        description: 'You should upgrade commons-io in 4 projects', 
        impact: 'High', 
        affectedProjects: Math.round(4 * timeMultiplier) 
      },
      { 
        id: '2', 
        title: 'Replace moment.js', 
        description: 'Consider replacing moment.js with dayjs in 3 projects', 
        impact: 'Medium', 
        affectedProjects: Math.round(3 * timeMultiplier) 
      },
      { 
        id: '3', 
        title: 'Update Spring Framework', 
        description: 'Update Spring Framework to latest version in 2 projects', 
        impact: 'High', 
        affectedProjects: Math.round(2 * timeMultiplier) 
      },
      { 
        id: '4', 
        title: 'Remove unused dependencies', 
        description: 'Remove 15 unused dependencies across projects', 
        impact: 'Low', 
        affectedProjects: Math.round(6 * timeMultiplier) 
      },
      { 
        id: '5', 
        title: 'Add security headers', 
        description: 'Implement security headers in 3 API projects', 
        impact: 'Medium', 
        affectedProjects: Math.round(3 * timeMultiplier) 
      }
    ];
  };

  const aiRecommendations = getAIRecommendations();

  // Get time-aware automation score data
  const getAutomationScoreData = () => {
    const days = parseInt(timeFilter);
    const timeMultiplier = days / 30; // Base on 30 days
    
    return {
      overall: Math.round(78 * timeMultiplier),
      critical: Math.round(85 * timeMultiplier),
      high: Math.round(72 * timeMultiplier),
      medium: Math.round(65 * timeMultiplier)
    };
  };

  const automationScoreData = getAutomationScoreData();

  // Mock data for security metrics
  const getSecurityMetrics = (): SecurityMetrics => {
    const days = parseInt(timeFilter);
    const timeMultiplier = days / 30;
    
    return {
      networkScans: Math.round(156 * timeMultiplier),
      webScans: Math.round(89 * timeMultiplier),
      directoryScans: Math.round(234 * timeMultiplier),
      osDetections: Math.round(67 * timeMultiplier),
      totalVulnerabilities: Math.round(1247 * timeMultiplier),
      remediationProgress: Math.round(78 * timeMultiplier),
      complianceScore: Math.round(92 * timeMultiplier),
      threatIntelligence: Math.round(156 * timeMultiplier)
    };
  };

  const securityMetrics = getSecurityMetrics();

  // Get risk score color
  const getRiskScoreColor = (score: number) => {
    if (score >= 80) return '#dc2626'; // Red
    if (score >= 60) return '#f97316'; // Orange
    if (score >= 40) return '#eab308'; // Yellow
    return '#22c55e'; // Green
  };

  // Get impact color
  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'High': return '#dc2626';
      case 'Medium': return '#f97316';
      case 'Low': return '#22c55e';
      default: return '#6b7280';
    }
  };

  // Get status color


  // Handle file upload
  const handleFileUpload = useCallback((files: FileList | null) => {
    if (!files || files.length === 0) return;

    setIsUploading(true);
    setUploadProgress(0);

    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          alert('SBOM uploaded successfully! AI analysis completed.');
          return 0;
        }
        return prev + 10;
      });
    }, 200);
  }, []);

  // Handle drag events
  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    handleFileUpload(e.dataTransfer.files);
  }, [handleFileUpload]);

  return (
    <div className="w-full h-full bg-gray-50 dark:bg-gray-900">
      <div className="w-full space-y-6 p-4 lg:p-6">
        {/* Enhanced Page Header with Quick Actions */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Security Dashboard</h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">AI-powered vulnerability analysis and threat intelligence</p>
              </div>
            </div>
            
            <div className="flex flex-col sm:flex-row items-start sm:items-center space-y-3 sm:space-y-0 sm:space-x-4">
              {/* Quick Actions */}
              <div className="flex items-center space-x-2">
                <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors duration-200 flex items-center space-x-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  <span>New Scan</span>
                </button>
                <button className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors duration-200 flex items-center space-x-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                  <span>Export Report</span>
                </button>
              </div>
              
              {/* Time Filter */}
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
                  <option value="365">Last year</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Key Metrics Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Critical Vulnerabilities */}
          <div className="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-800/20 rounded-2xl shadow-lg p-6 border border-red-200 dark:border-red-800 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-red-700 dark:text-red-300">Critical Vulnerabilities</p>
                <p className="text-3xl font-bold text-red-800 dark:text-red-200">{summaryData.openVulnerabilities.critical}</p>
                <div className="flex items-center mt-2">
                  <span className="text-xs text-red-600 dark:text-red-400">+15% this week</span>
                  <svg className="w-4 h-4 ml-1 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
              </div>
              <div className="p-3 bg-red-200 dark:bg-red-800/30 rounded-xl">
                <svg className="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
            </div>
          </div>

          {/* Total SBOMs */}
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-2xl shadow-lg p-6 border border-blue-200 dark:border-blue-800 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-700 dark:text-blue-300">SBOMs Analyzed</p>
                <p className="text-3xl font-bold text-blue-800 dark:text-blue-200">{summaryData.totalSboms.toLocaleString()}</p>
                <div className="flex items-center mt-2">
                  <span className="text-xs text-blue-600 dark:text-blue-400">+12% this month</span>
                  <svg className="w-4 h-4 ml-1 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
              </div>
              <div className="p-3 bg-blue-200 dark:bg-blue-800/30 rounded-xl">
                <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            </div>
          </div>

          {/* Security Score */}
          <div className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-2xl shadow-lg p-6 border border-green-200 dark:border-green-800 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-700 dark:text-green-300">Security Score</p>
                <p className="text-3xl font-bold text-green-800 dark:text-green-200">87%</p>
                <div className="flex items-center mt-2">
                  <span className="text-xs text-green-600 dark:text-green-400">+5% this week</span>
                  <svg className="w-4 h-4 ml-1 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
              </div>
              <div className="p-3 bg-green-200 dark:bg-green-800/30 rounded-xl">
                <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>

          {/* AI Insights */}
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 rounded-2xl shadow-lg p-6 border border-purple-200 dark:border-purple-800 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-purple-700 dark:text-purple-300">AI Insights</p>
                <p className="text-3xl font-bold text-purple-800 dark:text-purple-200">{summaryData.aiSuggestions}</p>
                <div className="flex items-center mt-2">
                  <span className="text-xs text-purple-600 dark:text-purple-400">New today</span>
                  <svg className="w-4 h-4 ml-1 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
              </div>
              <div className="p-3 bg-purple-200 dark:bg-purple-800/30 rounded-xl">
                <svg className="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Analytics & Trends Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Vulnerability Trend Chart */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Vulnerability Trends</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Last {timeFilter} days analysis</p>
              </div>
              <select
                value={selectedSeverity}
                onChange={(e) => setSelectedSeverity(e.target.value)}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Severities</option>
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
              </select>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis 
                  dataKey="date" 
                  stroke="#6b7280"
                  tick={{ fill: '#6b7280' }}
                  tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                />
                <YAxis stroke="#6b7280" tick={{ fill: '#6b7280' }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1f2937', 
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#f9fafb'
                  }}
                />
                <Legend />
                <Area type="monotone" dataKey="critical" stackId="1" stroke="#dc2626" fill="#dc2626" fillOpacity={0.6} name="Critical" />
                <Area type="monotone" dataKey="high" stackId="1" stroke="#f97316" fill="#f97316" fillOpacity={0.6} name="High" />
                <Area type="monotone" dataKey="medium" stackId="1" stroke="#eab308" fill="#eab308" fillOpacity={0.6} name="Medium" />
                <Area type="monotone" dataKey="predicted" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.3} strokeDasharray="5 5" name="AI Predicted" />
              </AreaChart>
            </ResponsiveContainer>
            <div className="mt-4 p-4 bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
              <div className="flex items-center space-x-2">
                <svg className="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                <p className="text-sm text-purple-800 dark:text-purple-400 font-medium">
                  AI detected anomaly: Critical vulnerabilities spiked 40% on March 30th
                </p>
              </div>
            </div>
          </div>

          {/* SBOM Coverage by Project */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Project Coverage</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">SBOM analysis across projects</p>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-xs text-gray-500 dark:text-gray-400">{projectCoverage.length} projects</span>
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={projectCoverage} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis type="number" domain={[0, 100]} stroke="#6b7280" tick={{ fill: '#6b7280' }} />
                <YAxis type="category" dataKey="name" stroke="#6b7280" tick={{ fill: '#6b7280' }} width={100} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1f2937', 
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#f9fafb'
                  }}
                  formatter={(value: any, _name: any, props: any) => [
                    `${value}% coverage`,
                    `${props.payload.outdatedPackages} outdated packages • Risk: ${props.payload.riskScore}`
                  ]}
                />
                <Bar dataKey="coverage" fill="#3b82f6" radius={[0, 4, 4, 0]}>
                  {projectCoverage.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={getRiskScoreColor(entry.riskScore)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
            <div className="mt-4 p-4 bg-gradient-to-r from-blue-50 to-green-50 dark:from-blue-900/20 dark:to-green-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
              <div className="flex items-center space-x-2">
                <svg className="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <p className="text-sm text-blue-800 dark:text-blue-400">
                  Coverage ranges from {Math.min(...projectCoverage.map(p => p.coverage))}% to {Math.max(...projectCoverage.map(p => p.coverage))}% across {projectCoverage.length} projects
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Most At-Risk Repos */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">📉 Most At-Risk Repos (Last {timeFilter} Days)</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {atRiskRepos.map((repo, _index) => (
              <div key={repo.name} className="p-4 border border-gray-200 dark:border-gray-700 rounded-xl hover:shadow-md transition-shadow duration-200">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900 dark:text-white">{repo.name}</h4>
                  <span 
                    className="px-2 py-1 rounded-full text-xs font-medium text-white"
                    style={{ backgroundColor: getRiskScoreColor(repo.riskScore) }}
                  >
                    {repo.riskScore}
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                  {repo.criticalVulns} critical vulnerabilities
                </p>
                <p className="text-xs text-blue-600 dark:text-blue-400">
                  🧠 {repo.aiNote}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Security Insights Quick Access */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-2xl shadow-lg p-6 border border-blue-200 dark:border-blue-800">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Security Insights</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Comprehensive vulnerability analysis across network, web, IoT, and human factors
                </p>
              </div>
            </div>
            <a
              href="/security-insights"
              className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg font-medium transition-all duration-200 transform hover:scale-105 shadow-lg"
            >
              View All Insights
            </a>
          </div>
          
          <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{securityMetrics.networkScans}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Network Scans</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">{securityMetrics.webScans}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Web Scans</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">{securityMetrics.directoryScans}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Directory Scans</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">{securityMetrics.osDetections}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">OS Detections</div>
            </div>
          </div>
        </div>

        {/* Directory Scanning & OS Detection */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        </div>

        {/* Security Metrics Overview */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">📊 Security Metrics Overview</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{securityMetrics.totalVulnerabilities}</div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Total Vulnerabilities</p>
              <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div className="bg-red-500 h-2 rounded-full" style={{ width: '65%' }}></div>
              </div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">{securityMetrics.remediationProgress}%</div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Remediation Progress</p>
              <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: `${securityMetrics.remediationProgress}%` }}></div>
              </div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">{securityMetrics.complianceScore}%</div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Compliance Score</p>
              <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div className="bg-purple-500 h-2 rounded-full" style={{ width: `${securityMetrics.complianceScore}%` }}></div>
              </div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">{securityMetrics.threatIntelligence}</div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Threat Intel Alerts</p>
              <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div className="bg-orange-500 h-2 rounded-full" style={{ width: '45%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* AI Summary Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Top AI Flagged Risks */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">🔎 Top AI Flagged Risks</h3>
            <div className="space-y-3">
              <div className="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg border-l-4 border-red-500">
                <p className="text-sm font-medium text-red-900 dark:text-red-300">Library log4j has shadow dependencies</p>
                <p className="text-xs text-red-700 dark:text-red-400">Found in 3 SBOMs</p>
              </div>
              <div className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg border-l-4 border-orange-500">
                <p className="text-sm font-medium text-orange-900 dark:text-orange-300">Spring Framework outdated</p>
                <p className="text-xs text-orange-700 dark:text-orange-400">5.3.x detected in 2 projects</p>
              </div>
              <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border-l-4 border-yellow-500">
                <p className="text-sm font-medium text-yellow-900 dark:text-yellow-300">Unused dependencies detected</p>
                <p className="text-xs text-yellow-700 dark:text-yellow-400">15 packages across 4 projects</p>
              </div>
            </div>
          </div>

          {/* AI Recommendations Carousel */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">🧠 AI Recommendations (Last {timeFilter} Days)</h3>
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {aiRecommendations.map((rec) => (
                <div key={rec.id} className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h4 className="text-sm font-medium text-gray-900 dark:text-white">{rec.title}</h4>
                      <p className="text-xs text-gray-600 dark:text-gray-300 mt-1">{rec.description}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{rec.affectedProjects} projects affected</p>
                    </div>
                    <span 
                      className="px-2 py-1 rounded-full text-xs font-medium text-white ml-2"
                      style={{ backgroundColor: getImpactColor(rec.impact) }}
                    >
                      {rec.impact}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Fix Automation Score */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">🛠️ Fix Automation Score (Last {timeFilter} Days)</h3>
            <div className="space-y-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600 dark:text-green-400">{automationScoreData.overall}%</div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Automatically Fixable</p>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Critical Vulnerabilities</span>
                  <span>{automationScoreData.critical}% fixable</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div className="bg-red-500 h-2 rounded-full" style={{ width: `${automationScoreData.critical}%` }}></div>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>High Vulnerabilities</span>
                  <span>{automationScoreData.high}% fixable</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div className="bg-orange-500 h-2 rounded-full" style={{ width: `${automationScoreData.high}%` }}></div>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Medium Vulnerabilities</span>
                  <span>{automationScoreData.medium}% fixable</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div className="bg-yellow-500 h-2 rounded-full" style={{ width: `${automationScoreData.medium}%` }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Upload Area */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
          <div className="text-center">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">📥 Upload New SBOM</h3>
            <div
              className={`border-2 border-dashed rounded-xl p-8 transition-all duration-200 ${
                dragActive 
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
                  : 'border-gray-300 dark:border-gray-600'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <div className="space-y-4">
                <div className="text-4xl">📄</div>
                <div>
                  <p className="text-lg font-medium text-gray-900 dark:text-white">
                    Drag and drop your SBOM file here
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                    Supports JSON, CycloneDX, SPDX formats
                  </p>
                </div>
                <div>
                  <label className="cursor-pointer">
                    <span className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200">
                      Or click to browse
                    </span>
                    <input
                      type="file"
                      className="hidden"
                      accept=".json,.xml,.spdx"
                      onChange={(e) => handleFileUpload(e.target.files)}
                    />
                  </label>
                </div>
                {isUploading && (
                  <div className="mt-4">
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full transition-all duration-200"
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">
                      Uploading... {uploadProgress}%
                    </p>
                  </div>
                )}
                <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <p className="text-sm text-green-800 dark:text-green-400">
                    🧠 AI Preview: 5 potential CVEs identified before scan
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 