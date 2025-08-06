import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, Cell, PieChart, Pie } from 'recharts';

interface ActivityItem {
  id: string;
  timestamp: string;
  type: 'scan' | 'alert' | 'violation' | 'pr' | 'update';
  title: string;
  description: string;
  severity?: 'critical' | 'high' | 'medium' | 'low';
  project?: string;
  isNew?: boolean;
}

interface Integration {
  id: string;
  name: string;
  icon: string;
  description: string;
  status: 'connected' | 'available' | 'recommended';
  action: string;
}

const Home: React.FC = () => {

  const [showActivityFeed, setShowActivityFeed] = useState(true);
  const [currentUser] = useState('Kiran');

  // Stats data
  const statsData = {
    totalSboms: 8132,
    openVulnerabilities: 294,
    policiesViolated: 17,
    aiSuggestions: 2374,
    trends: {
      sboms: '+12%',
      vulnerabilities: '-8%',
      policies: '+3%',
      suggestions: '+25%'
    }
  };

  // Chart data
  const vulnerabilityTrendData = [
    { date: 'Jan 1', critical: 45, high: 78, medium: 156, low: 234 },
    { date: 'Jan 8', critical: 52, high: 82, medium: 142, low: 198 },
    { date: 'Jan 15', critical: 38, high: 65, medium: 128, low: 187 },
    { date: 'Jan 22', critical: 42, high: 71, medium: 135, low: 203 },
    { date: 'Jan 29', critical: 35, high: 58, medium: 121, low: 176 },
    { date: 'Feb 5', critical: 29, high: 49, medium: 108, low: 165 }
  ];

  const sbomCoverageData = [
    { name: 'Covered', value: 78, color: '#10B981' },
    { name: 'Uncovered', value: 22, color: '#EF4444' }
  ];

  const vulnerablePackagesData = [
    { name: 'log4j-core', vulnerabilities: 12, severity: 'critical' },
    { name: 'spring-core', vulnerabilities: 8, severity: 'high' },
    { name: 'jackson-databind', vulnerabilities: 7, severity: 'high' },
    { name: 'netty', vulnerabilities: 6, severity: 'medium' },
    { name: 'guava', vulnerabilities: 5, severity: 'medium' },
    { name: 'commons-io', vulnerabilities: 4, severity: 'low' },
    { name: 'slf4j-api', vulnerabilities: 3, severity: 'low' },
    { name: 'junit', vulnerabilities: 2, severity: 'low' }
  ];

  // Activity feed data
  const activityItems: ActivityItem[] = [
    {
      id: '1',
      timestamp: '2 min ago',
      type: 'scan',
      title: 'New Scan started',
      description: 'project-x.sbom.json',
      project: 'project-x',
      isNew: true
    },
    {
      id: '2',
      timestamp: '5 min ago',
      type: 'alert',
      title: 'AI Alert: CVE-2023-1234 likely to escalate',
      description: 'Critical vulnerability detected in production dependencies',
      severity: 'critical',
      isNew: true
    },
    {
      id: '3',
      timestamp: '12 min ago',
      type: 'violation',
      title: 'Policy Violation Detected',
      description: 'api-gateway - Outdated dependency policy breached',
      project: 'api-gateway',
      severity: 'high'
    },
    {
      id: '4',
      timestamp: '1 hour ago',
      type: 'pr',
      title: 'GitHub PR merged',
      description: 'Added 2 new dependencies to user-service',
      project: 'user-service'
    },
    {
      id: '5',
      timestamp: '2 hours ago',
      type: 'update',
      title: 'Auto-update completed',
      description: 'Updated 15 packages in payment-service',
      project: 'payment-service'
    }
  ];

  // Integration data
  const integrations: Integration[] = [
    {
      id: 'github',
      name: 'GitHub',
      icon: '🔗',
      description: 'Connect repositories for automated scanning',
      status: 'connected',
      action: 'Manage'
    },
    {
      id: 'webhook',
      name: 'Webhook',
      icon: '🌐',
      description: 'Set up webhooks for real-time alerts',
      status: 'available',
      action: 'Connect'
    },
    {
      id: 'vscode',
      name: 'VSCode Plugin',
      icon: '💻',
      description: 'Install plugin for IDE integration',
      status: 'recommended',
      action: 'Install'
    },
    {
      id: 'openai',
      name: 'OpenAI Key',
      icon: '🧠',
      description: 'Configure AI analysis capabilities',
      status: 'available',
      action: 'Add Key'
    }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return '#EF4444';
      case 'high': return '#F97316';
      case 'medium': return '#EAB308';
      case 'low': return '#10B981';
      default: return '#6B7280';
    }
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'scan': return '📄';
      case 'alert': return '🚨';
      case 'violation': return '⚠️';
      case 'pr': return '🔀';
      case 'update': return '🔄';
      default: return '📋';
    }
  };

     return (
     <div className="w-full h-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
               <div className="px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
                     <h1 className="text-5xl lg:text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6 leading-tight">
             SBOM AI Sniffer — Intelligent SBOM Visibility & Security
           </h1>
                            <p className="text-2xl text-gray-600 dark:text-gray-300 mb-8">
                    Secure your supply chain — powered by AI.
                  </p>
                  <p className="text-lg text-gray-500 dark:text-gray-400 mb-8">
                    Real-time SBOM analysis, vulnerability detection, and AI-generated insights to keep your projects safe.
                  </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 mb-8">
            <button className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-xl font-semibold text-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105">
              📤 Upload SBOM
            </button>
            <button className="px-8 py-4 bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 text-gray-700 dark:text-gray-300 rounded-xl font-semibold text-lg transition-all duration-200">
              🔍 Run Live Scan
            </button>
          </div>
          
          <button className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium text-lg transition-colors">
            🎬 See It In Action →
          </button>
        </div>

        {/* Welcome Message */}
        <div className="mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center space-x-3">
              <span className="text-2xl">👋</span>
              <div>
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  Welcome back, {currentUser}
                </h2>
                <p className="text-gray-600 dark:text-gray-300">
                  Your SBOM security dashboard is ready. Here's what's happening with your projects.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Overview Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl">📄</div>
              <div className="text-sm text-green-600 dark:text-green-400 font-medium flex items-center">
                📈 {statsData.trends.sboms}
              </div>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              {statsData.totalSboms.toLocaleString()}
            </h3>
            <p className="text-gray-600 dark:text-gray-300">Total SBOMs Analyzed</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl">🛑</div>
              <div className="text-sm text-red-600 dark:text-red-400 font-medium flex items-center">
                📉 {statsData.trends.vulnerabilities}
              </div>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              {statsData.openVulnerabilities}
            </h3>
            <p className="text-gray-600 dark:text-gray-300">Open Vulnerabilities</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl">⚠️</div>
              <div className="text-sm text-orange-600 dark:text-orange-400 font-medium flex items-center">
                📈 {statsData.trends.policies}
              </div>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              {statsData.policiesViolated}
            </h3>
            <p className="text-gray-600 dark:text-gray-300">Policies Violated</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl">🤖</div>
              <div className="text-sm text-purple-600 dark:text-purple-400 font-medium flex items-center">
                📈 {statsData.trends.suggestions}
              </div>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              {statsData.aiSuggestions.toLocaleString()}
            </h3>
            <p className="text-gray-600 dark:text-gray-300">AI Suggestions Generated</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          {/* Charts Section */}
          <div className="lg:col-span-2 space-y-8">
            {/* Vulnerability Trends Chart */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6">📈 Vulnerability Trends Over Time</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={vulnerabilityTrendData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="date" stroke="#6B7280" />
                  <YAxis stroke="#6B7280" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1F2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px'
                    }}
                  />
                  <Legend />
                  <Line type="monotone" dataKey="critical" stroke="#EF4444" strokeWidth={3} />
                  <Line type="monotone" dataKey="high" stroke="#F97316" strokeWidth={3} />
                  <Line type="monotone" dataKey="medium" stroke="#EAB308" strokeWidth={3} />
                  <Line type="monotone" dataKey="low" stroke="#10B981" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Vulnerable Packages Chart */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6">📦 Top Vulnerable Packages</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={vulnerablePackagesData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" stroke="#6B7280" />
                  <YAxis stroke="#6B7280" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1F2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px'
                    }}
                  />
                  <Bar dataKey="vulnerabilities">
                    {vulnerablePackagesData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={getSeverityColor(entry.severity)} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="space-y-8">
            {/* SBOM Coverage Chart */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6">📊 SBOM Coverage by Repo</h3>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={sbomCoverageData}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {sbomCoverageData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1F2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px'
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="text-center mt-4">
                <div className="text-3xl font-bold text-gray-900 dark:text-white">78%</div>
                <div className="text-gray-600 dark:text-gray-300">Coverage Rate</div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6">⚡ Quick Actions</h3>
              <div className="space-y-3">
                <button className="w-full flex items-center space-x-3 p-3 bg-blue-50 dark:bg-blue-900/20 hover:bg-blue-100 dark:hover:bg-blue-900/30 rounded-lg transition-colors">
                  <span className="text-xl">📤</span>
                  <span className="text-gray-700 dark:text-gray-300">Upload SBOM</span>
                </button>
                <button className="w-full flex items-center space-x-3 p-3 bg-purple-50 dark:bg-purple-900/20 hover:bg-purple-100 dark:hover:bg-purple-900/30 rounded-lg transition-colors">
                  <span className="text-xl">🧠</span>
                  <span className="text-gray-700 dark:text-gray-300">View Live AI Feed</span>
                </button>
                <button className="w-full flex items-center space-x-3 p-3 bg-green-50 dark:bg-green-900/20 hover:bg-green-100 dark:hover:bg-green-900/30 rounded-lg transition-colors">
                  <span className="text-xl">🛠️</span>
                  <span className="text-gray-700 dark:text-gray-300">Add Model / API Key</span>
                </button>
                <button className="w-full flex items-center space-x-3 p-3 bg-orange-50 dark:bg-orange-900/20 hover:bg-orange-100 dark:hover:bg-orange-900/30 rounded-lg transition-colors">
                  <span className="text-xl">🌐</span>
                  <span className="text-gray-700 dark:text-gray-300">Open Web Scan</span>
                </button>
                <button className="w-full flex items-center space-x-3 p-3 bg-indigo-50 dark:bg-indigo-900/20 hover:bg-indigo-100 dark:hover:bg-indigo-900/30 rounded-lg transition-colors">
                  <span className="text-xl">🧩</span>
                  <span className="text-gray-700 dark:text-gray-300">Install Plugin</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* AI-Powered Highlights */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-2xl shadow-lg border border-blue-200 dark:border-blue-800 p-6 mb-8">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
            🧠 AI-Powered Highlights
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center space-x-2 mb-2">
                <span className="text-lg">🧠</span>
                <span className="font-semibold text-gray-900 dark:text-white">AI Insight</span>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-300">
                Your API gateway has high dependency drift — AI suggests lockfile audit.
              </p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center space-x-2 mb-2">
                <span className="text-lg">🔮</span>
                <span className="font-semibold text-gray-900 dark:text-white">Predicted Risk</span>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-300">
                Risk Score: <span className="font-bold text-orange-600">78/100</span> <span className="text-green-600">(↑ 12%)</span>
              </p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center space-x-2 mb-2">
                <span className="text-lg">✅</span>
                <span className="font-semibold text-gray-900 dark:text-white">Suggested Fix</span>
              </div>
                             <p className="text-sm text-gray-600 dark:text-gray-300">
                 Update log4j-core to &gt;=2.19.1
               </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Recent Activity Feed */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">🧾 Recent Activity Feed</h3>
                <button
                  onClick={() => setShowActivityFeed(!showActivityFeed)}
                  className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
                >
                  {showActivityFeed ? 'Hide' : 'Show'}
                </button>
              </div>
            </div>
            {showActivityFeed && (
              <div className="p-6">
                <div className="space-y-4">
                  {activityItems.map((item) => (
                    <div key={item.id} className={`flex items-start space-x-3 p-3 rounded-lg ${item.isNew ? 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800' : 'bg-gray-50 dark:bg-gray-700/50'}`}>
                      <div className="text-lg">{getActivityIcon(item.type)}</div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <h4 className="font-medium text-gray-900 dark:text-white text-sm">{item.title}</h4>
                          <span className="text-xs text-gray-500 dark:text-gray-400">{item.timestamp}</span>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-300">{item.description}</p>
                        {item.project && (
                          <span className="inline-block mt-1 text-xs bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300 px-2 py-1 rounded">
                            {item.project}
                          </span>
                        )}
                      </div>
                      {item.isNew && (
                        <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Integration Recommendations */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">🔌 Integration Recommendations</h3>
                               <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                   Connect SBOM AI Sniffer with your tools to automate security
                 </p>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {integrations.map((integration) => (
                  <div key={integration.id} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <span className="text-xl">{integration.icon}</span>
                      <div>
                        <h4 className="font-medium text-gray-900 dark:text-white">{integration.name}</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-300">{integration.description}</p>
                      </div>
                    </div>
                    <button className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                      integration.status === 'connected' 
                        ? 'bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-300'
                        : integration.status === 'recommended'
                        ? 'bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300'
                        : 'bg-gray-100 dark:bg-gray-600 text-gray-700 dark:text-gray-300'
                    }`}>
                      {integration.action}
                    </button>
                  </div>
                ))}
                <button className="w-full flex items-center justify-center space-x-2 p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg text-gray-600 dark:text-gray-400 hover:border-gray-400 dark:hover:border-gray-500 transition-colors">
                  <span>+</span>
                  <span>Add External Integration</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-6 mb-4 md:mb-0">
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white">About</a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white">Docs</a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white">Blog</a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white">GitHub</a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white">Contact</a>
            </div>
                         <div className="text-gray-500 dark:text-gray-400 text-sm">
               v1.0.3 © 2025 SBOM AI Sniffer
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home; 