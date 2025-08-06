import React, { useState, useEffect } from 'react';
import PageHeader from '../components/PageHeader';

interface LiveEvent {
  id: string;
  timestamp: string;
  type: 'upload' | 'vulnerability' | 'policy' | 'ai-fix' | 'threat';
  title: string;
  project?: string;
  user?: string;
  component?: string;
  cve?: string;
  policy?: string;
  details: string;
  aiInsight?: string;
  action?: string;
  severity?: 'Critical' | 'High' | 'Medium' | 'Low';
  status?: 'pending' | 'processing' | 'completed' | 'failed';
}

interface FeedStats {
  sbomsUploaded: number;
  vulnerabilitiesDetected: number;
  policyViolations: number;
  aiFixesSuggested: number;
  autoFixesApplied: number;
}

const LiveFeed: React.FC = () => {
  const [events, setEvents] = useState<LiveEvent[]>([]);
  const [selectedEvent, setSelectedEvent] = useState<LiveEvent | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [stats, _setStats] = useState<FeedStats>({
    sbomsUploaded: 145,
    vulnerabilitiesDetected: 421,
    policyViolations: 36,
    aiFixesSuggested: 127,
    autoFixesApplied: 42
  });

  // Mock data for live events
  const mockEvents: LiveEvent[] = [
    {
      id: '1',
      timestamp: '12:03 PM',
      type: 'upload',
      title: '📦 SBOM Uploaded',
      project: 'ecommerce-api-service',
      user: 'alice.wang@company.com',
      details: 'Detected: 126 Components, 3 Critical CVEs',
      aiInsight: '4 transitive dependencies may cause exposure. Suggest isolating guava version.',
      action: '🟢 Auto Scan Started',
      status: 'completed'
    },
    {
      id: '2',
      timestamp: '12:05 PM',
      type: 'vulnerability',
      title: '🔥 Vulnerability Detected',
      component: 'log4j:2.14.1',
      cve: 'CVE-2021-44228',
      project: 'ecommerce-api-service',
      details: 'Critical severity vulnerability detected',
      aiInsight: 'Apply patch 2.17.1 immediately. This is a known RCE.',
      action: '🚀 1-Click Fix Available',
      severity: 'Critical',
      status: 'processing'
    },
    {
      id: '3',
      timestamp: '12:06 PM',
      type: 'policy',
      title: '🧠 AI Policy Violation',
      policy: 'No criticals in production',
      project: 'payments-gateway',
      component: 'jackson-core',
      details: 'Policy breach detected in production environment',
      aiInsight: 'Marked as policy breach due to transitive risk. Consider sandboxing.',
      action: '🔧 Fix Flow Suggested',
      severity: 'Critical',
      status: 'pending'
    },
    {
      id: '4',
      timestamp: '12:08 PM',
      type: 'ai-fix',
      title: '🤖 AI Fix Applied',
      project: 'user-auth-service',
      component: 'spring-security',
      details: 'Automatically upgraded to secure version',
      aiInsight: 'Security patch applied successfully. No breaking changes detected.',
      action: '✅ Fix Applied Successfully',
      status: 'completed'
    },
    {
      id: '5',
      timestamp: '12:10 PM',
      type: 'threat',
      title: '🌐 NVD Threat Intel',
      component: 'netty',
      cve: 'CVE-2025-19834',
      details: 'New vulnerability discovered in netty library',
      aiInsight: 'Monitor for updates. Current version not affected.',
      action: '📊 Monitoring Active',
      severity: 'Medium',
      status: 'pending'
    },
    {
      id: '6',
      timestamp: '12:12 PM',
      type: 'upload',
      title: '📦 SBOM Uploaded',
      project: 'mobile-app-backend',
      user: 'bob.smith@company.com',
      details: 'Detected: 89 Components, 1 High CVE',
      aiInsight: 'Low risk profile. Consider dependency pruning for optimization.',
      action: '🟢 Auto Scan Started',
      status: 'completed'
    },
    {
      id: '7',
      timestamp: '12:15 PM',
      type: 'vulnerability',
      title: '🔥 Vulnerability Detected',
      component: 'axios:1.4.0',
      cve: 'CVE-2023-1234',
      project: 'mobile-app-backend',
      details: 'SSRF vulnerability in HTTP client',
      aiInsight: 'Upgrade to axios 1.6.0. No API changes required.',
      action: '🚀 1-Click Fix Available',
      severity: 'High',
      status: 'processing'
    },
    {
      id: '8',
      timestamp: '12:18 PM',
      type: 'policy',
      title: '🧠 AI Policy Violation',
      policy: 'No outdated dependencies',
      project: 'analytics-service',
      component: 'moment.js',
      details: 'Outdated library detected in production',
      aiInsight: 'Consider migration to dayjs for better performance and security.',
      action: '🔧 Migration Plan Generated',
      severity: 'Medium',
      status: 'pending'
    }
  ];

  // Simulate real-time updates
  useEffect(() => {
    setEvents(mockEvents);
    
    // Simulate new events every 10 seconds
    const interval = setInterval(() => {
      const newEvent: LiveEvent = {
        id: Date.now().toString(),
        timestamp: new Date().toLocaleTimeString('en-US', { 
          hour: 'numeric', 
          minute: '2-digit',
          hour12: true 
        }),
        type: 'upload',
        title: '📦 SBOM Uploaded',
        project: 'test-service-' + Math.floor(Math.random() * 1000),
        user: 'user@company.com',
        details: 'Detected: ' + Math.floor(Math.random() * 200) + ' Components',
        aiInsight: 'AI analysis completed successfully.',
        action: '🟢 Auto Scan Started',
        status: 'completed'
      };
      
      setEvents(prev => [newEvent, ...prev.slice(0, 19)]); // Keep only 20 events
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  // Get event type styles
  const getEventTypeStyles = (type: string) => {
    switch (type) {
      case 'upload':
        return { bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800', icon: '📦', color: 'text-blue-600 dark:text-blue-400' };
      case 'vulnerability':
        return { bg: 'bg-red-50 dark:bg-red-900/20', border: 'border-red-200 dark:border-red-800', icon: '🔥', color: 'text-red-600 dark:text-red-400' };
      case 'policy':
        return { bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800', icon: '🧠', color: 'text-orange-600 dark:text-orange-400' };
      case 'ai-fix':
        return { bg: 'bg-green-50 dark:bg-green-900/20', border: 'border-green-200 dark:border-green-800', icon: '🤖', color: 'text-green-600 dark:text-green-400' };
      case 'threat':
        return { bg: 'bg-purple-50 dark:bg-purple-900/20', border: 'border-purple-200 dark:border-purple-800', icon: '🌐', color: 'text-purple-600 dark:text-purple-400' };
      default:
        return { bg: 'bg-gray-50 dark:bg-gray-900/20', border: 'border-gray-200 dark:border-gray-800', icon: '📋', color: 'text-gray-600 dark:text-gray-400' };
    }
  };

  // Get severity styles
  const getSeverityStyles = (severity?: string) => {
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
  const getStatusStyles = (status?: string) => {
    switch (status) {
      case 'completed':
        return { bg: 'bg-green-100 dark:bg-green-900/20', text: 'text-green-800 dark:text-green-400' };
      case 'processing':
        return { bg: 'bg-blue-100 dark:bg-blue-900/20', text: 'text-blue-800 dark:text-blue-400' };
      case 'pending':
        return { bg: 'bg-yellow-100 dark:bg-yellow-900/20', text: 'text-yellow-800 dark:text-yellow-400' };
      case 'failed':
        return { bg: 'bg-red-100 dark:bg-red-900/20', text: 'text-red-800 dark:text-red-400' };
      default:
        return { bg: 'bg-gray-100 dark:bg-gray-900/20', text: 'text-gray-800 dark:text-gray-400' };
    }
  };

  // Handle show more click
  const handleShowMore = (event: LiveEvent) => {
    setSelectedEvent(event);
    setShowModal(true);
  };

  // Close modal
  const closeModal = () => {
    setShowModal(false);
    setSelectedEvent(null);
  };

  return (
    <div className="w-full h-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
                    <div className="px-3 sm:px-4 lg:px-6 py-6">
        {/* Page Header */}
        <PageHeader
          title="Live Feed"
          description="Real-time SBOM analysis events and AI-powered insights"
          icon={
            <svg className="w-6 h-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          }
          actions={
            <div className="flex flex-col items-end space-y-3">
              <div className="flex items-center space-x-3 bg-white dark:bg-gray-800 rounded-full px-4 py-2 shadow-lg border border-gray-200 dark:border-gray-700">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-semibold text-green-600 dark:text-green-400">LIVE</span>
                <span className="text-xs text-gray-500 dark:text-gray-400">•</span>
                <span className="text-sm text-gray-600 dark:text-gray-300 font-medium">
                  {events.length} events
                </span>
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400 text-right">
                Last updated: {new Date().toLocaleTimeString()}
              </div>
            </div>
          }
        />

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-6 lg:gap-8">
          {/* Live Event Stream - Takes 3 columns */}
          <div className="xl:col-span-3">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
              {/* Stream Header */}
              <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white">🎬 Real-Time Event Stream</h2>
                    <p className="text-sm text-gray-600 dark:text-gray-300">Reverse chronological order - newest first</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-xs font-medium text-green-600 dark:text-green-400">ACTIVE</span>
                  </div>
                </div>
              </div>
              
              {/* Event Stream */}
              <div className="max-h-[calc(100vh-300px)] overflow-y-auto">
                <div className="p-6 space-y-4">
                  {events.map((event, index) => {
                    const typeStyles = getEventTypeStyles(event.type);
                    const severityStyles = event.severity ? getSeverityStyles(event.severity) : null;
                    const statusStyles = event.status ? getStatusStyles(event.status) : null;
                    
                    return (
                      <div 
                        key={event.id}
                        className={`relative p-6 rounded-xl border transition-all duration-300 hover:shadow-lg hover:scale-[1.02] ${
                          index === 0 ? 'ring-2 ring-blue-500 ring-opacity-50 animate-pulse' : ''
                        } ${typeStyles.bg} ${typeStyles.border} bg-white dark:bg-gray-800`}
                      >
                        {/* Event Header */}
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center space-x-4">
                            <div className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl ${typeStyles.bg}`}>
                              {typeStyles.icon}
                            </div>
                            <div>
                              <div className="flex items-center space-x-3 mb-1">
                                <span className="text-sm font-medium text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded-full">
                                  🕒 {event.timestamp}
                                </span>
                                <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                                  {event.title}
                                </h3>
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            {severityStyles && (
                              <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold ${severityStyles.bg} ${severityStyles.text} ${severityStyles.border}`}>
                                {event.severity}
                              </span>
                            )}
                            {statusStyles && (
                              <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold ${statusStyles.bg} ${statusStyles.text}`}>
                                {event.status}
                              </span>
                            )}
                          </div>
                        </div>

                        {/* Event Details */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                          {event.project && (
                            <div className="flex items-center space-x-2">
                              <span className="text-gray-400">🏗️</span>
                              <span className="text-sm text-gray-700 dark:text-gray-300">
                                <span className="font-medium">Project:</span> {event.project}
                              </span>
                            </div>
                          )}
                          {event.user && (
                            <div className="flex items-center space-x-2">
                              <span className="text-gray-400">👤</span>
                              <span className="text-sm text-gray-700 dark:text-gray-300">
                                <span className="font-medium">User:</span> {event.user}
                              </span>
                            </div>
                          )}
                          {event.component && (
                            <div className="flex items-center space-x-2">
                              <span className="text-gray-400">🔧</span>
                              <span className="text-sm text-gray-700 dark:text-gray-300">
                                <span className="font-medium">Component:</span> {event.component}
                              </span>
                            </div>
                          )}
                          {event.cve && (
                            <div className="flex items-center space-x-2">
                              <span className="text-gray-400">⚠️</span>
                              <span className="text-sm text-red-600 dark:text-red-400 font-mono">
                                <span className="font-medium">CVE:</span> {event.cve}
                              </span>
                            </div>
                          )}
                        </div>

                        {/* Description */}
                        <div className="mb-4">
                          <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                            {event.details}
                          </p>
                        </div>

                        {/* AI Insight */}
                        {event.aiInsight && (
                          <div className="mb-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                            <div className="flex items-start space-x-2">
                              <span className="text-blue-600 dark:text-blue-400 text-lg">💡</span>
                              <div>
                                <p className="text-sm font-semibold text-blue-800 dark:text-blue-300 mb-1">AI Insight</p>
                                <p className="text-sm text-blue-700 dark:text-blue-200">{event.aiInsight}</p>
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Action and Footer */}
                        <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
                          <div className="flex items-center space-x-3">
                            {event.action && (
                              <span className="text-sm font-semibold text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full">
                                {event.action}
                              </span>
                            )}
                          </div>
                          <button 
                            onClick={() => handleShowMore(event)}
                            className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 text-sm font-semibold transition-colors duration-200 flex items-center space-x-1"
                          >
                            <span>View Details</span>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>

          {/* Right Sidebar - Analytics & Stats */}
          <div className="xl:col-span-1">
            <div className="space-y-6">
              {/* Summary Stats */}
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                  📊 Feed Analytics
                  <span className="ml-2 text-xs bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 px-2 py-1 rounded-full">24h</span>
                </h3>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-900/10 rounded-xl">
                    <div className="flex items-center space-x-3 min-w-0 flex-1">
                      <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0">
                        <span className="text-white text-lg">📦</span>
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">SBOMs Uploaded</p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Last 24 hours</p>
                      </div>
                    </div>
                    <span className="text-lg lg:text-xl xl:text-2xl font-bold text-blue-600 dark:text-blue-400 ml-2 flex-shrink-0">{stats.sbomsUploaded}</span>
                  </div>

                  <div className="flex items-center justify-between p-3 bg-gradient-to-r from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-900/10 rounded-xl">
                    <div className="flex items-center space-x-3 min-w-0 flex-1">
                      <div className="w-10 h-10 bg-red-500 rounded-lg flex items-center justify-center flex-shrink-0">
                        <span className="text-white text-lg">🦠</span>
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Vulnerabilities</p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Detected</p>
                      </div>
                    </div>
                    <span className="text-lg lg:text-xl xl:text-2xl font-bold text-red-600 dark:text-red-400 ml-2 flex-shrink-0">{stats.vulnerabilitiesDetected}</span>
                  </div>

                  <div className="flex items-center justify-between p-3 bg-gradient-to-r from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-900/10 rounded-xl">
                    <div className="flex items-center space-x-3 min-w-0 flex-1">
                      <div className="w-10 h-10 bg-orange-500 rounded-lg flex items-center justify-center flex-shrink-0">
                        <span className="text-white text-lg">⚠️</span>
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Policy Violations</p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Found</p>
                      </div>
                    </div>
                    <span className="text-lg lg:text-xl xl:text-2xl font-bold text-orange-600 dark:text-orange-400 ml-2 flex-shrink-0">{stats.policyViolations}</span>
                  </div>

                  <div className="flex items-center justify-between p-3 bg-gradient-to-r from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-900/10 rounded-xl">
                    <div className="flex items-center space-x-3 min-w-0 flex-1">
                      <div className="w-10 h-10 bg-purple-500 rounded-lg flex items-center justify-center flex-shrink-0">
                        <span className="text-white text-lg">🤖</span>
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">AI Fixes</p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Suggested</p>
                      </div>
                    </div>
                    <span className="text-lg lg:text-xl xl:text-2xl font-bold text-purple-600 dark:text-purple-400 ml-2 flex-shrink-0">{stats.aiFixesSuggested}</span>
                  </div>

                  <div className="flex items-center justify-between p-3 bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-900/10 rounded-xl">
                    <div className="flex items-center space-x-3 min-w-0 flex-1">
                      <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center flex-shrink-0">
                        <span className="text-white text-lg">✅</span>
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Auto Fixes</p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Applied</p>
                      </div>
                    </div>
                    <span className="text-lg lg:text-xl xl:text-2xl font-bold text-green-600 dark:text-green-400 ml-2 flex-shrink-0">{stats.autoFixesApplied}</span>
                  </div>
                </div>
              </div>

              {/* Threat Intelligence */}
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                  📡 Threat Intelligence
                  <span className="ml-2 text-xs bg-green-100 dark:bg-green-900/20 text-green-600 dark:text-green-400 px-2 py-1 rounded-full">LIVE</span>
                </h3>
                
                <div className="space-y-4">
                  <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/10 rounded-xl border border-blue-200 dark:border-blue-800">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-blue-600 dark:text-blue-400">🌐</span>
                      <span className="text-sm font-semibold text-blue-800 dark:text-blue-300">NVD API</span>
                    </div>
                    <p className="text-xs text-blue-700 dark:text-blue-200 leading-relaxed">
                      New CVE-2025-19834 in netty discovered. Monitoring active.
                    </p>
                  </div>

                  <div className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/10 rounded-xl border border-green-200 dark:border-green-800">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-green-600 dark:text-green-400">🧪</span>
                      <span className="text-sm font-semibold text-green-800 dark:text-green-300">OSS Index</span>
                    </div>
                    <p className="text-xs text-green-700 dark:text-green-200 leading-relaxed">
                      Real-time feed of public library exposures. 12 new alerts.
                    </p>
                  </div>

                  <div className="p-4 bg-gradient-to-r from-purple-50 to-violet-50 dark:from-purple-900/20 dark:to-violet-900/10 rounded-xl border border-purple-200 dark:border-purple-800">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-purple-600 dark:text-purple-400">🧠</span>
                      <span className="text-sm font-semibold text-purple-800 dark:text-purple-300">ML Threat Hub</span>
                    </div>
                    <p className="text-xs text-purple-700 dark:text-purple-200 leading-relaxed">
                      Log anomaly detected in build pipeline. Investigation ongoing.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Event Detail Modal */}
      {showModal && selectedEvent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              {/* Modal Header */}
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <span className="text-3xl">{getEventTypeStyles(selectedEvent.type).icon}</span>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                      {selectedEvent.title}
                    </h2>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      🕒 {selectedEvent.timestamp}
                    </p>
                  </div>
                </div>
                <button
                  onClick={closeModal}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* Event Details */}
              <div className="space-y-6">
                {/* Basic Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {selectedEvent.project && (
                    <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                      <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Project</h3>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white">{selectedEvent.project}</p>
                    </div>
                  )}
                  {selectedEvent.user && (
                    <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                      <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">User</h3>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white">{selectedEvent.user}</p>
                    </div>
                  )}
                  {selectedEvent.component && (
                    <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                      <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Component</h3>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white">{selectedEvent.component}</p>
                    </div>
                  )}
                  {selectedEvent.cve && (
                    <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                      <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">CVE</h3>
                      <p className="text-lg font-semibold text-red-600 dark:text-red-400">{selectedEvent.cve}</p>
                    </div>
                  )}
                  {selectedEvent.policy && (
                    <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                      <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Policy</h3>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white">{selectedEvent.policy}</p>
                    </div>
                  )}
                  {selectedEvent.severity && (
                    <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                      <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Severity</h3>
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getSeverityStyles(selectedEvent.severity).bg} ${getSeverityStyles(selectedEvent.severity).text} ${getSeverityStyles(selectedEvent.severity).border}`}>
                        {selectedEvent.severity}
                      </span>
                    </div>
                  )}
                </div>

                {/* Description */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Description</h3>
                  <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <p className="text-gray-700 dark:text-gray-300">{selectedEvent.details}</p>
                  </div>
                </div>

                {/* AI Insight */}
                {selectedEvent.aiInsight && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">🧠 AI Insight</h3>
                    <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                      <p className="text-gray-800 dark:text-gray-200">{selectedEvent.aiInsight}</p>
                    </div>
                  </div>
                )}

                {/* Action */}
                {selectedEvent.action && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Action</h3>
                    <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                      <p className="text-gray-800 dark:text-gray-200 font-medium">{selectedEvent.action}</p>
                    </div>
                  </div>
                )}

                {/* Status */}
                {selectedEvent.status && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Status</h3>
                    <span className={`inline-flex items-center px-3 py-2 rounded-lg text-sm font-medium ${getStatusStyles(selectedEvent.status).bg} ${getStatusStyles(selectedEvent.status).text}`}>
                      {selectedEvent.status}
                    </span>
                  </div>
                )}

                {/* Additional Actions */}
                <div className="flex space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <button className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200">
                    📊 View Full Report
                  </button>
                  <button className="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors duration-200">
                    🔧 Take Action
                  </button>
                  <button className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors duration-200">
                    📋 Export
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

export default LiveFeed; 