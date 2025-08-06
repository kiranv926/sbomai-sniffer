import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';

interface AdminSection {
  id: string;
  name: string;
  icon: React.ReactNode;
  subsections?: string[];
}

const Administration: React.FC = () => {
  const [selectedSection, setSelectedSection] = useState('general');
  const [expandedSection, setExpandedSection] = useState('configuration');

  const adminSections: AdminSection[] = [
    {
      id: 'configuration',
      name: 'Configuration',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      ),
      subsections: ['General', 'BOM Formats', 'Email', 'Welcome Message', 'Internal Components', 'Task scheduler', 'Telemetry', 'Search']
    },
    {
      id: 'analyzers',
      name: 'Analyzers',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      )
    },
    {
      id: 'vulnerability-sources',
      name: 'Vulnerability Sources',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      )
    },
    {
      id: 'repositories',
      name: 'Repositories',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z" />
        </svg>
      )
    },
    {
      id: 'notifications',
      name: 'Notifications',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      )
    },
    {
      id: 'integrations',
      name: 'Integrations',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
        </svg>
      )
    },
    {
      id: 'access-management',
      name: 'Access Management',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
        </svg>
      ),
      subsections: ['LDAP Users', 'Managed Users', 'OpenID Connect Users', 'OpenID Connect Groups', 'Teams', 'Permissions', 'Portfolio Access Control']
    }
  ];

  const renderGeneralSettings = () => (
    <div className="space-y-6">
      {/* Base URL Section */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Base URL
        </label>
        <div className="relative">
          <input
            type="text"
            placeholder="Base URL"
            className="w-full px-3 py-2 border border-red-300 dark:border-red-600 rounded-md focus:ring-2 focus:ring-red-500 focus:border-red-500 dark:bg-gray-700 dark:text-white transition-all duration-200"
          />
          <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex space-x-1">
            <div className="w-5 h-5 bg-red-500 rounded-full flex items-center justify-center text-white text-xs shadow-sm">
              !
            </div>
            <div className="w-5 h-5 bg-blue-500 rounded flex items-center justify-center text-white text-xs shadow-sm">
              i
            </div>
          </div>
        </div>
      </div>

      {/* SVG Badge Access */}
      <div className="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
        <input
          type="checkbox"
          id="svg-badge-access"
          className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600 transition-colors duration-200"
        />
        <label htmlFor="svg-badge-access" className="text-sm font-medium text-gray-700 dark:text-gray-300">
          Enable unauthenticated SVG badge access
        </label>
      </div>

      {/* Default Language Section */}
      <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          Default Language
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
          Default language, which is used for everyone, when they didn't specify one. Language from Browser will be used, when this is disabled.
        </p>
        
        <div className="flex items-center space-x-3 mb-4">
          <input
            type="checkbox"
            id="enable-default-language"
            className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600 transition-colors duration-200"
          />
          <label htmlFor="enable-default-language" className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Enable Default language
          </label>
        </div>

        <select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-all duration-200">
          <option value="">Select Language</option>
          <option value="en">English</option>
          <option value="es">Spanish</option>
          <option value="fr">French</option>
          <option value="de">German</option>
          <option value="it">Italian</option>
          <option value="pt">Portuguese</option>
          <option value="ru">Russian</option>
          <option value="zh">Chinese</option>
          <option value="ja">Japanese</option>
          <option value="ko">Korean</option>
        </select>
      </div>

      {/* Update Button */}
      <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
        <button className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-all duration-200 transform hover:scale-105 shadow-md hover:shadow-lg">
          Update
        </button>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (selectedSection) {
      case 'general':
        return renderGeneralSettings();
      default:
        return (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🔧</div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              {adminSections.find(s => s.id === selectedSection)?.name} Settings
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Configuration options for {adminSections.find(s => s.id === selectedSection)?.name.toLowerCase()} will be displayed here.
            </p>
          </div>
        );
    }
  };

  return (
    <div className="w-full h-full bg-gray-50 dark:bg-gray-900 flex">
      {/* Left Sidebar - Matching main navigation colors */}
      <div className="w-64 bg-gray-900 dark:bg-gray-950 text-white flex-shrink-0 border-r border-gray-700 dark:border-gray-800">
        <nav className="mt-4">
          {adminSections.map((section) => (
            <div key={section.id}>
              <button
                onClick={() => {
                  if (section.subsections) {
                    setExpandedSection(expandedSection === section.id ? '' : section.id);
                  } else {
                    setSelectedSection(section.id);
                  }
                }}
                className={`w-full flex items-center px-4 py-3 text-left transition-colors duration-200 ${
                  (section.subsections && expandedSection === section.id) || 
                  (!section.subsections && selectedSection === section.id)
                    ? 'bg-blue-600 text-white' 
                    : 'text-gray-300 hover:text-white hover:bg-gray-700 dark:hover:bg-gray-800'
                }`}
              >
                <span className="mr-3">{section.icon}</span>
                <span className="flex-1">{section.name}</span>
                {section.subsections && (
                  <svg 
                    className={`w-4 h-4 transition-transform duration-200 ${
                      expandedSection === section.id ? 'rotate-180' : ''
                    }`} 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                )}
              </button>
              
                             {section.subsections && expandedSection === section.id && (
                 <div className="bg-gray-800 dark:bg-gray-900">
                   {section.subsections.map((subsection, index) => (
                     <button
                       key={index}
                       onClick={() => setSelectedSection(subsection.toLowerCase().replace(' ', '-'))}
                       className={`w-full flex items-center px-8 py-2 text-left text-sm transition-colors duration-200 ${
                         selectedSection === subsection.toLowerCase().replace(' ', '-') 
                           ? 'bg-blue-600 text-white' 
                           : 'text-gray-300 hover:text-white hover:bg-gray-700 dark:hover:bg-gray-800'
                       }`}
                     >
                       {subsection}
                     </button>
                   ))}
                 </div>
               )}
            </div>
          ))}
        </nav>
      </div>

      {/* Main Content Area - Enhanced transition */}
      <div className="flex-1 p-8 bg-gradient-to-br from-gray-50 via-gray-100 to-gray-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="max-w-4xl">
          {/* Breadcrumb */}
          <div className="mb-6">
            <nav className="flex" aria-label="Breadcrumb">
              <ol className="inline-flex items-center space-x-1 md:space-x-3">
                <li className="inline-flex items-center">
                  <a href="#" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200">
                    Home
                  </a>
                </li>
                <li>
                  <div className="flex items-center">
                    <svg className="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd"></path>
                    </svg>
                    <span className="text-gray-500 dark:text-gray-400">Administration</span>
                  </div>
                </li>
              </ol>
            </nav>
          </div>

                     {/* Page Header */}
           <PageHeader
             title={adminSections.find(s => s.id === selectedSection)?.name || 
                    adminSections.find(s => s.subsections?.some(sub => sub.toLowerCase().replace(' ', '-') === selectedSection))?.subsections?.find(sub => sub.toLowerCase().replace(' ', '-') === selectedSection) || 
                    'General'}
             description="Configure system settings, manage users, and control application behavior."
             icon={
               <svg className="w-6 h-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
               </svg>
             }
           />

          {/* Content */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6 transition-all duration-300 hover:shadow-xl">
            {renderContent()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Administration; 