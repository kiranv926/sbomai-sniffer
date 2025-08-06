import React, { useState } from 'react';
import Breadcrumb from '../components/Breadcrumb';

const BreadcrumbDemo: React.FC = () => {
  const [currentView, setCurrentView] = useState('main');
  const [showCustomExample, setShowCustomExample] = useState(false);

  // Different breadcrumb scenarios
  const breadcrumbScenarios = {
    main: [
      { name: 'Home', path: '/', icon: '🏠' },
      { name: 'Breadcrumb Demo', path: '/breadcrumb-demo', icon: '🧭', description: 'Navigation Examples' }
    ],
    vulnerabilities: [
      { name: 'Home', path: '/', icon: '🏠' },
      { name: 'Vulnerabilities', path: '/vulnerabilities', icon: '🛡️', description: 'Security Issues' },
      { name: 'Log4Shell', path: '/vulnerabilities/log4shell', icon: '🔥', description: 'Critical CVE-2021-44228' }
    ],
    aiAnalysis: [
      { name: 'Home', path: '/', icon: '🏠' },
      { name: 'AI Analysis', path: '/ai-analysis', icon: '🤖', description: 'AI-Powered Insights' },
      { name: 'Project Falcon', path: '/ai-analysis/project-falcon', icon: '📂', description: 'Repository Analysis' },
      { name: 'Recommendations', path: '/ai-analysis/project-falcon/recommendations', icon: '💡', description: 'AI Suggestions' }
    ],
    githubInsights: [
      { name: 'Home', path: '/', icon: '🏠' },
      { name: 'GitHub Insights', path: '/github-insights', icon: '📈', description: 'Repository Analysis' },
      { name: 'Pull Requests', path: '/github-insights/pull-requests', icon: '🔀', description: 'PR Analysis' },
      { name: 'Security Review', path: '/github-insights/pull-requests/security-review', icon: '🔍', description: 'Security Analysis' }
    ]
  };

  const getCurrentBreadcrumbs = () => {
    return breadcrumbScenarios[currentView as keyof typeof breadcrumbScenarios] || breadcrumbScenarios.main;
  };

  // Example custom breadcrumbs for documentation
  const customBreadcrumbs = [
    { name: 'Home', path: '/', icon: '🏠' },
    { name: 'Projects', path: '/projects', icon: '📁' },
    { name: 'Project Alpha', path: '/projects/alpha', icon: '🔷' },
    { name: 'Settings', path: '/projects/alpha/settings', icon: '⚙️' }
  ];

  return (
    <div className="w-full h-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-6">
      {/* Custom Breadcrumb */}
      <Breadcrumb items={getCurrentBreadcrumbs()} showSearch={true} />
      
      <div className="mt-8">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
              🧭 Breadcrumb Navigation Demo
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Experience the power of intelligent navigation with our professional breadcrumb component. 
              See how it adapts to different scenarios and provides seamless user experience.
            </p>
          </div>

          {/* Live Demo Section */}
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-xl p-6 mb-8 border border-blue-200 dark:border-blue-800">
            <h3 className="text-xl font-semibold text-blue-900 dark:text-blue-100 mb-4 flex items-center">
              🎮 Live Interactive Demo
            </h3>
            <p className="text-blue-800 dark:text-blue-200 mb-6">
              Click the scenario buttons below to see the breadcrumb navigation change dynamically:
            </p>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <button
                onClick={() => setCurrentView('main')}
                className={`px-4 py-3 rounded-lg font-medium transition-all duration-200 transform hover:scale-105 ${
                  currentView === 'main'
                    ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg'
                    : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600 border border-gray-200 dark:border-gray-600'
                }`}
              >
                🏠 Main
              </button>
              
              <button
                onClick={() => setCurrentView('vulnerabilities')}
                className={`px-4 py-3 rounded-lg font-medium transition-all duration-200 transform hover:scale-105 ${
                  currentView === 'vulnerabilities'
                    ? 'bg-gradient-to-r from-red-600 to-red-700 text-white shadow-lg'
                    : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600 border border-gray-200 dark:border-gray-600'
                }`}
              >
                🛡️ Vulnerabilities
              </button>
              
              <button
                onClick={() => setCurrentView('aiAnalysis')}
                className={`px-4 py-3 rounded-lg font-medium transition-all duration-200 transform hover:scale-105 ${
                  currentView === 'aiAnalysis'
                    ? 'bg-gradient-to-r from-purple-600 to-purple-700 text-white shadow-lg'
                    : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600 border border-gray-200 dark:border-gray-600'
                }`}
              >
                🤖 AI Analysis
              </button>
              
              <button
                onClick={() => setCurrentView('githubInsights')}
                className={`px-4 py-3 rounded-lg font-medium transition-all duration-200 transform hover:scale-105 ${
                  currentView === 'githubInsights'
                    ? 'bg-gradient-to-r from-green-600 to-green-700 text-white shadow-lg'
                    : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600 border border-gray-200 dark:border-gray-600'
                }`}
              >
                📈 GitHub Insights
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* Features Section */}
            <div className="bg-gray-50 dark:bg-gray-700 rounded-xl p-6 border border-gray-200 dark:border-gray-600">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                ✨ Key Features
              </h3>
              <ul className="space-y-3 text-sm text-gray-600 dark:text-gray-300">
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span><strong>Smart Navigation:</strong> Clickable breadcrumb segments with intelligent routing</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span><strong>Visual Indicators:</strong> Icons and colors for enhanced user experience</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span><strong>Quick Actions:</strong> Back button and search functionality</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span><strong>Context Awareness:</strong> Dynamic descriptions and tooltips</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span><strong>Responsive Design:</strong> Adapts seamlessly to all screen sizes</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span><strong>Accessibility:</strong> ARIA labels and keyboard navigation support</span>
                </li>
              </ul>
            </div>

            {/* Configuration Section */}
            <div className="bg-gray-50 dark:bg-gray-700 rounded-xl p-6 border border-gray-200 dark:border-gray-600">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                ⚙️ Configuration Options
              </h3>
              <ul className="space-y-3 text-sm text-gray-600 dark:text-gray-300">
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2">🔧</span>
                  <span><strong>showBackButton:</strong> Enable/disable back navigation</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2">🔧</span>
                  <span><strong>showSearch:</strong> Add breadcrumb filtering capability</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2">🔧</span>
                  <span><strong>items:</strong> Custom breadcrumb array with icons</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2">🔧</span>
                  <span><strong>Auto-detection:</strong> Default based on current route</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2">🔧</span>
                  <span><strong>Dynamic Updates:</strong> Real-time breadcrumb changes</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2">🔧</span>
                  <span><strong>Custom Styling:</strong> Theme-aware and customizable</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Custom Example Toggle */}
          <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-xl p-6 mb-8 border border-yellow-200 dark:border-yellow-800">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-semibold text-yellow-900 dark:text-yellow-100 mb-2">
                  🎯 Custom Breadcrumb Example
                </h3>
                <p className="text-yellow-800 dark:text-yellow-200">
                  See how to implement custom breadcrumbs with specific navigation paths
                </p>
              </div>
              <button
                onClick={() => setShowCustomExample(!showCustomExample)}
                className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                  showCustomExample
                    ? 'bg-yellow-600 text-white'
                    : 'bg-white dark:bg-gray-700 text-yellow-700 dark:text-yellow-300 hover:bg-yellow-50 dark:hover:bg-yellow-900/30 border border-yellow-300 dark:border-yellow-700'
                }`}
              >
                {showCustomExample ? 'Hide' : 'Show'} Example
              </button>
            </div>
            
            {showCustomExample && (
              <div className="mt-6 p-4 bg-white dark:bg-gray-800 rounded-lg border border-yellow-200 dark:border-yellow-700">
                <Breadcrumb items={customBreadcrumbs} showSearch={true} />
                <div className="mt-4 text-sm text-gray-600 dark:text-gray-400">
                  <p><strong>Path:</strong> Home → Projects → Project Alpha → Settings</p>
                  <p><strong>Features:</strong> Custom icons, search enabled, clickable navigation</p>
                </div>
              </div>
            )}
          </div>

          {/* Code Examples Section */}
          <div className="bg-gray-50 dark:bg-gray-700 rounded-xl p-6 border border-gray-200 dark:border-gray-600">
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-6 flex items-center">
              💻 Implementation Examples
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Default Usage (Auto-detection):</h4>
                <div className="bg-gray-900 dark:bg-black rounded-lg p-4 text-green-400 text-sm font-mono">
                  <div>&lt;Breadcrumb /&gt;</div>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                  Automatically detects current route and generates breadcrumbs
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Custom Breadcrumbs:</h4>
                <div className="bg-gray-900 dark:bg-black rounded-lg p-4 text-green-400 text-sm font-mono">
                  <div>&lt;Breadcrumb</div>
                  <div>&nbsp;&nbsp;items=&#123;customBreadcrumbs&#125;</div>
                  <div>&nbsp;&nbsp;showSearch=&#123;true&#125;</div>
                  <div>/&gt;</div>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                  Pass custom breadcrumb array with icons and descriptions
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Without Back Button:</h4>
                <div className="bg-gray-900 dark:bg-black rounded-lg p-4 text-green-400 text-sm font-mono">
                  <div>&lt;Breadcrumb</div>
                  <div>&nbsp;&nbsp;showBackButton=&#123;false&#125;</div>
                  <div>/&gt;</div>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                  Disable the back button for specific use cases
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">With Search Disabled:</h4>
                <div className="bg-gray-900 dark:bg-black rounded-lg p-4 text-green-400 text-sm font-mono">
                  <div>&lt;Breadcrumb</div>
                  <div>&nbsp;&nbsp;showSearch=&#123;false&#125;</div>
                  <div>/&gt;</div>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                  Remove search functionality for simpler navigation
                </p>
              </div>
            </div>
          </div>

          {/* Best Practices Section */}
          <div className="mt-8 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-xl p-6 border border-green-200 dark:border-green-800">
            <h3 className="text-xl font-semibold text-green-900 dark:text-green-100 mb-4 flex items-center">
              📚 Best Practices
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-green-800 dark:text-green-200 mb-2">✅ Do's</h4>
                <ul className="text-sm text-green-700 dark:text-green-300 space-y-1">
                  <li>• Keep breadcrumb paths concise and meaningful</li>
                  <li>• Use descriptive icons for visual recognition</li>
                  <li>• Ensure all segments are clickable</li>
                  <li>• Maintain consistent styling across pages</li>
                  <li>• Test navigation on mobile devices</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-red-800 dark:text-red-200 mb-2">❌ Don'ts</h4>
                <ul className="text-sm text-red-700 dark:text-red-300 space-y-1">
                  <li>• Don't create overly deep navigation paths</li>
                  <li>• Avoid generic or unclear breadcrumb names</li>
                  <li>• Don't forget accessibility considerations</li>
                  <li>• Avoid inconsistent icon usage</li>
                  <li>• Don't ignore mobile user experience</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BreadcrumbDemo; 