import React, { useState, useEffect } from 'react';
import PageHeader from '../components/PageHeader';

interface Policy {
  id: string;
  name: string;
  description: string;
  scope: 'OSS' | 'Container' | 'Binary' | 'All';
  severity: 'Low' | 'Medium' | 'High' | 'Critical';
  status: 'Active' | 'Inactive';
  violationsDetected: number;
  lastEvaluated: string;
  autoFix: boolean;
  ruleDefinition: string;
  tags: string[];
}

interface PolicyStats {
  totalPolicies: number;
  violatedPolicies: number;
  compliantSBOMs: number;
  pendingReviews: number;
}

interface ComplianceData {
  compliant: number;
  violated: number;
  notEvaluated: number;
}

const PolicyEngine: React.FC = () => {
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [selectedPolicy, setSelectedPolicy] = useState<Policy | null>(null);
  const [showEditor, setShowEditor] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [showAIChat, setShowAIChat] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [filters, setFilters] = useState({
    severity: '',
    status: '',
    scope: '',
    search: ''
  });
  const [aiChatMessage, setAiChatMessage] = useState('');
  const [aiChatHistory, setAiChatHistory] = useState<Array<{type: 'user' | 'ai', message: string}>>([]);

  const [stats, _setStats] = useState<PolicyStats>({
    totalPolicies: 24,
    violatedPolicies: 7,
    compliantSBOMs: 156,
    pendingReviews: 3
  });

  const [complianceData, _setComplianceData] = useState<ComplianceData>({
    compliant: 156,
    violated: 23,
    notEvaluated: 12
  });

  // Mock data for policies
  const mockPolicies: Policy[] = [
    {
      id: '1',
      name: 'No Critical CVEs in Production',
      description: 'Prevents deployment of components with critical severity vulnerabilities',
      scope: 'OSS',
      severity: 'Critical',
      status: 'Active',
      violationsDetected: 3,
      lastEvaluated: '2024-01-15 14:30',
      autoFix: true,
      ruleDefinition: '{"severity": "Critical", "action": "block"}',
      tags: ['security', 'production']
    },
    {
      id: '2',
      name: 'License Compliance Check',
      description: 'Ensures all dependencies have approved licenses',
      scope: 'OSS',
      severity: 'High',
      status: 'Active',
      violationsDetected: 8,
      lastEvaluated: '2024-01-15 13:45',
      autoFix: false,
      ruleDefinition: '{"licenses": ["MIT", "Apache-2.0"], "action": "warn"}',
      tags: ['license', 'compliance']
    },
    {
      id: '3',
      name: 'Container Image Age Limit',
      description: 'Prevents use of container images older than 30 days',
      scope: 'Container',
      severity: 'Medium',
      status: 'Active',
      violationsDetected: 12,
      lastEvaluated: '2024-01-15 12:20',
      autoFix: true,
      ruleDefinition: '{"maxAge": "30d", "action": "warn"}',
      tags: ['container', 'security']
    },
    {
      id: '4',
      name: 'Dependency Update Policy',
      description: 'Requires dependencies to be updated within 90 days of new release',
      scope: 'OSS',
      severity: 'Medium',
      status: 'Active',
      violationsDetected: 15,
      lastEvaluated: '2024-01-15 11:15',
      autoFix: false,
      ruleDefinition: '{"updateWindow": "90d", "action": "notify"}',
      tags: ['maintenance', 'updates']
    },
    {
      id: '5',
      name: 'Binary Size Limit',
      description: 'Prevents binaries larger than 100MB from being deployed',
      scope: 'Binary',
      severity: 'Low',
      status: 'Inactive',
      violationsDetected: 0,
      lastEvaluated: '2024-01-10 09:30',
      autoFix: false,
      ruleDefinition: '{"maxSize": "100MB", "action": "block"}',
      tags: ['performance', 'deployment']
    }
  ];

  useEffect(() => {
    setPolicies(mockPolicies);
  }, []);

  // Filter policies based on current filters
  const filteredPolicies = policies.filter(policy => {
    if (filters.severity && policy.severity !== filters.severity) return false;
    if (filters.status && policy.status !== filters.status) return false;
    if (filters.scope && policy.scope !== filters.scope) return false;
    if (filters.search && !policy.name.toLowerCase().includes(filters.search.toLowerCase())) return false;
    return true;
  });

  // Pagination
  const totalPages = Math.ceil(filteredPolicies.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedPolicies = filteredPolicies.slice(startIndex, startIndex + itemsPerPage);

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
        return { bg: 'bg-green-100 dark:bg-green-900/20', text: 'text-green-800 dark:text-green-400', border: 'border-green-200 dark:border-green-800' };
      default:
        return { bg: 'bg-gray-100 dark:bg-gray-900/20', text: 'text-gray-800 dark:text-gray-400', border: 'border-gray-200 dark:border-gray-800' };
    }
  };

  // Get status styles
  const getStatusStyles = (status: string) => {
    switch (status) {
      case 'Active':
        return { bg: 'bg-green-100 dark:bg-green-900/20', text: 'text-green-800 dark:text-green-400' };
      case 'Inactive':
        return { bg: 'bg-gray-100 dark:bg-gray-900/20', text: 'text-gray-800 dark:text-gray-400' };
      default:
        return { bg: 'bg-gray-100 dark:bg-gray-900/20', text: 'text-gray-800 dark:text-gray-400' };
    }
  };

  // Handle policy actions
  const handleEditPolicy = (policy: Policy) => {
    setSelectedPolicy(policy);
    setIsEditing(true);
    setShowEditor(true);
  };

  const handleDeletePolicy = (policyId: string) => {
    if (confirm('Are you sure you want to delete this policy?')) {
      setPolicies(policies.filter(p => p.id !== policyId));
    }
  };

  const handleNewPolicy = () => {
    setSelectedPolicy(null);
    setIsEditing(false);
    setShowEditor(true);
  };

  const handleSavePolicy = (policyData: Partial<Policy>) => {
    if (isEditing && selectedPolicy) {
      setPolicies(policies.map(p => p.id === selectedPolicy.id ? { ...p, ...policyData } : p));
    } else {
      const newPolicy: Policy = {
        id: Date.now().toString(),
        name: policyData.name || '',
        description: policyData.description || '',
        scope: policyData.scope || 'OSS',
        severity: policyData.severity || 'Medium',
        status: policyData.status || 'Active',
        violationsDetected: 0,
        lastEvaluated: new Date().toLocaleString(),
        autoFix: policyData.autoFix || false,
        ruleDefinition: policyData.ruleDefinition || '{}',
        tags: policyData.tags || []
      };
      setPolicies([newPolicy, ...policies]);
    }
    setShowEditor(false);
  };

  const handleAIChat = () => {
    if (aiChatMessage.trim()) {
      const userMessage = { type: 'user' as const, message: aiChatMessage };
      setAiChatHistory([...aiChatHistory, userMessage]);
      
      // Simulate AI response
      setTimeout(() => {
        const aiResponse = { 
          type: 'ai' as const, 
          message: `I understand you're asking about: "${aiChatMessage}". Here's my analysis and recommendations...` 
        };
        setAiChatHistory(prev => [...prev, aiResponse]);
      }, 1000);
      
      setAiChatMessage('');
    }
  };

  return (
    <div className="w-full h-full bg-gray-50 dark:bg-gray-900">
      <div className="w-full h-full space-y-3 p-2 lg:p-4 overflow-y-auto">
        {/* Page Header */}
        <PageHeader
          title="Policy Engine"
          description="Define, manage, and enforce security policies across your SBOM ecosystem"
          icon={
            <svg className="w-6 h-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          }
          actions={
            <div className="flex flex-wrap gap-3">
              <button
                onClick={handleNewPolicy}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2"
              >
                <span>➕</span>
                <span>New Policy</span>
              </button>
              <button className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2">
                <span>🔄</span>
                <span>Evaluate All</span>
              </button>
              <button className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2">
                <span>🤖</span>
                <span>AI Suggest</span>
              </button>
            </div>
          }
        />

        {/* 1. Policy Summary Panel */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">🔢 Total Policies</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.totalPolicies}</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🔢</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">🔴 Violated Policies</p>
                <p className="text-3xl font-bold text-red-600 dark:text-red-400">{stats.violatedPolicies}</p>
              </div>
              <div className="w-12 h-12 bg-red-100 dark:bg-red-900/20 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🔴</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">✅ Compliant SBOMs</p>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400">{stats.compliantSBOMs}</p>
              </div>
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
                <span className="text-2xl">✅</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">⚠️ Pending Reviews</p>
                <p className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">{stats.pendingReviews}</p>
              </div>
              <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg flex items-center justify-center">
                <span className="text-2xl">⚠️</span>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Policy List Table */}
          <div className="flex-1">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <div className="flex flex-col lg:flex-row lg:justify-between lg:items-center space-y-4 lg:space-y-0">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">🧩 Policy List</h2>
                  
                  {/* Filters */}
                  <div className="flex flex-wrap gap-3">
                    <input
                      type="text"
                      placeholder="Search policies..."
                      value={filters.search}
                      onChange={(e) => setFilters({...filters, search: e.target.value})}
                      className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                    />
                    <select
                      value={filters.severity}
                      onChange={(e) => setFilters({...filters, severity: e.target.value})}
                      className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                    >
                      <option value="">All Severities</option>
                      <option value="Critical">Critical</option>
                      <option value="High">High</option>
                      <option value="Medium">Medium</option>
                      <option value="Low">Low</option>
                    </select>
                    <select
                      value={filters.status}
                      onChange={(e) => setFilters({...filters, status: e.target.value})}
                      className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                    >
                      <option value="">All Statuses</option>
                      <option value="Active">Active</option>
                      <option value="Inactive">Inactive</option>
                    </select>
                    <select
                      value={filters.scope}
                      onChange={(e) => setFilters({...filters, scope: e.target.value})}
                      className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                    >
                      <option value="">All Scopes</option>
                      <option value="OSS">OSS</option>
                      <option value="Container">Container</option>
                      <option value="Binary">Binary</option>
                      <option value="All">All</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Table */}
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Policy Name</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Severity</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Violations</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Last Evaluated</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                    {paginatedPolicies.map((policy) => {
                      const severityStyles = getSeverityStyles(policy.severity);
                      const statusStyles = getStatusStyles(policy.status);
                      
                      return (
                        <tr key={policy.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                          <td className="px-6 py-4">
                            <div>
                              <div className="text-sm font-medium text-gray-900 dark:text-white">{policy.name}</div>
                              <div className="text-sm text-gray-500 dark:text-gray-400">{policy.description}</div>
                              <div className="flex flex-wrap gap-1 mt-1">
                                {policy.tags.map((tag, index) => (
                                  <span key={index} className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 dark:bg-gray-600 text-gray-800 dark:text-gray-200">
                                    {tag}
                                  </span>
                                ))}
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${severityStyles.bg} ${severityStyles.text} ${severityStyles.border}`}>
                              {policy.severity}
                            </span>
                          </td>
                          <td className="px-6 py-4">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusStyles.bg} ${statusStyles.text}`}>
                              {policy.status}
                            </span>
                          </td>
                          <td className="px-6 py-4">
                            <div className="text-sm text-gray-900 dark:text-white">
                              {policy.violationsDetected}
                              {policy.violationsDetected > 0 && (
                                <button className="ml-2 text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 text-xs">
                                  View
                                </button>
                              )}
                            </div>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                            {policy.lastEvaluated}
                          </td>
                          <td className="px-6 py-4">
                            <div className="flex space-x-2">
                              <button
                                onClick={() => handleEditPolicy(policy)}
                                className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 text-sm font-medium"
                              >
                                Edit
                              </button>
                              <button
                                onClick={() => handleDeletePolicy(policy.id)}
                                className="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 text-sm font-medium"
                              >
                                Delete
                              </button>
                              <button className="text-green-600 dark:text-green-400 hover:text-green-800 dark:hover:text-green-300 text-sm font-medium">
                                Report
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {/* Pagination */}
              <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-gray-700 dark:text-gray-300">
                    Showing {startIndex + 1} to {Math.min(startIndex + itemsPerPage, filteredPolicies.length)} of {filteredPolicies.length} policies
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                      disabled={currentPage === 1}
                      className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Previous
                    </button>
                    <span className="px-3 py-1 text-sm text-gray-700 dark:text-gray-300">
                      Page {currentPage} of {totalPages}
                    </span>
                    <button
                      onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                      disabled={currentPage === totalPages}
                      className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Next
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="lg:w-80 space-y-6">
            {/* 4. Policy Compliance Analytics */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">📊 Compliance Analytics</h3>
              
              {/* Pie Chart */}
              <div className="mb-6">
                <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Compliance Distribution</h4>
                <div className="flex items-center justify-center h-32 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900 dark:text-white">
                      {Math.round((complianceData.compliant / (complianceData.compliant + complianceData.violated + complianceData.notEvaluated)) * 100)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Compliant</div>
                  </div>
                </div>
                <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400 mt-2">
                  <span>✅ {complianceData.compliant}</span>
                  <span>🔴 {complianceData.violated}</span>
                  <span>⚪ {complianceData.notEvaluated}</span>
                </div>
              </div>

              {/* Trends */}
              <div>
                <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Weekly Trends</h4>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-600 dark:text-gray-400">This Week</span>
                    <span className="text-xs font-medium text-green-600 dark:text-green-400">+12%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-600 dark:text-gray-400">Last Week</span>
                    <span className="text-xs font-medium text-red-600 dark:text-red-400">-3%</span>
                  </div>
                </div>
              </div>
            </div>

            {/* 5. AI Features Panel */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">🧠 AI Features</h3>
              
              <div className="space-y-4">
                <button className="w-full p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 text-left hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors duration-200">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">🤖</span>
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">Auto-Suggest Policies</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">AI-generated policy recommendations</div>
                    </div>
                  </div>
                </button>

                <button className="w-full p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800 text-left hover:bg-green-100 dark:hover:bg-green-900/30 transition-colors duration-200">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">💡</span>
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">Explain Policy Impact</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Understand policy effectiveness</div>
                    </div>
                  </div>
                </button>

                <button 
                  onClick={() => setShowAIChat(true)}
                  className="w-full p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800 text-left hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors duration-200"
                >
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">💬</span>
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">Chat With PolicyBot</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Ask questions about policies</div>
                    </div>
                  </div>
                </button>
              </div>
            </div>

            {/* 6. Settings & Sync */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">⚙️ Settings & Sync</h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700 dark:text-gray-300">GitHub Sync</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" defaultChecked />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700 dark:text-gray-300">Auto-Fix Mode</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700 dark:text-gray-300">Enforcement Mode</span>
                  <select className="px-2 py-1 text-xs border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
                    <option>Warning</option>
                    <option>Block Build</option>
                    <option>Notify Only</option>
                  </select>
                </div>

                <button className="w-full px-3 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg text-sm font-medium transition-colors duration-200">
                  ⬇️ Export Policies
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* 3. Policy Editor Modal */}
        {showEditor && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                {/* Modal Header */}
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                    {isEditing ? 'Edit Policy' : 'New Policy'}
                  </h2>
                  <button
                    onClick={() => setShowEditor(false)}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                {/* Policy Form */}
                <div className="space-y-6">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 lg:gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Policy Name</label>
                      <input
                        type="text"
                        defaultValue={selectedPolicy?.name || ''}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        placeholder="Enter policy name"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Scope</label>
                      <select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
                        <option value="OSS">OSS</option>
                        <option value="Container">Container</option>
                        <option value="Binary">Binary</option>
                        <option value="All">All</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Description</label>
                    <textarea
                      defaultValue={selectedPolicy?.description || ''}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                      placeholder="Describe the policy purpose and requirements"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Severity</label>
                      <select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
                        <option value="Low">Low</option>
                        <option value="Medium">Medium</option>
                        <option value="High">High</option>
                        <option value="Critical">Critical</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</label>
                      <select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
                        <option value="Active">Active</option>
                        <option value="Inactive">Inactive</option>
                      </select>
                    </div>
                    <div className="flex items-center">
                      <label className="flex items-center">
                        <input type="checkbox" className="mr-2" defaultChecked={selectedPolicy?.autoFix || false} />
                        <span className="text-sm text-gray-700 dark:text-gray-300">Auto-Fix</span>
                      </label>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Rule Definition (JSON)</label>
                    <textarea
                      defaultValue={selectedPolicy?.ruleDefinition || '{}'}
                      rows={6}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white font-mono text-sm"
                      placeholder='{"severity": "Critical", "action": "block"}'
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Tags</label>
                    <input
                      type="text"
                      defaultValue={selectedPolicy?.tags?.join(', ') || ''}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                      placeholder="security, production, compliance"
                    />
                  </div>

                  {/* AI Suggestions */}
                  <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                    <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-2">🤖 AI Suggestions</h4>
                    <p className="text-sm text-gray-700 dark:text-gray-300">
                      Based on your SBOM patterns, consider adding: "No outdated dependencies" and "License compliance check"
                    </p>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <button
                      onClick={() => handleSavePolicy({})}
                      className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200"
                    >
                      {isEditing ? 'Update Policy' : 'Create Policy'}
                    </button>
                    <button
                      onClick={() => setShowEditor(false)}
                      className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors duration-200"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* AI Chat Modal */}
        {showAIChat && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl max-w-2xl w-full max-h-[80vh] overflow-hidden">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white">💬 Chat with PolicyBot</h2>
                  <button
                    onClick={() => setShowAIChat(false)}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>

              {/* Chat Messages */}
              <div className="p-6 h-96 overflow-y-auto">
                {aiChatHistory.length === 0 ? (
                  <div className="text-center text-gray-500 dark:text-gray-400">
                    <p className="mb-4">Ask me anything about your policies!</p>
                    <div className="space-y-2 text-sm">
                      <p>• "Which policy failed most in July?"</p>
                      <p>• "Suggest new policies for container images"</p>
                      <p>• "What's the compliance trend this month?"</p>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {aiChatHistory.map((message, index) => (
                      <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                          message.type === 'user' 
                            ? 'bg-blue-600 text-white' 
                            : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                        }`}>
                          {message.message}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Chat Input */}
              <div className="p-6 border-t border-gray-200 dark:border-gray-700">
                <div className="flex space-x-3">
                  <input
                    type="text"
                    value={aiChatMessage}
                    onChange={(e) => setAiChatMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleAIChat()}
                    placeholder="Ask about your policies..."
                    className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  />
                  <button
                    onClick={handleAIChat}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200"
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PolicyEngine; 