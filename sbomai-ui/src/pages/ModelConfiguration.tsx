import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';

interface Provider {
  id: string;
  name: string;
  logo: string;
  description: string;
  models: string[];
  isConnected: boolean;
  lastTested?: string;
  activeModels: string[];
}

interface ProviderConfig {
  apiKey: string;
  modelName: string;
  endpointUrl?: string;
  authHeaders?: string;
  temperature: number;
  topP: number;
  maxTokens: number;
  customParams?: string;
}

const ModelConfiguration: React.FC = () => {
  const [selectedProvider, setSelectedProvider] = useState<string | null>(null);
  const [showConfigModal, setShowConfigModal] = useState(false);
  const [showTestModal, setShowTestModal] = useState(false);
  const [testQuery, setTestQuery] = useState('');
  const [testResult, setTestResult] = useState<string>('');
  const [isTesting, setIsTesting] = useState(false);

  const [advancedSettings, setAdvancedSettings] = useState<Record<string, boolean>>({});
  const [showAddProviderModal, setShowAddProviderModal] = useState(false);
  const [customProviders, setCustomProviders] = useState<Provider[]>([]);

  // Available providers
  const providers: Provider[] = [
    {
      id: 'openai',
      name: 'OpenAI',
      logo: '🤖',
      description: 'Advanced natural language reasoning and analysis.',
      models: ['GPT-4', 'GPT-3.5-turbo', 'GPT-4-turbo'],
      isConnected: false,
      activeModels: []
    },
    {
      id: 'anthropic',
      name: 'Anthropic Claude',
      logo: '🧠',
      description: 'Safety-focused, detailed explanations.',
      models: ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku'],
      isConnected: false,
      activeModels: []
    },
    {
      id: 'google',
      name: 'Google Gemini',
      logo: '🔍',
      description: 'Fast, efficient analysis.',
      models: ['gemini-pro', 'gemini-pro-vision'],
      isConnected: false,
      activeModels: []
    },
    {
      id: 'custom',
      name: 'Custom API / Local Models',
      logo: '⚙️',
      description: 'For private/self-hosted AI or custom endpoints.',
      models: ['Custom Model'],
      isConnected: false,
      activeModels: []
    }
  ];

  // Model routing configuration
  const [modelRouting, setModelRouting] = useState({
    vulnerabilityAnalysis: 'openai',
    policyViolation: 'anthropic',
    threatIntelligence: 'google',
    codeReview: 'openai',
    dependencyAnalysis: 'anthropic'
  });

  const handleConnectProvider = (providerId: string) => {
    setSelectedProvider(providerId);
    setShowConfigModal(true);
  };

  const handleSaveConfig = (_providerId: string, _config: ProviderConfig) => {
    // Update provider status - for demo purposes, we'll just close the modal
    // In a real implementation, this would update the provider state
    setShowConfigModal(false);
    setSelectedProvider(null);
  };

  const handleTestConnection = async () => {
    setIsTesting(true);
    setTestResult('');
    
    // Simulate API test
    setTimeout(() => {
      const success = Math.random() > 0.3; // 70% success rate for demo
      setTestResult(success 
        ? '✅ Connection successful! API key is valid and model is responding correctly.'
        : '❌ Connection failed. Please check your API key and endpoint configuration.'
      );
      setIsTesting(false);
    }, 2000);
  };

  const handleTestQuery = async () => {
    setIsTesting(true);
    setTestResult('');
    
    // Simulate query test
    setTimeout(() => {
      setTestResult(`✅ Test query successful!
      
Sample Response:
"Based on the SBOM analysis, I've identified 3 critical vulnerabilities in the dependencies. The most concerning is CVE-2021-44228 in log4j version 2.14.1. I recommend upgrading to version 2.17.1 immediately to address this remote code execution vulnerability."
      
Response Time: 1.2s
Tokens Used: 156`);
      setIsTesting(false);
    }, 1500);
  };

  const getCurrentProvider = () => {
    const allProviders = [...providers, ...customProviders];
    return allProviders.find(p => p.id === selectedProvider);
  };

  const handleAddProvider = (newProvider: { name: string; logo: string; description: string; models: string[] }) => {
    const providerWithId: Provider = {
      ...newProvider,
      id: `custom-${Date.now()}`,
      isConnected: false,
      activeModels: []
    };
    setCustomProviders(prev => [...prev, providerWithId]);
    setShowAddProviderModal(false);
  };

  const getAllProviders = () => [...providers, ...customProviders];

  return (
    <div className="w-full h-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
                    <div className="px-3 sm:px-4 lg:px-6 py-6">
        {/* Page Header */}
        <PageHeader
          title="Model Configuration"
          description="Configure AI/ML providers for SBOM analysis and security insights"
          icon={
            <svg className="w-6 h-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          }
        />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Section 1: Available AI/ML Providers */}
          <div className="lg:col-span-2">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
                    🤖 Available AI/ML Providers
                    <span className="ml-3 text-sm bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 px-3 py-1 rounded-full">
                      {getAllProviders().length} Providers
                    </span>
                  </h2>
                </div>
                <button
                  onClick={() => setShowAddProviderModal(true)}
                  className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  <span className="text-lg">➕</span>
                  <span>Add Provider</span>
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {getAllProviders().map((provider) => (
                  <div 
                    key={provider.id}
                    className={`p-6 rounded-xl border-2 transition-all duration-300 hover:shadow-lg ${
                      provider.isConnected 
                        ? 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/10' 
                        : 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50'
                    }`}
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <div className="text-3xl">{provider.logo}</div>
                        <div>
                          <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                            {provider.name}
                          </h3>
                          <p className="text-sm text-gray-600 dark:text-gray-300">
                            {provider.description}
                          </p>
                        </div>
                      </div>
                      {provider.isConnected && (
                        <div className="flex items-center space-x-1">
                          <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                          <span className="text-xs text-green-600 dark:text-green-400 font-medium">Connected</span>
                        </div>
                      )}
                    </div>

                    <div className="mb-4">
                      <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Available Models:</h4>
                      <div className="flex flex-wrap gap-1">
                        {provider.models.map((model) => (
                          <span 
                            key={model}
                            className={`text-xs px-2 py-1 rounded-full ${
                              provider.activeModels.includes(model)
                                ? 'bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-300'
                                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                            }`}
                          >
                            {model}
                          </span>
                        ))}
                      </div>
                    </div>

                    {provider.lastTested && (
                      <div className="mb-4 text-xs text-gray-500 dark:text-gray-400">
                        Last tested: {provider.lastTested}
                      </div>
                    )}

                                         <div className="flex space-x-2">
                       <button
                         onClick={() => handleConnectProvider(provider.id)}
                         className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
                           provider.isConnected
                             ? 'bg-blue-600 hover:bg-blue-700 text-white'
                             : 'bg-green-600 hover:bg-green-700 text-white'
                         }`}
                       >
                         {provider.isConnected ? '🔧 Configure' : '🔗 Connect'}
                       </button>
                       {provider.id.startsWith('custom-') && (
                         <button
                           onClick={() => {
                             setCustomProviders(prev => prev.filter(p => p.id !== provider.id));
                           }}
                           className="px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors duration-200"
                           title="Remove Provider"
                         >
                           🗑️
                         </button>
                       )}
                     </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Section 3: Model Routing & Behavior */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6 mt-8">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                🎯 Model Routing & Behavior
                <span className="ml-2 text-xs bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 px-2 py-1 rounded-full">
                  Advanced
                </span>
              </h2>

              <div className="space-y-4">
                <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
                  Configure which models handle specific SBOM analysis tasks for optimal performance and accuracy.
                </p>

                {Object.entries(modelRouting).map(([task, providerId]) => (
                  <div key={task} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white capitalize">
                        {task.replace(/([A-Z])/g, ' $1').trim()}
                      </h4>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        AI analysis for {task.toLowerCase()}
                      </p>
                    </div>
                                         <select
                       value={providerId}
                       onChange={(e) => setModelRouting(prev => ({ ...prev, [task]: e.target.value }))}
                       className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
                     >
                       {getAllProviders().map(provider => (
                         <option key={provider.id} value={provider.id}>
                           {provider.name}
                         </option>
                       ))}
                     </select>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Section 4 & 5: Save & Test + Summary & Status */}
          <div className="space-y-6">
            {/* Save & Test Configuration */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                💾 Save & Test Configuration
              </h2>

              <div className="space-y-4">
                <button
                  onClick={() => setShowTestModal(true)}
                  className="w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200 flex items-center justify-center space-x-2"
                >
                  <span>🧪</span>
                  <span>Test All Connections</span>
                </button>

                <button className="w-full px-4 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors duration-200 flex items-center justify-center space-x-2">
                  <span>💾</span>
                  <span>Save Configuration</span>
                </button>

                <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
                  <div className="flex items-start space-x-2">
                    <span className="text-yellow-600 dark:text-yellow-400">⚠️</span>
                    <div className="text-sm text-yellow-800 dark:text-yellow-200">
                      <p className="font-medium mb-1">Security Note</p>
                      <p>API keys are encrypted and stored securely. Never share your keys in plain text.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Summary & Status */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                📊 Summary & Status
              </h2>

              <div className="space-y-4">
                                 <div className="flex items-center justify-between">
                   <span className="text-sm text-gray-600 dark:text-gray-300">Connected Providers</span>
                   <span className="text-lg font-bold text-green-600 dark:text-green-400">
                     {getAllProviders().filter(p => p.isConnected).length}/{getAllProviders().length}
                   </span>
                 </div>

                                 <div className="flex items-center justify-between">
                   <span className="text-sm text-gray-600 dark:text-gray-300">Active Models</span>
                   <span className="text-lg font-bold text-blue-600 dark:text-blue-400">
                     {getAllProviders().reduce((acc, p) => acc + p.activeModels.length, 0)}
                   </span>
                 </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Last Updated</span>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    {new Date().toLocaleDateString()}
                  </span>
                </div>

                                 <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                   <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Connected Providers:</h4>
                   <div className="space-y-2">
                     {getAllProviders().filter(p => p.isConnected).map(provider => (
                       <div key={provider.id} className="flex items-center justify-between text-sm">
                         <span className="text-gray-600 dark:text-gray-300">{provider.name}</span>
                         <div className="flex items-center space-x-1">
                           <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                           <span className="text-green-600 dark:text-green-400">Active</span>
                         </div>
                       </div>
                     ))}
                     {getAllProviders().filter(p => p.isConnected).length === 0 && (
                       <p className="text-sm text-gray-500 dark:text-gray-400 italic">No providers connected</p>
                     )}
                   </div>
                 </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Configuration Modal */}
      {showConfigModal && selectedProvider && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <span className="text-3xl">{getCurrentProvider()?.logo}</span>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                      Configure {getCurrentProvider()?.name}
                    </h2>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Set up connection and model parameters
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setShowConfigModal(false)}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <form onSubmit={(e) => {
                e.preventDefault();
                const formData = new FormData(e.currentTarget);
                const config: ProviderConfig = {
                  apiKey: formData.get('apiKey') as string,
                  modelName: formData.get('modelName') as string,
                  endpointUrl: formData.get('endpointUrl') as string,
                  authHeaders: formData.get('authHeaders') as string,
                  temperature: parseFloat(formData.get('temperature') as string),
                  topP: parseFloat(formData.get('topP') as string),
                  maxTokens: parseInt(formData.get('maxTokens') as string),
                  customParams: formData.get('customParams') as string
                };
                handleSaveConfig(selectedProvider, config);
              }}>
                <div className="space-y-6">
                  {/* Basic Configuration */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Basic Configuration</h3>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          API Key / Access Token *
                        </label>
                        <input
                          type="password"
                          name="apiKey"
                          required
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                          placeholder="sk-..."
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Model Name / Version *
                        </label>
                        <select
                          name="modelName"
                          required
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        >
                          {getCurrentProvider()?.models.map(model => (
                            <option key={model} value={model}>{model}</option>
                          ))}
                        </select>
                      </div>

                      {selectedProvider === 'custom' && (
                        <div>
                          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Endpoint URL
                          </label>
                          <input
                            type="url"
                            name="endpointUrl"
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            placeholder="https://api.example.com/v1/chat/completions"
                          />
                        </div>
                      )}

                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Authentication Headers (Optional)
                        </label>
                        <textarea
                          name="authHeaders"
                          rows={2}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                          placeholder='{"Authorization": "Bearer sk-...", "X-Custom-Header": "value"}'
                        />
                      </div>
                    </div>
                  </div>

                  {/* Advanced Settings */}
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Advanced Settings</h3>
                      <button
                        type="button"
                        onClick={() => setAdvancedSettings(prev => ({ ...prev, [selectedProvider]: !prev[selectedProvider] }))}
                        className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 text-sm font-medium"
                      >
                        {advancedSettings[selectedProvider] ? 'Hide' : 'Show'} Advanced
                      </button>
                    </div>

                    {advancedSettings[selectedProvider] && (
                      <div className="space-y-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                              Temperature
                            </label>
                            <input
                              type="number"
                              name="temperature"
                              min="0"
                              max="2"
                              step="0.1"
                              defaultValue="0.7"
                              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            />
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Controls creativity (0-2)</p>
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                              Top-p
                            </label>
                            <input
                              type="number"
                              name="topP"
                              min="0"
                              max="1"
                              step="0.1"
                              defaultValue="0.9"
                              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            />
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Nucleus sampling (0-1)</p>
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                              Max Tokens
                            </label>
                            <input
                              type="number"
                              name="maxTokens"
                              min="1"
                              max="4000"
                              defaultValue="1000"
                              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            />
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Response length limit</p>
                          </div>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Custom Parameters (JSON)
                          </label>
                          <textarea
                            name="customParams"
                            rows={3}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            placeholder='{"presence_penalty": 0.1, "frequency_penalty": 0.1}'
                          />
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Action Buttons */}
                  <div className="flex space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <button
                      type="button"
                      onClick={handleTestConnection}
                      disabled={isTesting}
                      className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg font-medium transition-colors duration-200 flex items-center justify-center space-x-2"
                    >
                      {isTesting ? (
                        <>
                          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                          <span>Testing...</span>
                        </>
                      ) : (
                        <>
                          <span>🧪</span>
                          <span>Test Connection</span>
                        </>
                      )}
                    </button>
                    <button
                      type="submit"
                      className="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors duration-200"
                    >
                      💾 Save Configuration
                    </button>
                  </div>

                  {testResult && (
                    <div className={`p-4 rounded-lg border ${
                      testResult.includes('✅') 
                        ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800' 
                        : 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
                    }`}>
                      <p className="text-sm whitespace-pre-line">{testResult}</p>
                    </div>
                  )}
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Test Query Modal */}
      {showTestModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">🧪 Test AI Query</h2>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    Test your configured models with a sample SBOM analysis query
                  </p>
                </div>
                <button
                  onClick={() => setShowTestModal(false)}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Test Query
                  </label>
                  <textarea
                    value={testQuery}
                    onChange={(e) => setTestQuery(e.target.value)}
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="Analyze this SBOM for security vulnerabilities and provide remediation recommendations..."
                    defaultValue="Analyze this SBOM for security vulnerabilities and provide remediation recommendations for any critical or high-severity issues found."
                  />
                </div>

                <button
                  onClick={handleTestQuery}
                  disabled={isTesting || !testQuery.trim()}
                  className="w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg font-medium transition-colors duration-200 flex items-center justify-center space-x-2"
                >
                  {isTesting ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Processing Query...</span>
                    </>
                  ) : (
                    <>
                      <span>🚀</span>
                      <span>Send Test Query</span>
                    </>
                  )}
                </button>

                {testResult && (
                  <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                    <h4 className="font-medium text-blue-800 dark:text-blue-300 mb-2">Test Result:</h4>
                    <p className="text-sm text-blue-700 dark:text-blue-200 whitespace-pre-line">{testResult}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
                 </div>
       )}

       {/* Add Provider Modal */}
       {showAddProviderModal && (
         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
           <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
             <div className="p-6">
               <div className="flex items-center justify-between mb-6">
                 <div>
                   <h2 className="text-2xl font-bold text-gray-900 dark:text-white">➕ Add New Provider</h2>
                   <p className="text-sm text-gray-600 dark:text-gray-300">
                     Add a custom AI/ML provider to your configuration
                   </p>
                 </div>
                 <button
                   onClick={() => setShowAddProviderModal(false)}
                   className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
                 >
                   <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                   </svg>
                 </button>
               </div>

               <form onSubmit={(e) => {
                 e.preventDefault();
                 const formData = new FormData(e.currentTarget);
                 const newProvider = {
                   name: formData.get('name') as string,
                   logo: formData.get('logo') as string,
                   description: formData.get('description') as string,
                   models: (formData.get('models') as string).split(',').map(m => m.trim()).filter(m => m)
                 };
                 handleAddProvider(newProvider);
               }}>
                 <div className="space-y-6">
                   <div>
                     <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                       Provider Name *
                     </label>
                     <input
                       type="text"
                       name="name"
                       required
                       className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                       placeholder="e.g., Azure OpenAI, AWS Bedrock"
                     />
                   </div>

                   <div>
                     <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                       Provider Logo (Emoji) *
                     </label>
                     <input
                       type="text"
                       name="logo"
                       required
                       className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                       placeholder="🤖"
                       defaultValue="🤖"
                     />
                   </div>

                   <div>
                     <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                       Description *
                     </label>
                     <textarea
                       name="description"
                       required
                       rows={3}
                       className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                       placeholder="Brief description of the provider's capabilities and strengths"
                     />
                   </div>

                   <div>
                     <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                       Available Models *
                     </label>
                     <textarea
                       name="models"
                       required
                       rows={3}
                       className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                       placeholder="model1, model2, model3 (comma-separated)"
                     />
                     <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                       Enter model names separated by commas
                     </p>
                   </div>

                   <div className="flex space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                     <button
                       type="button"
                       onClick={() => setShowAddProviderModal(false)}
                       className="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors duration-200"
                     >
                       Cancel
                     </button>
                     <button
                       type="submit"
                       className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200"
                     >
                       Add Provider
                     </button>
                   </div>
                 </div>
               </form>
             </div>
           </div>
         </div>
       )}
     </div>
   );
 };

export default ModelConfiguration; 