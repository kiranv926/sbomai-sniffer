import React, { useState, useMemo } from 'react';
import PageHeader from '../components/PageHeader';

interface Vulnerability {
  id: string;
  name: string;
  aliases: string[];
  published: string;
  cwe: string[];
  projects: number;
  severity: 'Critical' | 'High' | 'Medium' | 'Low' | 'Unassigned';
  description: string;
  cvssScore: number;
  affectedVersion: string;
  fixedVersion?: string;
}

const Vulnerabilities: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showColumnMenu, setShowColumnMenu] = useState(false);
  const [sortField, setSortField] = useState<string>('name');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');

  // Column visibility state
  const [visibleColumns, setVisibleColumns] = useState({
    name: true,
    aliases: false,
    published: true,
    cwe: true,
    projects: true,
    severity: true
  });

  // Mock data for summary cards
  const summaryData = {
    portfolioVulnerabilities: 0,
    projectsAtRisk: 0,
    vulnerableComponents: 0,
    inheritedRiskScore: 0
  };

  // Mock data for vulnerabilities (matching the image format)
  const vulnerabilities: Vulnerability[] = [
    {
      id: '1',
      name: 'NVD CVE-2025-8454',
      aliases: ['CVE-2025-8454'],
      published: '1 Aug 2025',
      cwe: ['CWE-89', 'CWE-74'],
      projects: 0,
      severity: 'High',
      description: 'SQL injection vulnerability in database connector',
      cvssScore: 8.5,
      affectedVersion: '2.1.0'
    },
    {
      id: '2',
      name: 'NVD CVE-2025-8436',
      aliases: ['CVE-2025-8436'],
      published: '1 Aug 2025',
      cwe: ['CWE-770'],
      projects: 0,
      severity: 'Medium',
      description: 'Resource exhaustion vulnerability',
      cvssScore: 5.3,
      affectedVersion: '1.8.2'
    },
    {
      id: '3',
      name: 'NVD CVE-2025-5921',
      aliases: ['CVE-2025-5921'],
      published: '1 Aug 2025',
      cwe: [],
      projects: 0,
      severity: 'Unassigned',
      description: 'Cross-site scripting vulnerability',
      cvssScore: 0,
      affectedVersion: '3.0.1'
    },
    {
      id: '4',
      name: 'NVD CVE-2025-54939',
      aliases: ['CVE-2025-54939'],
      published: '1 Aug 2025',
      cwe: ['CWE-89'],
      projects: 0,
      severity: 'High',
      description: 'SQL injection in query builder',
      cvssScore: 7.8,
      affectedVersion: '4.2.0'
    },
    {
      id: '5',
      name: 'NVD CVE-2025-31716',
      aliases: ['CVE-2025-31716'],
      published: '1 Aug 2025',
      cwe: ['CWE-74'],
      projects: 0,
      severity: 'Medium',
      description: 'Path traversal vulnerability',
      cvssScore: 6.1,
      affectedVersion: '1.5.3'
    },
    {
      id: '6',
      name: 'NVD CVE-2025-8435',
      aliases: ['CVE-2025-8435'],
      published: '1 Aug 2025',
      cwe: [],
      projects: 0,
      severity: 'Unassigned',
      description: 'Memory corruption vulnerability',
      cvssScore: 0,
      affectedVersion: '2.0.0'
    },
    {
      id: '7',
      name: 'NVD CVE-2025-7845',
      aliases: ['CVE-2025-7845'],
      published: '1 Aug 2025',
      cwe: ['CWE-89'],
      projects: 0,
      severity: 'High',
      description: 'SQL injection in authentication module',
      cvssScore: 8.2,
      affectedVersion: '3.1.4'
    },
    {
      id: '8',
      name: 'NVD CVE-2025-7725',
      aliases: ['CVE-2025-7725'],
      published: '1 Aug 2025',
      cwe: ['CWE-770'],
      projects: 0,
      severity: 'Medium',
      description: 'Denial of service vulnerability',
      cvssScore: 5.5,
      affectedVersion: '2.3.1'
    },
    {
      id: '9',
      name: 'NVD CVE-2025-7443',
      aliases: ['CVE-2025-7443'],
      published: '1 Aug 2025',
      cwe: ['CWE-74'],
      projects: 0,
      severity: 'Unassigned',
      description: 'Directory traversal vulnerability',
      cvssScore: 0,
      affectedVersion: '1.9.0'
    }
  ];

  // Filter and sort vulnerabilities
  const filteredAndSortedVulnerabilities = useMemo(() => {
    let filtered = vulnerabilities.filter(vuln => {
      const matchesSearch = vuln.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           vuln.aliases.some(alias => alias.toLowerCase().includes(searchTerm.toLowerCase())) ||
                           vuln.cwe.some(cwe => cwe.toLowerCase().includes(searchTerm.toLowerCase()));

      return matchesSearch;
    });

    // Sort vulnerabilities
    filtered.sort((a, b) => {
      let aValue: any = a[sortField as keyof Vulnerability];
      let bValue: any = b[sortField as keyof Vulnerability];

      if (sortField === 'published') {
        aValue = new Date(aValue).getTime();
        bValue = new Date(bValue).getTime();
      }

      if (sortDirection === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

    return filtered;
  }, [vulnerabilities, searchTerm, sortField, sortDirection]);

  // Get severity styles
  const getSeverityStyles = (severity: string) => {
    switch (severity) {
      case 'Critical':
        return { 
          bg: 'bg-red-100 dark:bg-red-900/20', 
          text: 'text-red-800 dark:text-red-400', 
          border: 'border-red-200 dark:border-red-800',
          icon: '🔴'
        };
      case 'High':
        return { 
          bg: 'bg-orange-100 dark:bg-orange-900/20', 
          text: 'text-orange-800 dark:text-orange-400', 
          border: 'border-orange-200 dark:border-orange-800',
          icon: '🟠'
        };
      case 'Medium':
        return { 
          bg: 'bg-yellow-100 dark:bg-yellow-900/20', 
          text: 'text-yellow-800 dark:text-yellow-400', 
          border: 'border-yellow-200 dark:border-yellow-800',
          icon: '🟡'
        };
      case 'Low':
        return { 
          bg: 'bg-green-100 dark:bg-green-900/20', 
          text: 'text-green-800 dark:text-green-400', 
          border: 'border-green-200 dark:border-green-800',
          icon: '🟢'
        };
      case 'Unassigned':
        return { 
          bg: 'bg-gray-100 dark:bg-gray-900/20', 
          text: 'text-gray-800 dark:text-gray-400', 
          border: 'border-gray-200 dark:border-gray-800',
          icon: '⚪'
        };
      default:
        return { 
          bg: 'bg-gray-100 dark:bg-gray-900/20', 
          text: 'text-gray-800 dark:text-gray-400', 
          border: 'border-gray-200 dark:border-gray-800',
          icon: '⚪'
        };
    }
  };

  // Handle sorting
  const handleSort = (field: string) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };



  // Toggle column visibility
  const toggleColumn = (column: string) => {
    setVisibleColumns(prev => ({
      ...prev,
      [column]: !prev[column as keyof typeof prev]
    }));
  };

  // Create vulnerability
  const createVulnerability = () => {
    alert('Opening vulnerability creation dialog...');
  };

  // Refresh data
  const refreshData = () => {
    alert('Refreshing vulnerability data...');
  };

  return (
    <div className="w-full h-full bg-gray-50 dark:bg-gray-900">
      {/* Page Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="p-6">
          <PageHeader
            title="Vulnerabilities"
            description="Comprehensive vulnerability management and analysis"
            icon={
              <svg className="w-6 h-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            }
            actions={
              <button
                onClick={createVulnerability}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                <span>Create Vulnerability</span>
              </button>
            }
          />
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">{summaryData.portfolioVulnerabilities}</p>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Portfolio Vulnerabilities</p>
              </div>
              <div className="p-3 bg-red-100 dark:bg-red-900/20 rounded-lg">
                <svg className="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">{summaryData.projectsAtRisk}</p>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Projects at Risk</p>
              </div>
              <div className="p-3 bg-orange-100 dark:bg-orange-900/20 rounded-lg">
                <svg className="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">{summaryData.vulnerableComponents}</p>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Vulnerable Components</p>
              </div>
              <div className="p-3 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg">
                <svg className="w-6 h-6 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">{summaryData.inheritedRiskScore}</p>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Inherited Risk Score</p>
              </div>
              <div className="p-3 bg-blue-100 dark:bg-blue-900/20 rounded-lg">
                <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Main Table Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          {/* Table Header with Search and Controls */}
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
              <div className="flex items-center space-x-4">
                {/* Search */}
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64"
                  />
                  <svg className="absolute left-3 top-2.5 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>

                {/* Refresh Button */}
                <button
                  onClick={refreshData}
                  className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors duration-200"
                  title="Refresh"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </button>

                {/* Column Visibility Menu */}
                <div className="relative">
                  <button
                    onClick={() => setShowColumnMenu(!showColumnMenu)}
                    className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors duration-200"
                    title="Column Visibility"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                    </svg>
                  </button>

                  {/* Column Visibility Dropdown */}
                  {showColumnMenu && (
                    <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50">
                      <div className="p-2">
                        <div className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-2 px-2">Column Visibility</div>
                        {Object.entries(visibleColumns).map(([column, isVisible]) => (
                          <label key={column} className="flex items-center px-2 py-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                            <input
                              type="checkbox"
                              checked={isVisible}
                              onChange={() => toggleColumn(column)}
                              className="rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500"
                            />
                            <span className="ml-2 text-sm text-gray-700 dark:text-gray-300 capitalize">
                              {column}
                            </span>
                          </label>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  {visibleColumns.name && (
                    <th 
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
                      onClick={() => handleSort('name')}
                    >
                      <div className="flex items-center space-x-1">
                        <span>Name</span>
                        {sortField === 'name' && (
                          <svg className={`w-4 h-4 ${sortDirection === 'asc' ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                          </svg>
                        )}
                      </div>
                    </th>
                  )}
                  {visibleColumns.aliases && (
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Aliases
                    </th>
                  )}
                  {visibleColumns.published && (
                    <th 
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
                      onClick={() => handleSort('published')}
                    >
                      <div className="flex items-center space-x-1">
                        <span>Published</span>
                        {sortField === 'published' && (
                          <svg className={`w-4 h-4 ${sortDirection === 'asc' ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                          </svg>
                        )}
                      </div>
                    </th>
                  )}
                  {visibleColumns.cwe && (
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      CWE
                    </th>
                  )}
                  {visibleColumns.projects && (
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Projects
                    </th>
                  )}
                  {visibleColumns.severity && (
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Severity
                    </th>
                  )}
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {filteredAndSortedVulnerabilities.map((vuln) => {
                  const severityStyles = getSeverityStyles(vuln.severity);
                  return (
                    <tr key={vuln.id} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                      {visibleColumns.name && (
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">{vuln.name}</div>
                        </td>
                      )}
                      {visibleColumns.aliases && (
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900 dark:text-white">
                            {vuln.aliases.join(', ')}
                          </div>
                        </td>
                      )}
                      {visibleColumns.published && (
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900 dark:text-white">{vuln.published}</div>
                        </td>
                      )}
                      {visibleColumns.cwe && (
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900 dark:text-white">
                            {vuln.cwe.length > 0 ? vuln.cwe.join(', ') : '-'}
                          </div>
                        </td>
                      )}
                      {visibleColumns.projects && (
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900 dark:text-white">{vuln.projects}</div>
                        </td>
                      )}
                      {visibleColumns.severity && (
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${severityStyles.bg} ${severityStyles.text} ${severityStyles.border}`}>
                            {severityStyles.icon} {vuln.severity}
                          </span>
                        </td>
                      )}
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium text-sm transition-colors duration-200">
                          View
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Table Footer */}
          <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-700 dark:text-gray-300">
                Showing {filteredAndSortedVulnerabilities.length} of {vulnerabilities.length} vulnerabilities
              </div>
              <div className="flex items-center space-x-2">
                <button className="px-3 py-1 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors duration-200">
                  Previous
                </button>
                <span className="px-3 py-1 text-sm text-gray-900 dark:text-white">1</span>
                <button className="px-3 py-1 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors duration-200">
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Vulnerabilities; 