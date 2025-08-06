import React, { useState, useRef, useEffect } from 'react';
import PageHeader from '../components/PageHeader';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isLoading?: boolean;
}

interface QuickAction {
  id: string;
  title: string;
  description: string;
  icon: string;
  action: string;
}

const AIAssist: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: "Hello! I'm your AI Security Assistant. I can help you with:\n\n• Vulnerability analysis and remediation\n• SBOM security assessment\n• Dependency risk evaluation\n• Security policy recommendations\n• Code security review\n\nHow can I assist you today?",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const quickActions: QuickAction[] = [
    {
      id: '1',
      title: 'Analyze Vulnerabilities',
      description: 'Get detailed analysis of security vulnerabilities',
      icon: '🛡️',
      action: 'Please analyze the vulnerabilities in my current SBOM and provide remediation recommendations.'
    },
    {
      id: '2',
      title: 'Dependency Risk Assessment',
      description: 'Evaluate risks in your dependencies',
      icon: '📊',
      action: 'Can you assess the security risks in my project dependencies and suggest safer alternatives?'
    },
    {
      id: '3',
      title: 'Security Policy Review',
      description: 'Review and improve security policies',
      icon: '⚙️',
      action: 'Help me review my current security policies and suggest improvements for better protection.'
    },
    {
      id: '4',
      title: 'Code Security Scan',
      description: 'Scan code for security issues',
      icon: '🔍',
      action: 'I need help scanning my codebase for potential security vulnerabilities and best practices.'
    },
    {
      id: '5',
      title: 'SBOM Generation Guide',
      description: 'Learn how to generate secure SBOMs',
      icon: '📋',
      action: 'Can you guide me through generating a comprehensive and secure Software Bill of Materials?'
    },
    {
      id: '6',
      title: 'Incident Response',
      description: 'Get help with security incidents',
      icon: '🚨',
      action: 'I suspect a security incident. Can you help me assess the situation and provide response guidance?'
    }
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = generateAIResponse(message);
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: aiResponse,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const generateAIResponse = (userMessage: string): string => {
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes('vulnerability') || lowerMessage.includes('cve')) {
      return `I've analyzed your vulnerability concerns. Here's what I found:\n\n🔍 **Current Status:**\n• 3 critical vulnerabilities detected\n• 7 high-risk dependencies identified\n• 2 outdated packages requiring updates\n\n🛠️ **Recommended Actions:**\n1. Update log4j-core to version 2.17.1 immediately\n2. Replace vulnerable jQuery with a modern alternative\n3. Implement proper input validation in authentication module\n\n📊 **Risk Assessment:**\n• Overall risk score: 7.8/10 (High)\n• Immediate action required for 2 items\n• 5 items can be addressed in next sprint\n\nWould you like me to provide detailed remediation steps for any specific vulnerability?`;
    }
    
    if (lowerMessage.includes('dependency') || lowerMessage.includes('risk')) {
      return `Here's my dependency risk assessment:\n\n📦 **Dependency Analysis:**\n• Total dependencies: 156\n• High-risk packages: 12\n• Outdated packages: 23\n• Unused dependencies: 8\n\n⚠️ **Critical Findings:**\n1. **express-session** (v1.17.0) - Known session fixation vulnerability\n2. **moment.js** (v2.29.0) - Multiple ReDoS vulnerabilities\n3. **lodash** (v4.17.15) - Prototype pollution risk\n\n🔄 **Recommended Updates:**\n• Upgrade express-session to v1.17.3+\n• Replace moment.js with dayjs or date-fns\n• Update lodash to v4.17.21+\n\n💡 **Pro Tips:**\n• Enable automated dependency scanning in CI/CD\n• Set up weekly security updates\n• Use dependency lock files for consistency\n\nWould you like me to generate a detailed upgrade plan?`;
    }
    
    if (lowerMessage.includes('policy') || lowerMessage.includes('security policy')) {
      return `I'll help you review and improve your security policies:\n\n📋 **Current Policy Assessment:**\n• ✅ Dependency scanning enabled\n• ⚠️ Code review policy needs strengthening\n• ❌ No automated security testing\n• ⚠️ Access control policies outdated\n\n🔧 **Recommended Improvements:**\n\n1. **Code Review Policy:**\n   • Require security-focused code reviews\n   • Mandate vulnerability scanning before merge\n   • Implement automated SAST tools\n\n2. **Access Control:**\n   • Implement least privilege principle\n   • Regular access reviews (quarterly)\n   • Multi-factor authentication for all accounts\n\n3. **Incident Response:**\n   • Create detailed incident response plan\n   • Establish communication protocols\n   • Regular incident response drills\n\n4. **Training & Awareness:**\n   • Monthly security training sessions\n   • Phishing simulation exercises\n   • Security best practices documentation\n\nWould you like me to help you draft specific policy documents?`;
    }
    
    if (lowerMessage.includes('code') || lowerMessage.includes('scan')) {
      return `I'll help you scan your codebase for security issues:\n\n🔍 **Code Security Analysis:**\n\n**Critical Issues Found:**\n1. **SQL Injection Risk** (Line 45, auth.js)\n   - Raw SQL queries without parameterization\n   - Risk: High | Impact: Data breach\n\n2. **XSS Vulnerability** (Line 123, user.js)\n   - Unvalidated user input in HTML output\n   - Risk: High | Impact: Session hijacking\n\n3. **Hardcoded Secrets** (Line 67, config.js)\n   - API keys exposed in source code\n   - Risk: Critical | Impact: Complete compromise\n\n**Medium Priority Issues:**\n• 5 instances of weak password validation\n• 3 cases of improper error handling\n• 2 potential race conditions\n\n**Recommendations:**\n1. Use parameterized queries for all database operations\n2. Implement proper input validation and sanitization\n3. Move secrets to environment variables\n4. Add comprehensive error handling\n5. Implement proper logging and monitoring\n\nWould you like me to provide specific code examples for fixing these issues?`;
    }
    
    if (lowerMessage.includes('sbom') || lowerMessage.includes('bill of materials')) {
      return 'I\'ll guide you through generating a comprehensive SBOM:\n\n📋 **SBOM Generation Guide:**\n\n**Step 1: Choose Your Tool**\n• **CycloneDX**: Industry standard, comprehensive\n• **SPDX**: ISO standard, detailed licensing\n• **SWID**: Government/enterprise focused\n\n**Step 2: Generate SBOM**\n```bash\n# Using CycloneDX\nnpm install -g @cyclonedx/cyclonedx-npm\ncyclonedx-npm --output-file bom.xml\n\n# Using SPDX\nnpm install -g @spdx/spdx-sbom-generator\nspdx-sbom-generator -p . -o spdx.json\n```\n\n**Step 3: Include Essential Information**\n• All direct and transitive dependencies\n• Version information and checksums\n• License details and compliance\n• Vulnerability data (if available)\n• Build and deployment context\n\n**Step 4: Validate and Verify**\n• Check for completeness and accuracy\n• Validate against schema standards\n• Include in CI/CD pipeline\n• Regular updates and maintenance\n\n**Best Practices:**\n• Generate SBOMs automatically in CI/CD\n• Include both development and production dependencies\n• Maintain historical SBOM versions\n• Integrate with vulnerability scanning tools\n\nWould you like me to help you set up automated SBOM generation for your project?';
    }
    
    if (lowerMessage.includes('incident') || lowerMessage.includes('breach')) {
      return `I understand you're dealing with a potential security incident. Here's my incident response guidance:\n\n🚨 **Immediate Response Steps:**\n\n1. **Assess the Situation**\n   • Determine scope and impact\n   • Identify affected systems and data\n   • Document everything immediately\n\n2. **Contain the Threat**\n   • Isolate affected systems\n   • Disable compromised accounts\n   • Block suspicious IP addresses\n   • Preserve evidence\n\n3. **Communicate**\n   • Notify security team and management\n   • Contact legal and compliance teams\n   • Prepare customer notifications (if needed)\n   • Coordinate with law enforcement (if required)\n\n4. **Investigate**\n   • Conduct thorough forensic analysis\n   • Identify root cause and attack vector\n   • Assess data exposure and impact\n   • Document findings and timeline\n\n5. **Remediate**\n   • Patch vulnerabilities\n   • Update security controls\n   • Implement additional monitoring\n   • Review and update incident response plan\n\n**Important:**\n• Don't delete any logs or evidence\n• Follow your organization's incident response plan\n• Consider engaging external security experts\n• Document all actions taken\n\nWould you like me to help you create a detailed incident response checklist?`;
    }

    // Default response
    return `I understand you're asking about "${userMessage}". Let me provide you with some helpful information:\n\n🔍 **Analysis:**\nI can help you with various security and SBOM-related topics including:\n\n• **Vulnerability Management**: Identify, assess, and remediate security vulnerabilities\n• **Dependency Analysis**: Evaluate risks in your software dependencies\n• **Security Policies**: Review and improve your security frameworks\n• **Code Security**: Scan and analyze code for security issues\n• **SBOM Management**: Generate and maintain Software Bills of Materials\n• **Incident Response**: Handle security incidents effectively\n\n💡 **Next Steps:**\nTo provide more specific assistance, could you please:\n1. Share more details about your specific concern\n2. Provide context about your project or environment\n3. Let me know what type of security analysis you need\n\nI'm here to help you maintain a secure and compliant software environment!`;
  };

  const handleQuickAction = (action: string) => {
    handleSendMessage(action);
  };

  return (
    <div className="w-full h-full bg-gray-50 dark:bg-gray-900">
      <div className="p-6">
        {/* Page Header */}
        <PageHeader
          title="AI Security Assistant"
          description="Your intelligent security companion for SBOM analysis, vulnerability assessment, and security guidance."
          icon={
            <svg className="w-6 h-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          }
        />

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-200px)]">
          {/* Chat Interface */}
          <div className="lg:col-span-3 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 flex flex-col">
            {/* Chat Header */}
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-lg">🤖</span>
                  </div>
                  <div>
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">AI Security Assistant</h2>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {isTyping ? 'Typing...' : 'Online'}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-green-600 dark:text-green-400 font-medium">Active</span>
                </div>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                      message.type === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{message.content}</div>
                    <div className={`text-xs mt-2 ${
                      message.type === 'user' ? 'text-blue-100' : 'text-gray-500 dark:text-gray-400'
                    }`}>
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              ))}
              
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
                    <div className="flex items-center space-x-2">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                      <span className="text-sm text-gray-500 dark:text-gray-400">AI is typing...</span>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-6 border-t border-gray-200 dark:border-gray-700">
              <div className="flex space-x-4">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage(inputMessage)}
                  placeholder="Ask me about security, vulnerabilities, SBOMs, or any security concerns..."
                  className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  disabled={isTyping}
                />
                <button
                  onClick={() => handleSendMessage(inputMessage)}
                  disabled={!inputMessage.trim() || isTyping}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2"
                >
                  <span>Send</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          {/* Quick Actions Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <span className="mr-2">⚡</span>
                Quick Actions
              </h3>
              
              <div className="space-y-3">
                {quickActions.map((action) => (
                  <button
                    key={action.id}
                    onClick={() => handleQuickAction(action.action)}
                    disabled={isTyping}
                    className="w-full p-4 text-left bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg border border-gray-200 dark:border-gray-600 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <div className="flex items-start space-x-3">
                      <span className="text-2xl">{action.icon}</span>
                      <div>
                        <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-1">
                          {action.title}
                        </h4>
                        <p className="text-xs text-gray-600 dark:text-gray-400">
                          {action.description}
                        </p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>

              {/* AI Capabilities */}
              <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-3">AI Capabilities</h4>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2 text-xs text-gray-600 dark:text-gray-400">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span>Vulnerability Analysis</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs text-gray-600 dark:text-gray-400">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span>SBOM Security Assessment</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs text-gray-600 dark:text-gray-400">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span>Dependency Risk Evaluation</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs text-gray-600 dark:text-gray-400">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span>Security Policy Review</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs text-gray-600 dark:text-gray-400">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span>Code Security Analysis</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs text-gray-600 dark:text-gray-400">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span>Incident Response Guidance</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAssist; 