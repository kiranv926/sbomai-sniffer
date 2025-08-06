import React from 'react';
import { Link, useLocation } from 'react-router-dom';

interface BreadcrumbItem {
  name: string;
  path: string;
  icon: string;
  description?: string;
}

interface BreadcrumbProps {
  items?: BreadcrumbItem[];
  showBackButton?: boolean;
  showSearch?: boolean;
}

const Breadcrumb: React.FC<BreadcrumbProps> = ({ 
  items, 
  showBackButton = true, 
  showSearch = false 
}) => {
  const location = useLocation();
  const [searchTerm, setSearchTerm] = React.useState('');



  // Default breadcrumb mapping based on current route
  const getDefaultBreadcrumbs = (): BreadcrumbItem[] => {
    const pathSegments = location.pathname.split('/').filter(Boolean);
         const breadcrumbs: BreadcrumbItem[] = [
       { name: 'Home', path: '/', icon: 'home' }
     ];

    if (pathSegments.length === 0) {
      return breadcrumbs;
    }

         const routeMap: { [key: string]: { name: string; icon: string; description?: string } } = {
       'dashboard': { name: 'Dashboard', icon: 'dashboard', description: 'Overview & Analytics' },
       'vulnerabilities': { name: 'Vulnerabilities', icon: 'shield', description: 'Security Issues' },
       'ai-analysis': { name: 'AI Analysis', icon: 'brain', description: 'AI-Powered Insights' },
       'ai-assist': { name: 'AI Assist', icon: 'chat', description: 'AI Chat Assistant' },
       'live-feed': { name: 'Live Feed', icon: 'broadcast', description: 'Real-time Events' },
       'policy-engine': { name: 'Policy Engine', icon: 'settings', description: 'Security Policies' },
       'github-insights': { name: 'GitHub Insights', icon: 'trending-up', description: 'Repository Analysis' },
       'web-scan': { name: 'Web Scan', icon: 'globe', description: 'Web Security Scanning' },
       'integrations': { name: 'Integrations', icon: 'link', description: 'Tool Connections' },
       'model-configuration': { name: 'Model Configuration', icon: 'cog', description: 'AI Model Settings' }
     };

    let currentPath = '';
    pathSegments.forEach((segment) => {
      currentPath += `/${segment}`;
      const routeInfo = routeMap[segment];
      
      if (routeInfo) {
        breadcrumbs.push({
          name: routeInfo.name,
          path: currentPath,
          icon: routeInfo.icon,
          description: routeInfo.description
        });
      } else {
                 // Handle dynamic segments (like specific vulnerability IDs, project names, etc.)
         breadcrumbs.push({
           name: segment.charAt(0).toUpperCase() + segment.slice(1).replace(/-/g, ' '),
           path: currentPath,
           icon: 'folder'
         });
      }
    });

    return breadcrumbs;
  };

     const breadcrumbItems = items || getDefaultBreadcrumbs();

   // Function to render SVG icons
   const renderIcon = (iconName: string) => {
     const iconClass = "w-4 h-4";
     switch (iconName) {
       case 'home':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
           </svg>
         );
       case 'dashboard':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
           </svg>
         );
       case 'shield':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
           </svg>
         );
       case 'brain':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
           </svg>
         );
       case 'chat':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
           </svg>
         );
       case 'broadcast':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
           </svg>
         );
       case 'settings':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
           </svg>
         );
       case 'trending-up':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
           </svg>
         );
       case 'globe':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
           </svg>
         );
       case 'link':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
           </svg>
         );
       case 'cog':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
           </svg>
         );
       case 'folder':
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-5l-2-2H5a2 2 0 00-2 2z" />
           </svg>
         );
       default:
         return (
           <svg className={iconClass} fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-5l-2-2H5a2 2 0 00-2 2z" />
           </svg>
         );
     }
   };

  const handleBackClick = () => {
    if (breadcrumbItems.length > 1) {
      const previousPath = breadcrumbItems[breadcrumbItems.length - 2].path;
      window.location.href = previousPath;
    }
  };

  const filteredItems = showSearch && searchTerm
    ? breadcrumbItems.filter(item => 
        item.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : breadcrumbItems;

  return (
    <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-3">
      <div className="flex items-center justify-between">
        {/* Breadcrumb Trail */}
        <div className="flex items-center space-x-2 flex-1 min-w-0">
          {showBackButton && breadcrumbItems.length > 1 && (
            <button
              onClick={handleBackClick}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200 mr-2"
              title="Go back"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
          )}

          {/* Search (Optional) */}
          {showSearch && (
            <div className="relative mr-4">
              <input
                type="text"
                placeholder="Search breadcrumbs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-48 px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <svg className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          )}

          {/* Breadcrumb Items */}
          <div className="flex items-center space-x-2 overflow-x-auto scrollbar-hide">
            {filteredItems.map((item, index) => {
              const isLast = index === filteredItems.length - 1;
              const isClickable = !isLast;

              return (
                <React.Fragment key={item.path}>
                  {isClickable ? (
                                         <Link
                       to={item.path}
                       className="flex items-center space-x-1 px-3 py-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200 group"
                       title={item.description}
                     >
                       <span className="text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-300">
                         {renderIcon(item.icon)}
                       </span>
                       <span className="text-sm text-gray-600 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white font-medium">
                         {item.name}
                       </span>
                     </Link>
                   ) : (
                     <div className="flex items-center space-x-1 px-3 py-1">
                       <span className="text-gray-500 dark:text-gray-400">
                         {renderIcon(item.icon)}
                       </span>
                       <span className="text-sm font-bold text-gray-900 dark:text-white">
                         {item.name}
                       </span>
                     </div>
                   )}
                  
                  {!isLast && (
                    <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  )}
                </React.Fragment>
              );
            })}
          </div>
        </div>


      </div>
    </div>
  );
};

export default Breadcrumb; 