import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';

// AI Analysis Interfaces
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
    type: 'upgrade' | 'remove' | 'replace' | 'add' | 'patch';
    package: string;
    description: string;
    currentVersion?: string;
    targetVersion?: string;
    replacement?: string;
  }[];
  estimatedTime: string;
  riskLevel: 'Low' | 'Medium' | 'High';
}

// GitHub Insights Interfaces
interface Repository {
  id: string;
  name: string;
  owner: string;
  language: string;
  dependencyCount: number;
  cveCount: number;
  riskScore: number;
  lastScanned: string;
  lastCommit: string;
  team: string;
  isActive: boolean;
  prCount: number;
  outdatedDeps: number;
}

interface PullRequest {
  id: string;
  title: string;
  repo: string;
  author: string;
  status: 'open' | 'merged' | 'closed';
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
  sbomChanges: boolean;
  dependencyChanges: string[];
  aiTags: string[];
  createdAt: string;
}

const AIRepositoryAnalysis: React.FC = () => {
  const [activeTab, setActiveTab] = useState('ai-analysis');
  const [aiQuery, setAiQuery] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [selectedPR, setSelectedPR] = useState<PullRequest | null>(null);
  const [showPRModal, setShowPRModal] = useState(false);
  const [showAIBot, setShowAIBot] = useState(false);
  const [botMessages, setBotMessages] = useState<Array<{ type: 'user' | 'bot'; content: string; timestamp: Date }>>([
    {
      type: 'bot',
      content: 'Hello! I\'m your AI Analysis Assistant. I can help you understand vulnerabilities, explain remediation strategies, and guide you through security insights. How can I help you today?',
      timestamp: new Date()
    }
  ]);
  const [botInput, setBotInput] = useState('');

  // Mock data for AI Analysis
  const summaryData = {
    analyzedSboms: 134,
    criticalVulns: 23,
    suggestions: 57
  };

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
    }
  ];

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
      name: 'react',
      usageTrend: 'stable',
      riskScore: 15,
      riskLevel: 'Low',
      fixAction: 'upgrade',
      currentVersion: '18.2.0',
      recommendedVersion: '18.3.0'
    },
    {
      name: 'axios',
      usageTrend: 'trending_up',
      riskScore: 45,
      riskLevel: 'Medium',
      fixAction: 'upgrade',
      currentVersion: '1.4.0',
      recommendedVersion: '1.6.0'
    },
    {
      name: 'lodash',
      usageTrend: 'trending_down',
      riskScore: 78,
      riskLevel: 'High',
      fixAction: 'replace',
      currentVersion: '4.17.21',
      replacement: 'ramda'
    }
  ];

  const fixPlans: FixPlan[] = [
    {
      id: 'plan-1',
      sbomId: 'sbom-123',
      actions: [
        {
          type: 'upgrade',
          package: 'react',
          description: 'Upgrade React to fix security vulnerabilities',
          currentVersion: '18.2.0',
          targetVersion: '18.3.0'
        }
      ],
      estimatedTime: '2 hours',
      riskLevel: 'Low'
    },
    {
      id: 'plan-2',
      sbomId: 'sbom-456',
      actions: [
        {
          type: 'patch',
          package: 'log4j-core',
          description: 'Critical security patch for log4j vulnerability',
          currentVersion: '2.17.0',
          targetVersion: '2.20.0'
        },
        {
          type: 'replace',
          package: 'lodash',
          description: 'Replace with safer alternative',
          currentVersion: '4.17.21',
          replacement: 'ramda'
        }
      ],
      estimatedTime: '4 hours',
      riskLevel: 'High'
    },
    {
      id: 'plan-3',
      sbomId: 'sbom-789',
      actions: [
        {
          type: 'upgrade',
          package: 'axios',
          description: 'Update HTTP client for better security',
          currentVersion: '1.4.0',
          targetVersion: '1.6.0'
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

  // Mock data for GitHub Insights
  const repositories: Repository[] = [
    {
      id: '1',
      name: 'ecommerce-api',
      owner: 'company',
      language: 'TypeScript',
      dependencyCount: 156,
      cveCount: 3,
      riskScore: 78,
      lastScanned: '2025-01-15T10:30:00Z',
      lastCommit: '2025-01-15T09:15:00Z',
      team: 'Backend',
      isActive: true,
      prCount: 5,
      outdatedDeps: 12
    },
    {
      id: '2',
      name: 'mobile-app',
      owner: 'company',
      language: 'Swift',
      dependencyCount: 89,
      cveCount: 1,
      riskScore: 45,
      lastScanned: '2025-01-14T16:45:00Z',
      lastCommit: '2025-01-14T14:20:00Z',
      team: 'Mobile',
      isActive: true,
      prCount: 3,
      outdatedDeps: 8
    }
  ];

  const pullRequests: PullRequest[] = [
    {
      id: 'pr-1',
      title: 'Fix critical vulnerability in log4j',
      repo: 'ecommerce-api',
      author: 'john.doe',
      status: 'open',
      riskLevel: 'critical',
      sbomChanges: true,
      dependencyChanges: ['log4j-core: 2.17.0 → 2.20.0'],
      aiTags: ['security', 'critical', 'automated-fix'],
      createdAt: '2025-01-15T08:00:00Z'
    }
  ];

  // Helper functions
  const getSeverityStyles = (severity: string) => {
    switch (severity) {
      case 'Critical': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'High': return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'Low': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  const getRiskLevelStyles = (riskLevel: string) => {
    switch (riskLevel) {
      case 'High': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'Low': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  const getUsageTrendIcon = (trend: string) => {
    switch (trend) {
      case 'trending_up':
        return (
          <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        );
      case 'trending_down':
        return (
          <svg className="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0v-8m0 8l-8-8-4 4-6-6" />
          </svg>
        );
      default:
        return (
          <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14" />
          </svg>
        );
    }
  };

  const getRiskColor = (score: number) => {
    if (score >= 80) return '#dc2626';
    if (score >= 60) return '#f97316';
    if (score >= 40) return '#eab308';
    return '#22c55e';
  };

  const handleAiQuery = () => {
    // Mock AI response
    setAiResponse('Based on the repository analysis, I recommend prioritizing the log4j vulnerability fix and implementing automated dependency scanning in your CI/CD pipeline.');
  };

  const handlePRDetails = (pr: PullRequest) => {
    setSelectedPR(pr);
    setShowPRModal(true);
  };

  const closePRModal = () => {
    setShowPRModal(false);
    setSelectedPR(null);
  };

  const handleBotMessage = (message: string) => {
    const userMessage = { type: 'user' as const, content: message, timestamp: new Date() };
    setBotMessages(prev => [...prev, userMessage]);
    setBotInput('');

    // Simulate bot response
    setTimeout(() => {
      const botResponse = generateBotResponse(message);
      const botMessage = { type: 'bot' as const, content: botResponse, timestamp: new Date() };
      setBotMessages(prev => [...prev, botMessage]);
    }, 1000);
  };

  const generateBotResponse = (userMessage: string): string => {
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes('vulnerability') || lowerMessage.includes('cve')) {
      return `I can see ${vulnerabilities.length} vulnerabilities in your analysis. The most critical one is CVE-2022-5678 affecting lodash, which should be addressed immediately. Would you like me to explain the remediation steps for any specific vulnerability?`;
    }
    
    if (lowerMessage.includes('dependency') || lowerMessage.includes('package')) {
      return `Your dependencies analysis shows ${dependencies.length} packages that need attention. The log4j-core package has a high-risk score of 92 and should be patched to version 2.20.0. I can help you understand the risk levels and recommended actions for each dependency.`;
    }
    
    if (lowerMessage.includes('fix') || lowerMessage.includes('remediation') || lowerMessage.includes('plan')) {
      return `I've generated ${fixPlans.length} fix plans for your security issues. The high-risk plan (plan-2) addresses the critical log4j vulnerability and lodash replacement, estimated to take 4 hours. Would you like me to walk you through the implementation steps?`;
    }
    
    if (lowerMessage.includes('risk') || lowerMessage.includes('score')) {
      return `Risk scores are calculated based on multiple factors including CVE severity, exploit availability, and potential impact. Scores above 80 are critical, 60-79 are high, 40-59 are medium, and below 40 are low. Your highest risk item is log4j-core with a score of 92.`;
    }
    
    if (lowerMessage.includes('ai') || lowerMessage.includes('analysis')) {
      return `The AI analysis has processed ${summaryData.analyzedSboms} SBOMs and identified ${summaryData.criticalVulns} critical vulnerabilities. The AI has provided ${summaryData.suggestions} actionable suggestions with 94% accuracy. The analysis uses machine learning to prioritize issues based on real-world threat intelligence.`;
    }
    
    if (lowerMessage.includes('help') || lowerMessage.includes('what can you do')) {
      return `I can help you with:\n• Understanding vulnerability details and severity\n• Explaining dependency risk scores and trends\n• Walking through fix plans and remediation steps\n• Interpreting AI analysis results\n• Providing security best practices\n\nJust ask me about any security concern!`;
    }
    
    return `I understand you're asking about "${userMessage}". I can help you understand vulnerabilities, dependencies, fix plans, and AI analysis results. Could you be more specific about what you'd like to know?`;
  };

  const tabs = [
    { id: 'ai-analysis', name: 'AI Analysis', icon: '🤖' },
    { id: 'repositories', name: 'Repositories', icon: '📁' },
    { id: 'pull-requests', name: 'Pull Requests', icon: '🔀' },
    { id: 'ai-insights', name: 'AI Insights', icon: '💡' }
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'ai-analysis':
        return (
          <div className="space-y-6">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                    <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Analyzed SBOMs</p>
                    <p className="text-2xl font-semibold text-gray-900 dark:text-white">{summaryData.analyzedSboms}</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="flex items-center">
                  <div className="p-2 bg-red-100 dark:bg-red-900 rounded-lg">
                    <svg className="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Critical Vulnerabilities</p>
                    <p className="text-2xl font-semibold text-gray-900 dark:text-white">{summaryData.criticalVulns}</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
                    <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">AI Suggestions</p>
                    <p className="text-2xl font-semibold text-gray-900 dark:text-white">{summaryData.suggestions}</p>
                  </div>
                </div>
              </div>
            </div>

                         {/* AI-Prioritized Vulnerabilities */}
             <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
               <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                 <h3 className="text-lg font-semibold text-gray-900 dark:text-white">AI-Prioritized Vulnerabilities</h3>
               </div>
               <div className="p-6">
                 <div className="space-y-4">
                   {vulnerabilities.map((vuln) => (
                     <div key={vuln.id} className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                       <div className="flex items-center space-x-4">
                         <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityStyles(vuln.severity)}`}>
                           {vuln.severity}
                         </span>
                         <div>
                           <p className="font-medium text-gray-900 dark:text-white">{vuln.component}</p>
                           <p className="text-sm text-gray-600 dark:text-gray-400">{vuln.id}</p>
                         </div>
                       </div>
                       <div className="text-right">
                         <p className="text-sm font-medium text-gray-900 dark:text-white">{vuln.aiSuggestion}</p>
                         <p className="text-xs text-gray-600 dark:text-gray-400">v{vuln.affectedVersion}</p>
                       </div>
                     </div>
                   ))}
                 </div>
               </div>
             </div>

             {/* Dependency Intelligence */}
             <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
               <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                 <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Dependency Intelligence</h3>
               </div>
               <div className="p-6">
                 <div className="space-y-4">
                   {dependencies.map((dep) => (
                     <div key={dep.name} className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                       <div className="flex items-center space-x-4">
                         <div className="flex items-center space-x-2">
                           {getUsageTrendIcon(dep.usageTrend)}
                           <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelStyles(dep.riskLevel)}`}>
                             {dep.riskLevel}
                           </span>
                         </div>
                         <div>
                           <p className="font-medium text-gray-900 dark:text-white">{dep.name}</p>
                           <p className="text-sm text-gray-600 dark:text-gray-400">v{dep.currentVersion}</p>
                         </div>
                       </div>
                       <div className="text-right">
                         <p className="text-sm font-medium text-gray-900 dark:text-white">{dep.fixAction}</p>
                         {dep.recommendedVersion && (
                           <p className="text-xs text-gray-600 dark:text-gray-400">→ v{dep.recommendedVersion}</p>
                         )}
                       </div>
                     </div>
                   ))}
                 </div>
               </div>
             </div>

             {/* AI-Generated Fix Plans */}
             <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
               <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                 <h3 className="text-lg font-semibold text-gray-900 dark:text-white">AI-Generated Fix Plans</h3>
               </div>
               <div className="p-6">
                 <div className="space-y-4">
                   {fixPlans.map((plan) => (
                     <div key={plan.id} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                       <div className="flex items-center justify-between mb-3">
                         <div className="flex items-center space-x-2">
                           <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelStyles(plan.riskLevel)}`}>
                             {plan.riskLevel} Risk
                           </span>
                           <span className="text-sm text-gray-600 dark:text-gray-400">SBOM: {plan.sbomId}</span>
                         </div>
                         <div className="text-right">
                           <p className="text-sm font-medium text-gray-900 dark:text-white">{plan.estimatedTime}</p>
                           <p className="text-xs text-gray-600 dark:text-gray-400">Estimated time</p>
                         </div>
                       </div>
                       <div className="space-y-2">
                         {plan.actions.map((action, index) => (
                           <div key={index} className="flex items-center space-x-3 p-2 bg-gray-50 dark:bg-gray-700 rounded">
                             <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                               action.type === 'upgrade' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' :
                               action.type === 'remove' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                               action.type === 'replace' ? 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200' :
                               'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                             }`}>
                               {action.type}
                             </span>
                             <div className="flex-1">
                               <p className="text-sm font-medium text-gray-900 dark:text-white">{action.package}</p>
                               <p className="text-xs text-gray-600 dark:text-gray-400">{action.description}</p>
                             </div>
                             {action.currentVersion && action.targetVersion && (
                               <div className="text-right">
                                 <p className="text-xs text-gray-600 dark:text-gray-400">v{action.currentVersion} → v{action.targetVersion}</p>
                               </div>
                             )}
                           </div>
                         ))}
                       </div>
                     </div>
                   ))}
                 </div>
               </div>
             </div>

             {/* AI Analysis Metrics */}
             <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
               <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                 <h3 className="text-lg font-semibold text-gray-900 dark:text-white">AI Analysis Metrics</h3>
               </div>
               <div className="p-6">
                 <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                   <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                     <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">94%</div>
                     <div className="text-sm text-gray-600 dark:text-gray-400">Accuracy Rate</div>
                   </div>
                   <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                     <div className="text-2xl font-bold text-green-600 dark:text-green-400">2.3s</div>
                     <div className="text-sm text-gray-600 dark:text-gray-400">Avg Response Time</div>
                   </div>
                   <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                     <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">156</div>
                     <div className="text-sm text-gray-600 dark:text-gray-400">Patterns Detected</div>
                   </div>
                   <div className="text-center p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                     <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">89%</div>
                     <div className="text-sm text-gray-600 dark:text-gray-400">Confidence Score</div>
                   </div>
                 </div>
               </div>
             </div>
          </div>
        );

      case 'repositories':
        return (
          <div className="space-y-6">
            {/* Repository Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="text-center">
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">{repositories.length}</p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Total Repositories</p>
                </div>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="text-center">
                  <p className="text-2xl font-bold text-red-600 dark:text-red-400">
                    {repositories.reduce((sum, repo) => sum + repo.cveCount, 0)}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Total CVEs</p>
                </div>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="text-center">
                  <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                    {repositories.reduce((sum, repo) => sum + repo.outdatedDeps, 0)}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Outdated Dependencies</p>
                </div>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="text-center">
                  <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                    {repositories.reduce((sum, repo) => sum + repo.prCount, 0)}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Active PRs</p>
                </div>
              </div>
            </div>

            {/* Repository List */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Repository Analysis</h3>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {repositories.map((repo) => (
                    <div key={repo.id} className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: getRiskColor(repo.riskScore) }}></div>
                        <div>
                          <p className="font-medium text-gray-900 dark:text-white">{repo.name}</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400">{repo.team} • {repo.language}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-900 dark:text-white">Risk: {repo.riskScore}</p>
                        <p className="text-xs text-gray-600 dark:text-gray-400">{repo.cveCount} CVEs, {repo.outdatedDeps} outdated</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );

      case 'pull-requests':
        return (
          <div className="space-y-6">
            {/* PR Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="text-center">
                  <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                    {pullRequests.filter(pr => pr.status === 'open').length}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Open PRs</p>
                </div>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="text-center">
                  <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                    {pullRequests.filter(pr => pr.status === 'merged').length}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Merged PRs</p>
                </div>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="text-center">
                  <p className="text-2xl font-bold text-red-600 dark:text-red-400">
                    {pullRequests.filter(pr => pr.riskLevel === 'critical').length}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Critical PRs</p>
                </div>
              </div>
            </div>

            {/* Pull Request List */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Pull Requests</h3>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {pullRequests.map((pr) => (
                    <div key={pr.id} className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer" onClick={() => handlePRDetails(pr)}>
                      <div className="flex items-center space-x-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelStyles(pr.riskLevel)}`}>
                          {pr.riskLevel}
                        </span>
                        <div>
                          <p className="font-medium text-gray-900 dark:text-white">{pr.title}</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400">{pr.repo} • {pr.author}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-900 dark:text-white">{pr.status}</p>
                        <p className="text-xs text-gray-600 dark:text-gray-400">{pr.aiTags.join(', ')}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );

      case 'ai-insights':
        return (
          <div className="space-y-6">
            {/* AI Query Interface */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">AI Security Assistant</h3>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Ask AI about your repositories and security
                    </label>
                    <div className="flex space-x-2">
                      <input
                        type="text"
                        value={aiQuery}
                        onChange={(e) => setAiQuery(e.target.value)}
                        placeholder="e.g., What are the most critical security issues in my repositories?"
                        className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      <button
                        onClick={handleAiQuery}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
                      >
                        Ask AI
                      </button>
                    </div>
                  </div>
                  
                  {aiResponse && (
                    <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                      <p className="text-sm text-blue-900 dark:text-blue-100">{aiResponse}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* AI Recommendations */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">AI Recommendations</h3>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  <div className="p-4 border border-yellow-200 dark:border-yellow-800 rounded-lg bg-yellow-50 dark:bg-yellow-900/20">
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mt-0.5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                      </svg>
                      <div>
                        <h4 className="font-medium text-yellow-900 dark:text-yellow-100">Critical: Update log4j-core</h4>
                        <p className="text-sm text-yellow-800 dark:text-yellow-200 mt-1">
                          Repository ecommerce-api has a critical vulnerability in log4j-core. Update to version 2.20.0 immediately.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-4 border border-blue-200 dark:border-blue-800 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <div>
                        <h4 className="font-medium text-blue-900 dark:text-blue-100">Recommendation: Enable automated scanning</h4>
                        <p className="text-sm text-blue-800 dark:text-blue-200 mt-1">
                          Implement automated dependency scanning in your CI/CD pipeline to catch vulnerabilities early.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return <div>Select a tab to view content</div>;
    }
  };

  return (
    <div className="w-full h-full bg-gray-50 dark:bg-gray-900">
      <div className="w-full space-y-6 p-4 lg:p-6">
        <PageHeader
          title="AI Analysis"
          description="Comprehensive AI-powered analysis of repositories, vulnerabilities, and security insights"
          icon={
            <svg className="w-6 h-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
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

      {/* PR Modal */}
      {showPRModal && selectedPR && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-2xl w-full mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Pull Request Details</h3>
              <button onClick={closePRModal} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white">{selectedPR.title}</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">{selectedPR.repo} • {selectedPR.author}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Status</p>
                  <p className="text-sm text-gray-900 dark:text-white">{selectedPR.status}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Risk Level</p>
                  <p className="text-sm text-gray-900 dark:text-white">{selectedPR.riskLevel}</p>
                </div>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Dependency Changes</p>
                <ul className="text-sm text-gray-900 dark:text-white mt-1">
                  {selectedPR.dependencyChanges.map((change, index) => (
                    <li key={index}>{change}</li>
                  ))}
                </ul>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300">AI Tags</p>
                <div className="flex flex-wrap gap-2 mt-1">
                  {selectedPR.aiTags.map((tag, index) => (
                    <span key={index} className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded-full">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
             )}

       {/* AI Analysis Assistant Bot */}
       <div className="fixed bottom-6 right-6 z-40">
         {showAIBot && (
           <div className="bg-white dark:bg-gray-800 rounded-lg shadow-2xl border border-gray-200 dark:border-gray-700 w-96 h-96 flex flex-col">
             {/* Bot Header */}
             <div className="bg-blue-600 text-white px-4 py-3 rounded-t-lg flex items-center justify-between">
               <div className="flex items-center space-x-2">
                 <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                   <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                   </svg>
                 </div>
                 <div>
                   <h3 className="font-semibold">AI Analysis Assistant</h3>
                   <p className="text-xs text-blue-100">Online</p>
                 </div>
               </div>
               <button
                 onClick={() => setShowAIBot(false)}
                 className="text-blue-100 hover:text-white transition-colors"
               >
                 <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                 </svg>
               </button>
             </div>

             {/* Chat Messages */}
             <div className="flex-1 overflow-y-auto p-4 space-y-3">
               {botMessages.map((message, index) => (
                 <div
                   key={index}
                   className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                 >
                   <div
                     className={`max-w-xs px-3 py-2 rounded-lg ${
                       message.type === 'user'
                         ? 'bg-blue-600 text-white'
                         : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                     }`}
                   >
                     <p className="text-sm whitespace-pre-line">{message.content}</p>
                     <p className="text-xs opacity-70 mt-1">
                       {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                     </p>
                   </div>
                 </div>
               ))}
             </div>

             {/* Input Area */}
             <div className="border-t border-gray-200 dark:border-gray-700 p-4">
               <div className="flex space-x-2">
                 <input
                   type="text"
                   value={botInput}
                   onChange={(e) => setBotInput(e.target.value)}
                   onKeyPress={(e) => {
                     if (e.key === 'Enter' && botInput.trim()) {
                       handleBotMessage(botInput.trim());
                     }
                   }}
                   placeholder="Ask about vulnerabilities, dependencies, or fix plans..."
                   className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                 />
                 <button
                   onClick={() => botInput.trim() && handleBotMessage(botInput.trim())}
                   disabled={!botInput.trim()}
                   className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                 >
                   <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                   </svg>
                 </button>
               </div>
             </div>
           </div>
         )}

         {/* Bot Toggle Button */}
         {!showAIBot && (
           <button
             onClick={() => setShowAIBot(true)}
             className="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-4 shadow-lg transition-colors duration-200"
           >
             <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
             </svg>
           </button>
         )}
       </div>
     </div>
   );
 };

export default AIRepositoryAnalysis; 