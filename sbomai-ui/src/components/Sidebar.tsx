import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../hooks/useTheme';

interface SidebarProps {
  onToggle?: (collapsed: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onToggle }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const location = useLocation();

  const handleToggle = () => {
    const newCollapsedState = !isCollapsed;
    setIsCollapsed(newCollapsedState);
    onToggle?.(newCollapsedState);
  };

     const navGroups = [
       {
         title: 'Overview & Analytics',
         items: [
           { 
             name: 'Dashboard', 
             href: '/dashboard', 
             icon: (
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
               </svg>
             )
           },
           {
             name: 'Projects',
             href: '/projects',
             icon: (
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
               </svg>
             )
           },
           {
             name: 'Security Insights',
             href: '/security-insights',
             icon: (
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
               </svg>
             )
           }
         ]
       },
       {
         title: 'Security & Monitoring',
         items: [
           { 
             name: 'Vulnerabilities', 
             href: '/vulnerabilities', 
             icon: (
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
               </svg>
             )
           },
           { 
             name: 'Live Feed', 
             href: '/live-feed', 
             icon: (
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
               </svg>
             )
           },
           { 
             name: 'Web Scan', 
             href: '/web-scan', 
             icon: (
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
               </svg>
             )
           }
         ]
       },
               {
          title: 'AI & Intelligence',
          items: [
            { 
              name: 'AI Analysis', 
              href: '/ai-repository-analysis', 
              icon: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              )
            },
            { 
              name: 'AI Assist', 
              href: '/ai-assist', 
              icon: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              )
            }
          ]
        },
       {
         title: 'Configuration & Management',
         items: [
           { 
             name: 'Policy Engine', 
             href: '/policy-engine', 
             icon: (
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
               </svg>
             )
           },
           { 
             name: 'Integrations', 
             href: '/integrations', 
             icon: (
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
               </svg>
             )
           },
           { 
             name: 'Model Configuration', 
             href: '/model-configuration', 
             icon: (
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
               </svg>
             )
           }
         ]
       },
       {
         title: 'Administration',
         items: [
           { 
             name: 'Administration', 
             href: '/administration', 
             icon: (
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
               </svg>
             )
           },
           { 
             name: 'Breadcrumb Demo', 
             href: '/breadcrumb-demo', 
             icon: (
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m0 0L9 7" />
               </svg>
             )
           }
         ]
       }
     ];

  return (
    <div className={`bg-gray-900 dark:bg-gray-950 text-white transition-all duration-300 ease-in-out ${isCollapsed ? 'w-16' : 'w-64'} min-h-screen flex-shrink-0 flex flex-col`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-700 dark:border-gray-800 relative">
        {!isCollapsed && (
          <Link to="/" className="flex items-center space-x-3 text-white hover:text-blue-300 transition-colors duration-200">
            {/* SBOM AI Sniffer Icon */}
            <div className="flex-shrink-0">
              <svg className="w-8 h-8" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                {/* Background Circle */}
                <circle cx="16" cy="16" r="15" fill="url(#gradient1)" stroke="currentColor" strokeWidth="1"/>
                
                {/* SS Letters */}
                <path d="M10 12C10 10.8954 10.8954 10 12 10H14C15.1046 10 16 10.8954 16 12V14C16 15.1046 15.1046 16 14 16H12C10.8954 16 10 15.1046 10 14V12Z" fill="currentColor"/>
                <path d="M16 16C16 14.8954 16.8954 14 18 14H20C21.1046 14 22 14.8954 22 16V18C22 19.1046 21.1046 20 20 20H18C16.8954 20 16 19.1046 16 18V16Z" fill="currentColor"/>
                
                {/* AI Neural Network Dots */}
                <circle cx="8" cy="24" r="1" fill="url(#gradient2)"/>
                <circle cx="12" cy="24" r="1" fill="url(#gradient2)"/>
                <circle cx="16" cy="24" r="1" fill="url(#gradient2)"/>
                <circle cx="20" cy="24" r="1" fill="url(#gradient2)"/>
                <circle cx="24" cy="24" r="1" fill="url(#gradient2)"/>
                
                {/* AI Connections */}
                <path d="M8 24L12 24" stroke="currentColor" strokeWidth="1" opacity="0.6"/>
                <path d="M12 24L16 24" stroke="currentColor" strokeWidth="1" opacity="0.6"/>
                <path d="M16 24L20 24" stroke="currentColor" strokeWidth="1" opacity="0.6"/>
                <path d="M20 24L24 24" stroke="currentColor" strokeWidth="1" opacity="0.6"/>
                
                {/* Gradients */}
                <defs>
                  <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#3B82F6"/>
                    <stop offset="100%" stopColor="#8B5CF6"/>
                  </linearGradient>
                  <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#10B981"/>
                    <stop offset="100%" stopColor="#F59E0B"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <span className="text-xl font-bold">SBOMAI Sniffer</span>
          </Link>
        )}
        {isCollapsed && (
          <Link to="/" className="flex items-center justify-center text-white hover:text-blue-300 transition-colors duration-200" title="Go to Home">
            {/* Collapsed Icon */}
            <svg className="w-8 h-8" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              {/* Background Circle */}
              <circle cx="16" cy="16" r="15" fill="url(#gradient1)" stroke="currentColor" strokeWidth="1"/>
              
              {/* SS Letters */}
              <path d="M10 12C10 10.8954 10.8954 10 12 10H14C15.1046 10 16 10.8954 16 12V14C16 15.1046 15.1046 16 14 16H12C10.8954 16 10 15.1046 10 14V12Z" fill="currentColor"/>
              <path d="M16 16C16 14.8954 16.8954 14 18 14H20C21.1046 14 22 14.8954 22 16V18C22 19.1046 21.1046 20 20 20H18C16.8954 20 16 19.1046 16 18V16Z" fill="currentColor"/>
              
              {/* AI Neural Network Dots */}
              <circle cx="8" cy="24" r="1" fill="url(#gradient2)"/>
              <circle cx="12" cy="24" r="1" fill="url(#gradient2)"/>
              <circle cx="16" cy="24" r="1" fill="url(#gradient2)"/>
              <circle cx="20" cy="24" r="1" fill="url(#gradient2)"/>
              <circle cx="24" cy="24" r="1" fill="url(#gradient2)"/>
              
              {/* AI Connections */}
              <path d="M8 24L12 24" stroke="currentColor" strokeWidth="1" opacity="0.6"/>
              <path d="M12 24L16 24" stroke="currentColor" strokeWidth="1" opacity="0.6"/>
              <path d="M16 24L20 24" stroke="currentColor" strokeWidth="1" opacity="0.6"/>
              <path d="M20 24L24 24" stroke="currentColor" strokeWidth="1" opacity="0.6"/>
              
              {/* Gradients */}
              <defs>
                <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#3B82F6"/>
                  <stop offset="100%" stopColor="#8B5CF6"/>
                </linearGradient>
                <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#10B981"/>
                  <stop offset="100%" stopColor="#F59E0B"/>
                </linearGradient>
              </defs>
            </svg>
          </Link>
        )}
        
        <div className="flex items-center space-x-1">
          {/* Theme Toggle Button - Hide when collapsed to save space */}
          {!isCollapsed && (
            <button
              onClick={toggleTheme}
              className="p-2 rounded-md hover:bg-gray-700 dark:hover:bg-gray-800 transition-colors duration-200"
              title={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
            >
              {theme === 'light' ? (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              )}
            </button>
          )}
          
          {/* Collapse Toggle Button - Always visible */}
          <button
            onClick={handleToggle}
            className="p-1 rounded hover:bg-gray-700 dark:hover:bg-gray-800 transition-colors duration-200"
            title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {isCollapsed ? (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
              </svg>
            ) : (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7M19 19l-7-7 7-7" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="mt-4 space-y-4">
        {navGroups.map((group) => (
          <div key={group.title} className="px-3">
            {/* Group Title */}
            {!isCollapsed && (
              <div className="px-3 py-1">
                <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                  {group.title}
                </h3>
              </div>
            )}
            
            {/* Group Items */}
            <div className="space-y-0.5">
              {group.items.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center px-3 py-2 rounded-md transition-colors duration-200 group relative ${
                      isActive 
                        ? 'bg-blue-600 text-white' 
                        : 'text-gray-300 hover:text-white hover:bg-gray-700 dark:hover:bg-gray-800'
                    }`}
                  >
                    <span className="mr-3">{item.icon}</span>
                    {!isCollapsed && (
                      <span className="text-sm font-medium">{item.name}</span>
                    )}
                    {isCollapsed && (
                      <div className="absolute left-16 bg-gray-800 dark:bg-gray-900 text-white text-sm px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap z-50">
                        {item.name}
                      </div>
                    )}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="mt-auto p-4 border-t border-gray-700 dark:border-gray-800">
        {!isCollapsed && (
          <div className="text-xs text-gray-400 text-center">
            SBOM AI Sniffer v1.0.0
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar; 