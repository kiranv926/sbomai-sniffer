import React, { useState, useMemo } from 'react';

interface Vulnerability {
  id: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  aiSuggestion: string;
  component: string;
  affectedVersion: string;
  fixedVersion?: string;
  status: 'open' | 'fixed' | 'ignored';
}

interface Dependency {
  name: string;
  usageTrend: 'trending_up' | 'trending_down' | 'stable';
  riskScore: number;
  riskLevel: 'High' | 'Medium' | 'Low';
  fixAction: 'patch' | 'upgrade' | 'replace' | 'ignore';
  currentVersion: string;
  recommendedVersion?: string;
  replacement?: string;
}

interface FixPlan {
  id: string;
  sbomId: string;
  actions: {
    type: 'upgrade' | 'remove' | 'replace' | 'add';
    package: string;
    description: string;
    currentVersion?: string;
    targetVersion?: string;
    replacement?: string;
  }[];
  estimatedTime: string;
  riskLevel: 'Low' | 'Medium' | 'High';
}

const AIAnalysis: React.FC = () => {
  const [dateRange, setDateRange] = useState('7');
  const [severityFilter, setSeverityFilter] = useState<string>('all');
  const [showRemediatedOnly, setShowRemediatedOnly] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFixPlan, setSelectedFixPlan] = useState<string | null>(null);

  // Mock data for summary cards
  const summaryData = {
    analyzedSboms: 134,
    criticalVulns: 23,
    suggestions: 57
  };

  // Mock data for AI-Prioritized Vulnerabilities
  const vulnerabilities: Vulnerability[] = [
    {
      id: 'CVE-2023-1234',
      severity: 'High',
      aiSuggestion: 'Upgrade to v1.5.2',
      component: 'react',
      affectedVersion: '18.2.0',
      fixedVersion: '18.3.0',
      status: 'open'
    },
    {
      id: 'CVE-2022-5678',
      severity: 'Critical',
      aiSuggestion: 'Replace with safer lib',
      component: 'lodash',
      affectedVersion: '4.17.21',
      fixedVersion: '4.17.22',
      status: 'open'
    },
    {
      id: 'CVE-2024-9012',
      severity: 'Medium',
      aiSuggestion: 'Apply patch from repo',
      component: 'axios',
      affectedVersion: '1.4.0',
      status: 'open'
    },
    {
      id: 'CVE-2023-3456',
      severity: 'Critical',
      aiSuggestion: 'Immediate upgrade required',
      component: 'express',
      affectedVersion: '4.18.2',
      fixedVersion: '4.19.0',
      status: 'fixed'
    }
  ];

  // Mock data for Dependency Intelligence
  const dependencies: Dependency[] = [
    {
      name: 'log4j-core',
      usageTrend: 'trending_down',
      riskScore: 92,
      riskLevel: 'High',
      fixAction: 'patch',
      currentVersion: '2.17.0',
      recommendedVersion: '2.20.0'
    },
    {
      name: 'lodash',
      usageTrend: 'stable',
      riskScore: 30,
      riskLevel: 'Low',
      fixAction: 'ignore',
      currentVersion: '4.17.21'
    },
    {
      name: 'express',
      usageTrend: 'trending_up',
      riskScore: 70,
      riskLevel: 'Medium',
      fixAction: 'upgrade',
      currentVersion: '4.18.2',
      recommendedVersion: '4.19.0'
    },
    {
      name: 'moment',
      usageTrend: 'trending_down',
      riskScore: 85,
      riskLevel: 'High',
      fixAction: 'replace',
      currentVersion: '2.29.4',
      replacement: 'dayjs'
    }
  ];

  // Mock data for AI Recommendations & Fix Plans
  const fixPlans: FixPlan[] = [
    {
      id: 'plan-001',
      sbomId: 'frontend-api.json',
      actions: [
        {
          type: 'upgrade',
          package: 'axios',
          description: 'Upgrade to latest secure version',
          currentVersion: '1.4.0',
          targetVersion: '1.6.0'
        },
        {
          type: 'remove',
          package: 'debug',
          description: 'Remove unused debug package'
        },
        {
          type: 'replace',
          package: 'moment',
          description: 'Replace with lighter alternative',
          currentVersion: '2.29.4',
          replacement: 'dayjs'
        }
      ],
      estimatedTime: '2 hours',
      riskLevel: 'Low'
    },
    {
      id: 'plan-002',
      sbomId: 'backend-service.json',
      actions: [
        {
          type: 'upgrade',
          package: 'express',
          description: 'Critical security upgrade',
          currentVersion: '4.18.2',
          targetVersion: '4.19.0'
        },
        {
          type: 'add',
          package: 'helmet',
          description: 'Add security headers middleware'
        }
      ],
      estimatedTime: '1 hour',
      riskLevel: 'Medium'
    }
  ];

  // Filter vulnerabilities
  const filteredVulnerabilities = useMemo(() => {
    return vulnerabilities.filter(vuln => {
      const matchesSeverity = severityFilter === 'all' || vuln.severity === severityFilter;
      const matchesStatus = !showRemediatedOnly || vuln.status === 'open';
      return matchesSeverity && matchesStatus;
    });
  }, [vulnerabilities, severityFilter, showRemediatedOnly]);

  // Filter dependencies
  const filteredDependencies = useMemo(() => {
    return dependencies.filter(dep => {
      const matchesSearch = dep.name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = !showRemediatedOnly || dep.fixAction !== 'ignore';
      return matchesSearch && matchesStatus;
    });
  }, [dependencies, searchTerm, showRemediatedOnly]);

  // Get severity styles
  const getSeverityStyles = (severity: string) => {
    switch (severity) {
      case 'Critical':
        return { bg: 'bg-red-100 dark:bg-red-900/20', text: 'text-red-800 dark:text-red-400', border: 'border-red-200 dark:border-red-800' };
      case 'High':
        return { bg: 'bg-orange-100 dark:bg-orange-900/20', text: 'text-orange-800 dark:text-orange-400', border: 'border-orange-200 dark:border-orange-800' };
      case 'Medium':
        return { bg: 'bg-yellow-100 dark:bg-yellow-900/20', text: 'text-yellow-800 dark:text-yellow-400', border: 'border-yellow-200 dark:border-yellow-800' };
      case 'Low':
        return { bg: 'bg-blue-100 dark:bg-blue-900/20', text: 'text-blue-800 dark:text-blue-400', border: 'border-blue-200 dark:border-blue-800' };
      default:
        return { bg: 'bg-gray-100 dark:bg-gray-900/20', text: 'text-gray-800 dark:text-gray-400', border: 'border-gray-200 dark:border-gray-800' };
    }
  };

  // Get risk level styles
  const getRiskLevelStyles = (riskLevel: string) => {
    switch (riskLevel) {
      case 'High':
        return { bg: 'bg-red-100 dark:bg-red-900/20', text: 'text-red-800 dark:text-red-400' };
      case 'Medium':
        return { bg: 'bg-yellow-100 dark:bg-yellow-900/20', text: 'text-yellow-800 dark:text-yellow-400' };
      case 'Low':
        return { bg: 'bg-green-100 dark:bg-green-900/20', text: 'text-green-800 dark:text-green-400' };
      default:
        return { bg: 'bg-gray-100 dark:bg-gray-900/20', text: 'text-gray-800 dark:text-gray-400' };
    }
  };

  // Get usage trend icon
  const getUsageTrendIcon = (trend: string) => {
    switch (trend) {
      case 'trending_up':
        return '📈';
      case 'trending_down':
        return '📉';
      case 'stable':
        return '➡️';
      default:
        return '❓';
    }
  };

  // Export report
  const exportReport = () => {
    alert('Exporting AI Analysis Report...');
  };

  // Refresh analysis
  const refreshAnalysis = () => {
    alert('Refreshing AI Analysis...');
  };

  // Apply fix plan
  const applyFixPlan = (planId: string) => {
    alert(`Applying fix plan ${planId} via GitHub PR...`);
  };

  return (
    <div className="w-full h-full bg-gray-50 dark:bg-gray-900 p-4 lg:p-6">
      <div className="w-full space-y-6">
        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white mb-2">🧠 AI Analysis</h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 mb-4">
            AI-powered vulnerability analysis and intelligent remediation suggestions
          </p>
          
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">📅 Date Range:</label>
              <select
                value={dateRange}
                onChange={(e) => setDateRange(e.target.value)}
                className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="1">Last 24 hours</option>
                <option value="7">Last 7 days</option>
                <option value="30">Last 30 days</option>
                <option value="90">Last 90 days</option>
              </select>
            </div>
            <button
              onClick={refreshAnalysis}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2"
            >
              <span>🔄</span>
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">✅ Analyzed SBOMs</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">{summaryData.analyzedSboms}</p>
              </div>
              <div className="p-3 bg-green-100 dark:bg-green-900/20 rounded-xl">
                <span className="text-2xl">📊</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">🚨 Critical Vulns</p>
                <p className="text-3xl font-bold text-red-600 dark:text-red-400">{summaryData.criticalVulns}</p>
              </div>
              <div className="p-3 bg-red-100 dark:bg-red-900/20 rounded-xl">
                <span className="text-2xl">⚠️</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">💡 Suggestions</p>
                <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">{summaryData.suggestions}</p>
              </div>
              <div className="p-3 bg-blue-100 dark:bg-blue-900/20 rounded-xl">
                <span className="text-2xl">💡</span>
              </div>
            </div>
          </div>
        </div>

        {/* Section 1: AI-Prioritized Vulnerabilities */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">📊 AI-Prioritized Vulnerabilities</h2>
            
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center space-y-4 sm:space-y-0">
              <div className="flex items-center space-x-4">
                <select
                  value={severityFilter}
                  onChange={(e) => setSeverityFilter(e.target.value)}
                  className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">All Severities</option>
                  <option value="Critical">Critical</option>
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={showRemediatedOnly}
                    onChange={(e) => setShowRemediatedOnly(e.target.checked)}
                    className="rounded border-gray-300 dark:border-gray-600"
                  />
                  <span className="text-sm text-gray-700 dark:text-gray-300">Show open only</span>
                </label>
              </div>
              <button
                onClick={exportReport}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors duration-200"
              >
                Export Report
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    ⚠️ Vulnerability
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    🔍 Severity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    💡 AI Suggestion
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    📦 Component
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    📅 Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {filteredVulnerabilities.map((vuln) => {
                  const severityStyles = getSeverityStyles(vuln.severity);
                  return (
                    <tr key={vuln.id} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900 dark:text-white">{vuln.id}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${severityStyles.bg} ${severityStyles.text} ${severityStyles.border}`}>
                          {vuln.severity}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-900 dark:text-white">{vuln.aiSuggestion}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900 dark:text-white">{vuln.component}</div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">{vuln.affectedVersion}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          vuln.status === 'fixed' 
                            ? 'bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-400'
                            : vuln.status === 'ignored'
                            ? 'bg-gray-100 dark:bg-gray-900/20 text-gray-800 dark:text-gray-400'
                            : 'bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-400'
                        }`}>
                          {vuln.status}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Section 2: Dependency Intelligence */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">🔄 Dependency Intelligence</h2>
            
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center space-y-4 sm:space-y-0">
              <div className="flex items-center space-x-4">
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={showRemediatedOnly}
                    onChange={(e) => setShowRemediatedOnly(e.target.checked)}
                    className="rounded border-gray-300 dark:border-gray-600"
                  />
                  <span className="text-sm text-gray-700 dark:text-gray-300">✅ Show remediated only</span>
                </label>
              </div>
              <div className="relative">
                <input
                  type="text"
                  placeholder="🔍 Search packages..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <svg className="absolute left-3 top-2.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    📦 Package Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    📈 Usage Trend
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    ⚠️ Risk Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    🔁 Fix
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {filteredDependencies.map((dep) => {
                  const riskStyles = getRiskLevelStyles(dep.riskLevel);
                  return (
                    <tr key={dep.name} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900 dark:text-white">{dep.name}</div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">v{dep.currentVersion}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center space-x-2">
                          <span className="text-lg">{getUsageTrendIcon(dep.usageTrend)}</span>
                          <span className="text-sm text-gray-900 dark:text-white capitalize">
                            {dep.usageTrend.replace('_', ' ')}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center space-x-2">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${riskStyles.bg} ${riskStyles.text}`}>
                            {dep.riskScore}% {dep.riskLevel} Risk
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          dep.fixAction === 'patch' 
                            ? 'bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-400'
                            : dep.fixAction === 'upgrade'
                            ? 'bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-400'
                            : dep.fixAction === 'replace'
                            ? 'bg-orange-100 dark:bg-orange-900/20 text-orange-800 dark:text-orange-400'
                            : 'bg-gray-100 dark:bg-gray-900/20 text-gray-800 dark:text-gray-400'
                        }`}>
                          {dep.fixAction}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Section 3: AI Recommendations & Fix Plans */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">💡 AI Recommendations & Fix Plans</h2>
          </div>

          <div className="p-6 space-y-4">
            {fixPlans.map((plan) => (
              <div key={plan.id} className="border border-gray-200 dark:border-gray-700 rounded-xl p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      ✅ Auto-Generated Fix Plan for SBOM: {plan.sbomId}
                    </h3>
                    <div className="flex items-center space-x-4 mt-2 text-sm text-gray-600 dark:text-gray-300">
                      <span>⏱️ Estimated Time: {plan.estimatedTime}</span>
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        plan.riskLevel === 'High' 
                          ? 'bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-400'
                          : plan.riskLevel === 'Medium'
                          ? 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-400'
                          : 'bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-400'
                      }`}>
                        Risk: {plan.riskLevel}
                      </span>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => setSelectedFixPlan(selectedFixPlan === plan.id ? null : plan.id)}
                      className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors duration-200"
                    >
                      📝 Review Plan
                    </button>
                    <button
                      onClick={() => applyFixPlan(plan.id)}
                      className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors duration-200"
                    >
                      ⚙️ Apply via GitHub PR
                    </button>
                  </div>
                </div>

                {selectedFixPlan === plan.id && (
                  <div className="mt-4 space-y-3">
                    {plan.actions.map((action, index) => (
                      <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <span className="text-lg">
                          {action.type === 'upgrade' ? '⬆️' : 
                           action.type === 'remove' ? '🗑️' : 
                           action.type === 'replace' ? '🔄' : '➕'}
                        </span>
                        <div className="flex-1">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">
                            {action.type === 'upgrade' && `${action.package} → ${action.targetVersion}`}
                            {action.type === 'remove' && `Remove ${action.package}`}
                            {action.type === 'replace' && `${action.package} → ${action.replacement}`}
                            {action.type === 'add' && `Add ${action.package}`}
                          </div>
                          <div className="text-xs text-gray-600 dark:text-gray-300">
                            {action.description}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* AI Suggestion Types Sidebar */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">🧠 AI Suggestion Types:</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center space-x-3">
              <span className="text-lg">🔍</span>
              <span className="text-sm text-gray-700 dark:text-gray-300">Version Upgrade Recommendations</span>
            </div>
            <div className="flex items-center space-x-3">
              <span className="text-lg">🔄</span>
              <span className="text-sm text-gray-700 dark:text-gray-300">Library Substitutions</span>
            </div>
            <div className="flex items-center space-x-3">
              <span className="text-lg">📉</span>
              <span className="text-sm text-gray-700 dark:text-gray-300">Risk Mitigation Actions</span>
            </div>
            <div className="flex items-center space-x-3">
              <span className="text-lg">🧪</span>
              <span className="text-sm text-gray-700 dark:text-gray-300">Suggested Tests to Add</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAnalysis; 