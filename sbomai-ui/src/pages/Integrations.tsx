import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';

interface Integration {
  id: string;
  name: string;
  category: string;
  status: 'connected' | 'not-installed' | 'not-connected';
  description: string;
  icon: string;
  details?: string;
  actions: {
    primary: string;
    secondary?: string;
    tertiary?: string;
  };
}

const Integrations: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const integrations: Integration[] = [
    // Developer Tools (IDE)
    {
      id: 'vscode',
      name: 'VSCode Plugin',
      category: 'Developer Tools',
      status: 'connected',
      description: 'IDE integration for real-time SBOM analysis',
      icon: '🧩',
      details: 'Installed ✅',
      actions: { primary: 'Configure', secondary: 'Docs' }
    },
    {
      id: 'intellij',
      name: 'IntelliJ Plugin',
      category: 'Developer Tools',
      status: 'not-installed',
      description: 'JetBrains IDE integration',
      icon: '🟠',
      actions: { primary: 'Install' }
    },
    {
      id: 'eclipse',
      name: 'Eclipse',
      category: 'Developer Tools',
      status: 'not-installed',
      description: 'Eclipse IDE integration',
      icon: '⚪',
      actions: { primary: 'Install' }
    },
    // Source Control
    {
      id: 'github',
      name: 'GitHub',
      category: 'Source Control',
      status: 'connected',
      description: 'GitHub repository integration',
      icon: '🔗',
      details: '3 repos connected',
      actions: { primary: 'Configure' }
    },
    {
      id: 'gitlab',
      name: 'GitLab',
      category: 'Source Control',
      status: 'not-connected',
      description: 'GitLab repository integration',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    {
      id: 'bitbucket',
      name: 'Bitbucket',
      category: 'Source Control',
      status: 'not-connected',
      description: 'Bitbucket repository integration',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    // CI/CD Pipelines
    {
      id: 'github-actions',
      name: 'GitHub Actions',
      category: 'CI/CD Pipelines',
      status: 'connected',
      description: 'GitHub Actions pipeline integration',
      icon: '⚙️',
      details: 'Synced Daily',
      actions: { primary: 'Configure' }
    },
    {
      id: 'jenkins',
      name: 'Jenkins',
      category: 'CI/CD Pipelines',
      status: 'not-connected',
      description: 'Jenkins pipeline integration',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    {
      id: 'circleci',
      name: 'CircleCI',
      category: 'CI/CD Pipelines',
      status: 'not-connected',
      description: 'CircleCI pipeline integration',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    {
      id: 'gitlab-ci',
      name: 'GitLab CI',
      category: 'CI/CD Pipelines',
      status: 'not-connected',
      description: 'GitLab CI/CD integration',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    // Package Registries
    {
      id: 'npm',
      name: 'npm',
      category: 'Package Registries',
      status: 'connected',
      description: 'npm package registry integration',
      icon: '📦',
      details: '2 orgs monitored',
      actions: { primary: 'Configure' }
    },
    {
      id: 'maven',
      name: 'Maven Central',
      category: 'Package Registries',
      status: 'not-connected',
      description: 'Maven Central repository integration',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    {
      id: 'pypi',
      name: 'PyPI',
      category: 'Package Registries',
      status: 'not-connected',
      description: 'Python Package Index integration',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    // Security Feeds
    {
      id: 'nvd',
      name: 'NVD',
      category: 'Security Feeds',
      status: 'connected',
      description: 'National Vulnerability Database feed',
      icon: '🛡️',
      details: 'Default Feed Active',
      actions: { primary: 'Configure' }
    },
    {
      id: 'snyk',
      name: 'Snyk',
      category: 'Security Feeds',
      status: 'not-connected',
      description: 'Snyk vulnerability database',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    {
      id: 'osv',
      name: 'OSV',
      category: 'Security Feeds',
      status: 'not-connected',
      description: 'Open Source Vulnerabilities database',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    // Issue Trackers
    {
      id: 'jira',
      name: 'Jira',
      category: 'Issue Trackers',
      status: 'connected',
      description: 'Jira issue tracking integration',
      icon: '📝',
      details: 'Connected',
      actions: { primary: 'Map Fields' }
    },
    {
      id: 'github-issues',
      name: 'GitHub Issues',
      category: 'Issue Trackers',
      status: 'not-connected',
      description: 'GitHub Issues integration',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    // Alerting / Notifications
    {
      id: 'slack',
      name: 'Slack',
      category: 'Alerting / Notifications',
      status: 'connected',
      description: 'Slack notification integration',
      icon: '📢',
      details: '#sbom-alerts channel',
      actions: { primary: 'Manage' }
    },
    {
      id: 'teams',
      name: 'Microsoft Teams',
      category: 'Alerting / Notifications',
      status: 'not-connected',
      description: 'Microsoft Teams integration',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    {
      id: 'email',
      name: 'Email Alerts',
      category: 'Alerting / Notifications',
      status: 'not-connected',
      description: 'Email notification system',
      icon: '⚪',
      actions: { primary: 'Configure' }
    },
    // Runtime Monitoring
    {
      id: 'kubernetes',
      name: 'Kubernetes',
      category: 'Runtime Monitoring',
      status: 'not-connected',
      description: 'Kubernetes cluster monitoring',
      icon: '🚀',
      actions: { primary: 'Install Agent' }
    },
    {
      id: 'aws-lambda',
      name: 'AWS Lambda',
      category: 'Runtime Monitoring',
      status: 'not-connected',
      description: 'AWS Lambda function monitoring',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    {
      id: 'docker',
      name: 'Docker Runtime',
      category: 'Runtime Monitoring',
      status: 'not-connected',
      description: 'Docker container monitoring',
      icon: '⚪',
      actions: { primary: 'Connect' }
    },
    // Reporting / Export
    {
      id: 'pdf-export',
      name: 'Export as PDF',
      category: 'Reporting / Export',
      status: 'connected',
      description: 'PDF report generation',
      icon: '📊',
      actions: { primary: 'Configure Template' }
    },
    {
      id: 'webhook',
      name: 'Webhook Delivery',
      category: 'Reporting / Export',
      status: 'connected',
      description: 'Webhook notification delivery',
      icon: '📊',
      actions: { primary: 'Set Destination' }
    },
    {
      id: 'embed-dashboard',
      name: 'Embed in Dashboard',
      category: 'Reporting / Export',
      status: 'not-connected',
      description: 'Embed reports in external dashboards',
      icon: '⚪',
      actions: { primary: 'Get Snippet' }
    }
  ];

  const categories = ['all', ...Array.from(new Set(integrations.map(i => i.category)))];

  const filteredIntegrations = integrations.filter(integration => {
    const matchesSearch = integration.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         integration.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || integration.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected': return 'text-green-500';
      case 'not-installed': return 'text-orange-500';
      case 'not-connected': return 'text-gray-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected': return '✔️';
      case 'not-installed': return '🟠';
      case 'not-connected': return '⚪';
      default: return '⚪';
    }
  };

  const [selectedRecommendation, setSelectedRecommendation] = useState<number | null>(null);

  const aiRecommendations = [
    {
      id: 1,
      title: "Connect GitLab CI for your `backend-api` project",
      description: "Your backend-api project is missing CI/CD integration. GitLab CI would provide automated SBOM generation and vulnerability scanning on every commit.",
      benefits: [
        "Automated SBOM generation on code changes",
        "Real-time vulnerability detection in CI pipeline",
        "Block deployments with critical vulnerabilities",
        "Integration with existing GitLab workflow"
      ],
      impact: "High",
      effort: "Medium",
      category: "CI/CD Pipelines"
    },
    {
      id: 2,
      title: "You're missing real-time alerts for Slack in Production",
      description: "Production environments need immediate notification of security issues. Slack integration would provide instant alerts for critical vulnerabilities.",
      benefits: [
        "Instant notification of critical vulnerabilities",
        "Customizable alert channels (#security, #devops)",
        "Integration with existing Slack workspace",
        "Reduced time to respond to security threats"
      ],
      impact: "High",
      effort: "Low",
      category: "Alerting / Notifications"
    },
    {
      id: 3,
      title: "Only 30% of your dependencies are covered by OSS Index – consider adding Snyk",
      description: "Your current vulnerability coverage is limited. Adding Snyk would significantly expand your security monitoring across more package ecosystems.",
      benefits: [
        "Expanded vulnerability database coverage",
        "Support for npm, Maven, PyPI, and more",
        "Advanced vulnerability scoring and prioritization",
        "Integration with existing security workflows"
      ],
      impact: "Medium",
      effort: "Low",
      category: "Security Feeds"
    },
    {
      id: 4,
      title: "Enable Kubernetes monitoring for container security",
      description: "Your containerized applications lack runtime security monitoring. Kubernetes integration would provide real-time container vulnerability scanning.",
      benefits: [
        "Real-time container vulnerability scanning",
        "Runtime security monitoring",
        "Integration with Kubernetes RBAC",
        "Automated security policy enforcement"
      ],
      impact: "High",
      effort: "High",
      category: "Runtime Monitoring"
    },
    {
      id: 5,
      title: "Connect Jira for automated issue creation",
      description: "Manual vulnerability tracking is inefficient. Jira integration would automatically create and assign security issues to the appropriate teams.",
      benefits: [
        "Automated issue creation for vulnerabilities",
        "Integration with existing Jira workflows",
        "Custom field mapping for security data",
        "Improved team collaboration on security issues"
      ],
      impact: "Medium",
      effort: "Medium",
      category: "Issue Trackers"
    }
  ];

  return (
    <div className="w-full h-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
                    <div className="px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <PageHeader
          title="Integrations"
          description="Connect and manage your development tools, services, and platforms"
          icon={
            <svg className="w-6 h-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
          }
        />

        {/* Search and Filter Bar */}
        <div className="flex flex-col lg:flex-row gap-4 mb-8">
          <div className="flex-1">
            <div className="relative">
              <input
                type="text"
                placeholder="Search integrations..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-3 pl-12 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:text-white"
              />
              <div className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400">
                🔍
              </div>
            </div>
          </div>
          <div className="flex gap-2">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:text-white"
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category === 'all' ? 'All Categories' : category}
                </option>
              ))}
            </select>
            <button className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-all duration-200 flex items-center space-x-2">
              <span>➕</span>
              <span>Connect New</span>
            </button>
          </div>
        </div>

        {/* Integrations Grid */}
        <div className="space-y-8">
          {categories.filter(cat => cat !== 'all').map(category => {
            const categoryIntegrations = filteredIntegrations.filter(i => i.category === category);
            if (categoryIntegrations.length === 0) return null;

            return (
              <div key={category} className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
                {/* Category Header */}
                <div className="bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-600 px-6 py-4 border-b border-gray-200 dark:border-gray-600">
                  <h2 className="text-xl font-semibold text-gray-800 dark:text-white">
                    {category}
                  </h2>
                </div>

                {/* Category Items */}
                <div className="p-6">
                  <div className="grid gap-4">
                    {categoryIntegrations.map(integration => (
                      <div key={integration.id} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
                        <div className="flex items-center space-x-4">
                          <div className="text-2xl">{integration.icon}</div>
                          <div className="flex-1">
                            <div className="flex items-center space-x-2">
                              <h3 className="font-medium text-gray-900 dark:text-white">
                                {integration.name}
                              </h3>
                              <span className={`text-sm ${getStatusColor(integration.status)}`}>
                                {getStatusIcon(integration.status)}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                              {integration.description}
                            </p>
                            {integration.details && (
                              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                {integration.details}
                              </p>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-md transition-colors duration-200">
                            {integration.actions.primary}
                          </button>
                          {integration.actions.secondary && (
                            <button className="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-700 dark:text-gray-200 text-sm rounded-md transition-colors duration-200">
                              {integration.actions.secondary}
                            </button>
                          )}
                          {integration.actions.tertiary && (
                            <button className="px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-600 dark:text-gray-300 text-sm rounded-md transition-colors duration-200">
                              {integration.actions.tertiary}
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* AI Recommendations */}
        <div className="mt-8 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-xl p-6 border border-blue-200 dark:border-blue-700">
          <div className="flex items-center space-x-3 mb-4">
            <span className="text-2xl">🤖</span>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
              AI Recommendations
            </h3>
          </div>
          <div className="space-y-3">
            {aiRecommendations.map((recommendation) => (
              <div key={recommendation.id} className="flex items-start space-x-3 p-4 bg-white dark:bg-gray-800 rounded-lg border border-blue-200 dark:border-blue-700 hover:shadow-md transition-shadow duration-200">
                <span className="text-blue-500 mt-1">💡</span>
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-1">
                    {recommendation.title}
                  </h4>
                  <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                    {recommendation.description}
                  </p>
                  <div className="flex items-center space-x-4 text-xs">
                    <span className={`px-2 py-1 rounded-full ${
                      recommendation.impact === 'High' ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400' :
                      recommendation.impact === 'Medium' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400' :
                      'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
                    }`}>
                      Impact: {recommendation.impact}
                    </span>
                    <span className={`px-2 py-1 rounded-full ${
                      recommendation.effort === 'High' ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400' :
                      recommendation.effort === 'Medium' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400' :
                      'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
                    }`}>
                      Effort: {recommendation.effort}
                    </span>
                    <span className="text-gray-500 dark:text-gray-400">
                      {recommendation.category}
                    </span>
                  </div>
                </div>
                <div className="flex flex-col space-y-2">
                  <button 
                    onClick={() => setSelectedRecommendation(recommendation.id)}
                    className="px-3 py-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-700 dark:text-gray-200 text-sm rounded-md transition-colors duration-200"
                  >
                    View Details
                  </button>
                  <button className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-md transition-colors duration-200">
                    Connect
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recommendation Details Modal */}
        {selectedRecommendation && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                    🤖 AI Recommendation Details
                  </h3>
                  <button
                    onClick={() => setSelectedRecommendation(null)}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors duration-200"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                
                {(() => {
                  const recommendation = aiRecommendations.find(r => r.id === selectedRecommendation);
                  if (!recommendation) return null;
                  
                  return (
                    <div className="space-y-6">
                      {/* Header */}
                      <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-4">
                        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                          {recommendation.title}
                        </h4>
                        <p className="text-gray-700 dark:text-gray-300">
                          {recommendation.description}
                        </p>
                      </div>

                      {/* Metadata */}
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
                          <div className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Impact</div>
                          <div className={`text-lg font-semibold ${
                            recommendation.impact === 'High' ? 'text-red-600 dark:text-red-400' :
                            recommendation.impact === 'Medium' ? 'text-yellow-600 dark:text-yellow-400' :
                            'text-green-600 dark:text-green-400'
                          }`}>
                            {recommendation.impact}
                          </div>
                        </div>
                        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
                          <div className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Effort</div>
                          <div className={`text-lg font-semibold ${
                            recommendation.effort === 'High' ? 'text-red-600 dark:text-red-400' :
                            recommendation.effort === 'Medium' ? 'text-yellow-600 dark:text-yellow-400' :
                            'text-green-600 dark:text-green-400'
                          }`}>
                            {recommendation.effort}
                          </div>
                        </div>
                        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
                          <div className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Category</div>
                          <div className="text-lg font-semibold text-gray-900 dark:text-white">
                            {recommendation.category}
                          </div>
                        </div>
                      </div>

                      {/* Benefits */}
                      <div>
                        <h5 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                          🎯 Key Benefits
                        </h5>
                        <div className="space-y-2">
                          {recommendation.benefits.map((benefit, index) => (
                            <div key={index} className="flex items-start space-x-3 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-700">
                              <span className="text-green-500 mt-1">✓</span>
                              <span className="text-gray-700 dark:text-gray-300">{benefit}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex flex-col sm:flex-row gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                        <button className="flex-1 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200">
                          🚀 Connect Integration
                        </button>
                        <button className="flex-1 px-6 py-3 bg-gray-200 hover:bg-gray-300 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-700 dark:text-gray-200 rounded-lg font-medium transition-colors duration-200">
                          📋 Add to Roadmap
                        </button>
                        <button 
                          onClick={() => setSelectedRecommendation(null)}
                          className="px-6 py-3 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-600 dark:text-gray-300 rounded-lg font-medium transition-colors duration-200"
                        >
                          Close
                        </button>
                      </div>
                    </div>
                  );
                })()}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Integrations; 