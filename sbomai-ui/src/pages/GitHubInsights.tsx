import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell, PieChart, Pie } from 'recharts';
import PageHeader from '../components/PageHeader';

interface Repository {
  id: string;
  name: string;
  owner: string;
  language: string;
  dependencyCount: number;
  cveCount: number;
  riskScore: number;
  lastScanned: string;
  lastCommit: string;
  team: string;
  isActive: boolean;
  prCount: number;
  outdatedDeps: number;
}

interface PullRequest {
  id: string;
  title: string;
  repo: string;
  author: string;
  status: 'open' | 'merged' | 'closed';
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
  sbomChanges: boolean;
  dependencyChanges: string[];
  aiTags: string[];
  createdAt: string;
}

interface RiskData {
  repo: string;
  risk: number;
  activity: number;
  dependencies: number;
  cves: number;
  lastCommit: string;
}

const GitHubInsights: React.FC = () => {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [pullRequests, setPullRequests] = useState<PullRequest[]>([]);

  const [searchTerm, setSearchTerm] = useState('');
  const [filterTeam, setFilterTeam] = useState('all');
  const [filterLanguage, setFilterLanguage] = useState('all');
  const [filterRisk, setFilterRisk] = useState('all');
  const [aiQuery, setAiQuery] = useState('');
  const [aiResponse, setAiResponse] = useState('');

  const [selectedPR, setSelectedPR] = useState<PullRequest | null>(null);
  const [showPRModal, setShowPRModal] = useState(false);

  // Mock data for repositories
  const mockRepositories: Repository[] = [
    {
      id: '1',
      name: 'ecommerce-api',
      owner: 'company',
      language: 'TypeScript',
      dependencyCount: 156,
      cveCount: 3,
      riskScore: 78,
      lastScanned: '2025-01-15T10:30:00Z',
      lastCommit: '2025-01-15T09:15:00Z',
      team: 'Backend',
      isActive: true,
      prCount: 5,
      outdatedDeps: 12
    },
    {
      id: '2',
      name: 'mobile-app',
      owner: 'company',
      language: 'Swift',
      dependencyCount: 89,
      cveCount: 1,
      riskScore: 45,
      lastScanned: '2025-01-14T16:45:00Z',
      lastCommit: '2025-01-14T14:20:00Z',
      team: 'Mobile',
      isActive: true,
      prCount: 3,
      outdatedDeps: 8
    },
    {
      id: '3',
      name: 'admin-dashboard',
      owner: 'company',
      language: 'React',
      dependencyCount: 234,
      cveCount: 7,
      riskScore: 92,
      lastScanned: '2025-01-15T08:20:00Z',
      lastCommit: '2025-01-15T07:30:00Z',
      team: 'Frontend',
      isActive: true,
      prCount: 8,
      outdatedDeps: 23
    },
    {
      id: '4',
      name: 'data-pipeline',
      owner: 'company',
      language: 'Python',
      dependencyCount: 67,
      cveCount: 2,
      riskScore: 34,
      lastScanned: '2025-01-13T12:10:00Z',
      lastCommit: '2025-01-13T11:45:00Z',
      team: 'Data',
      isActive: false,
      prCount: 1,
      outdatedDeps: 5
    },
    {
      id: '5',
      name: 'auth-service',
      owner: 'company',
      language: 'Go',
      dependencyCount: 45,
      cveCount: 0,
      riskScore: 12,
      lastScanned: '2025-01-15T11:00:00Z',
      lastCommit: '2025-01-15T10:30:00Z',
      team: 'Backend',
      isActive: true,
      prCount: 2,
      outdatedDeps: 3
    }
  ];

  // Mock data for pull requests
  const mockPullRequests: PullRequest[] = [
    {
      id: '1',
      title: 'Update log4j to 2.17.1 to fix CVE-2021-44228',
      repo: 'ecommerce-api',
      author: 'alice.wang',
      status: 'open',
      riskLevel: 'critical',
      sbomChanges: true,
      dependencyChanges: ['log4j:2.14.1 → 2.17.1'],
      aiTags: ['needs-security-review', 'critical-update'],
      createdAt: '2025-01-15T09:00:00Z'
    },
    {
      id: '2',
      title: 'Add new analytics library',
      repo: 'admin-dashboard',
      author: 'bob.smith',
      status: 'open',
      riskLevel: 'medium',
      sbomChanges: true,
      dependencyChanges: ['analytics-lib:1.0.0'],
      aiTags: ['safe-to-merge'],
      createdAt: '2025-01-15T08:30:00Z'
    },
    {
      id: '3',
      title: 'Upgrade axios to latest version',
      repo: 'mobile-app',
      author: 'charlie.brown',
      status: 'open',
      riskLevel: 'low',
      sbomChanges: true,
      dependencyChanges: ['axios:1.4.0 → 1.6.0'],
      aiTags: ['safe-to-merge'],
      createdAt: '2025-01-15T07:45:00Z'
    }
  ];

  // Mock risk data for heatmap
  const riskData: RiskData[] = mockRepositories.map(repo => ({
    repo: repo.name,
    risk: repo.riskScore,
    activity: repo.isActive ? 85 : 20,
    dependencies: repo.dependencyCount,
    cves: repo.cveCount,
    lastCommit: repo.lastCommit
  }));

  // Mock data for charts
  const cveTrendData = [
    { date: '2025-01-10', critical: 2, high: 5, medium: 8, low: 12 },
    { date: '2025-01-11', critical: 1, high: 6, medium: 7, low: 15 },
    { date: '2025-01-12', critical: 3, high: 4, medium: 9, low: 11 },
    { date: '2025-01-13', critical: 2, high: 7, medium: 6, low: 14 },
    { date: '2025-01-14', critical: 1, high: 5, medium: 8, low: 13 },
    { date: '2025-01-15', critical: 2, high: 6, medium: 7, low: 12 }
  ];

  const languageData = [
    { name: 'TypeScript', value: 35, color: '#3178C6' },
    { name: 'React', value: 25, color: '#61DAFB' },
    { name: 'Python', value: 20, color: '#3776AB' },
    { name: 'Go', value: 15, color: '#00ADD8' },
    { name: 'Swift', value: 5, color: '#FA7343' }
  ];

  useEffect(() => {
    setRepositories(mockRepositories);
    setPullRequests(mockPullRequests);
  }, []);

  // Calculate overview stats
  const totalRepos = repositories.length;
  const openPRs = pullRequests.filter(pr => pr.status === 'open').length;
  const reposWithCVEs = repositories.filter(repo => repo.cveCount > 0).length;
  const outdatedDeps = repositories.reduce((sum, repo) => sum + repo.outdatedDeps, 0);
  const avgRiskScore = Math.round(repositories.reduce((sum, repo) => sum + repo.riskScore, 0) / repositories.length);

  // Filter repositories based on search and filters
  const filteredRepositories = repositories.filter(repo => {
    const matchesSearch = repo.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         repo.owner.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesTeam = filterTeam === 'all' || repo.team === filterTeam;
    const matchesLanguage = filterLanguage === 'all' || repo.language === filterLanguage;
    const matchesRisk = filterRisk === 'all' || 
                       (filterRisk === 'low' && repo.riskScore < 30) ||
                       (filterRisk === 'medium' && repo.riskScore >= 30 && repo.riskScore < 70) ||
                       (filterRisk === 'high' && repo.riskScore >= 70);

    return matchesSearch && matchesTeam && matchesLanguage && matchesRisk;
  });

  // Get unique teams and languages for filters
  const teams = [...new Set(repositories.map(repo => repo.team))];
  const languages = [...new Set(repositories.map(repo => repo.language))];

  // Handle AI query
  const handleAiQuery = () => {
    if (aiQuery.trim()) {
      // Mock AI response
      const responses = [
        `Found ${reposWithCVEs} repositories with critical CVEs in the last 30 days. The highest risk repos are: ${repositories.filter(r => r.cveCount > 0).slice(0, 3).map(r => r.name).join(', ')}`,
        `Based on activity and risk analysis, I recommend prioritizing: ${repositories.sort((a, b) => b.riskScore - a.riskScore).slice(0, 2).map(r => r.name).join(', ')}`,
        `Found ${pullRequests.filter(pr => pr.riskLevel === 'high' || pr.riskLevel === 'critical').length} PRs with high-risk dependency changes in the last week.`
      ];
      setAiResponse(responses[Math.floor(Math.random() * responses.length)]);
    }
  };

  // Handle PR details view
  const handlePRDetails = (pr: PullRequest) => {
    setSelectedPR(pr);
    setShowPRModal(true);
  };

  // Close PR modal
  const closePRModal = () => {
    setShowPRModal(false);
    setSelectedPR(null);
  };

  // Get risk color
  const getRiskColor = (score: number) => {
    if (score < 30) return 'text-green-600 bg-green-100';
    if (score < 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  // Get risk level color
  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="w-full h-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
                    <div className="px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <PageHeader
          title="GitHub Insights"
          description="AI-powered repository monitoring and risk analysis"
          icon={
            <svg className="w-6 h-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
            </svg>
          }
          actions={
            <div className="flex items-center space-x-4">
              <button className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors duration-200 flex items-center space-x-2">
                <span>➕</span>
                <span>Connect Repository</span>
              </button>
              <button className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold transition-colors duration-200 flex items-center space-x-2">
                <span>🔄</span>
                <span>Sync Now</span>
              </button>
            </div>
          }
        />

        {/* Repository Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl">📁</span>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Repos</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{totalRepos}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-orange-500 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl">⏳</span>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Open PRs</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{openPRs}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-red-500 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl">🐛</span>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Repos with CVEs</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{reposWithCVEs}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-yellow-500 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl">🔄</span>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Outdated Deps</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{outdatedDeps}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl">🧠</span>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">AI Risk Score</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{avgRiskScore}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* AI Risk Dashboard */}
          <div className="lg:col-span-2">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">🧠 AI-Powered Repo Risk Dashboard</h2>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-green-600 dark:text-green-400 font-medium">Live</span>
                </div>
              </div>

              {/* Risk Heatmap */}
              <div className="grid grid-cols-5 gap-4 mb-6">
                {riskData.map((data, index) => (
                  <div
                    key={index}
                    className="relative p-4 rounded-xl border cursor-pointer hover:shadow-lg transition-all duration-200"
                    style={{
                      backgroundColor: data.risk > 70 ? '#FEE2E2' : data.risk > 30 ? '#FEF3C7' : '#D1FAE5',
                      borderColor: data.risk > 70 ? '#FCA5A5' : data.risk > 30 ? '#FCD34D' : '#A7F3D0'
                    }}

                  >
                    <div className="text-center">
                      <p className="text-sm font-semibold text-gray-900 mb-1">{data.repo}</p>
                      <p className="text-lg font-bold" style={{ color: data.risk > 70 ? '#DC2626' : data.risk > 30 ? '#D97706' : '#059669' }}>
                        {data.risk}
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">
                        {data.dependencies} deps • {data.cves} CVEs
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Filters */}
              <div className="flex flex-wrap gap-4">
                <select
                  value={filterTeam}
                  onChange={(e) => setFilterTeam(e.target.value)}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="all">All Teams</option>
                  {teams.map(team => (
                    <option key={team} value={team}>{team}</option>
                  ))}
                </select>

                <select
                  value={filterLanguage}
                  onChange={(e) => setFilterLanguage(e.target.value)}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="all">All Languages</option>
                  {languages.map(lang => (
                    <option key={lang} value={lang}>{lang}</option>
                  ))}
                </select>

                <select
                  value={filterRisk}
                  onChange={(e) => setFilterRisk(e.target.value)}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="all">All Risk Levels</option>
                  <option value="low">Low Risk</option>
                  <option value="medium">Medium Risk</option>
                  <option value="high">High Risk</option>
                </select>
              </div>
            </div>
          </div>

          {/* AI Assistant Panel */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                🤖 AI Assistant
                <span className="ml-2 text-xs bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 px-2 py-1 rounded-full">BETA</span>
              </h3>

              <div className="space-y-4">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={aiQuery}
                    onChange={(e) => setAiQuery(e.target.value)}
                    placeholder="Ask GitHubBot..."
                    className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                    onKeyPress={(e) => e.key === 'Enter' && handleAiQuery()}
                  />
                  <button
                    onClick={handleAiQuery}
                    className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors duration-200"
                  >
                    Ask
                  </button>
                </div>

                {aiResponse && (
                  <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
                    <p className="text-sm text-purple-800 dark:text-purple-200">{aiResponse}</p>
                  </div>
                )}

                <div className="space-y-2">
                  <p className="text-xs font-medium text-gray-600 dark:text-gray-400">Quick Actions:</p>
                  <button className="w-full text-left px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors duration-200">
                    Show repos with critical CVEs
                  </button>
                  <button className="w-full text-left px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors duration-200">
                    Prioritize repos by risk
                  </button>
                  <button className="w-full text-left px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors duration-200">
                    Find high-risk PRs
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Repository Table */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">🗃️ Repository Table</h2>
            <div className="flex items-center space-x-4">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search repositories..."
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
              <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200">
                📥 Export
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Repository</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Owner</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Language</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Dependencies</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">CVEs</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Risk Score</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Last Scanned</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredRepositories.map((repo) => (
                  <tr key={repo.id} className="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">📁</span>
                        <span className="font-medium text-gray-900 dark:text-white">{repo.name}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-gray-600 dark:text-gray-300">{repo.owner}</td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-300 rounded-full text-xs font-medium">
                        {repo.language}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-gray-600 dark:text-gray-300">{repo.dependencyCount}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${repo.cveCount > 0 ? 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300' : 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300'}`}>
                        {repo.cveCount}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(repo.riskScore)}`}>
                        {repo.riskScore}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-gray-600 dark:text-gray-300">
                      {new Date(repo.lastScanned).toLocaleDateString()}
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-2">
                        <button className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 text-sm font-medium">
                          View
                        </button>
                        <button className="text-green-600 dark:text-green-400 hover:text-green-800 dark:hover:text-green-300 text-sm font-medium">
                          Re-scan
                        </button>
                        <button className="text-purple-600 dark:text-purple-400 hover:text-purple-800 dark:hover:text-purple-300 text-sm font-medium">
                          SBOM Diff
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Pull Request Analyzer */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">🔄 Pull Request Analyzer</h2>
          
          <div className="space-y-4">
            {pullRequests.map((pr) => (
              <div key={pr.id} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md transition-shadow duration-200">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="font-semibold text-gray-900 dark:text-white">{pr.title}</h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getRiskLevelColor(pr.riskLevel)}`}>
                        {pr.riskLevel.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                      {pr.repo} • {pr.author} • {new Date(pr.createdAt).toLocaleDateString()}
                    </p>
                    <div className="flex items-center space-x-4">
                      {pr.sbomChanges && (
                        <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-300 rounded-full text-xs font-medium">
                          SBOM Changes
                        </span>
                      )}
                      {pr.dependencyChanges.map((change, index) => (
                        <span key={index} className="px-2 py-1 bg-yellow-100 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-300 rounded-full text-xs font-medium">
                          {change}
                        </span>
                      ))}
                    </div>
                    <div className="flex items-center space-x-2 mt-2">
                      {pr.aiTags.map((tag, index) => (
                        <span key={index} className="px-2 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-800 dark:text-purple-300 rounded-full text-xs font-medium">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button 
                      onClick={() => handlePRDetails(pr)}
                      className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm font-medium transition-colors duration-200"
                    >
                      View Details
                    </button>
                    <button className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-sm font-medium transition-colors duration-200">
                      Approve
                    </button>
                    <button className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white rounded text-sm font-medium transition-colors duration-200">
                      Block
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* CVE Trend Chart */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">📊 CVE Trend Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={cveTrendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="critical" stroke="#DC2626" strokeWidth={2} />
                <Line type="monotone" dataKey="high" stroke="#EA580C" strokeWidth={2} />
                <Line type="monotone" dataKey="medium" stroke="#D97706" strokeWidth={2} />
                <Line type="monotone" dataKey="low" stroke="#059669" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Language Distribution */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">📈 Language Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={languageData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {languageData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pull Request Details Modal */}
        {showPRModal && selectedPR && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                {/* Modal Header */}
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center">
                      <span className="text-white text-xl">🔄</span>
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                        Pull Request Analysis
                      </h2>
                      <p className="text-sm text-gray-600 dark:text-gray-300">
                        #{selectedPR.id} • {selectedPR.repo}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={closePRModal}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                {/* PR Basic Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">📋 Basic Information</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Title:</span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">{selectedPR.title}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Repository:</span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">{selectedPR.repo}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Author:</span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">{selectedPR.author}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Created:</span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          {new Date(selectedPR.createdAt).toLocaleString()}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Status:</span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          selectedPR.status === 'open' ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300' :
                          selectedPR.status === 'merged' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-300' :
                          'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-300'
                        }`}>
                          {selectedPR.status.toUpperCase()}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">⚠️ Security Analysis</h3>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Risk Level:</span>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getRiskLevelColor(selectedPR.riskLevel)}`}>
                          {selectedPR.riskLevel.toUpperCase()}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600 dark:text-gray-400">SBOM Changes:</span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          selectedPR.sbomChanges ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-300' : 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-300'
                        }`}>
                          {selectedPR.sbomChanges ? 'YES' : 'NO'}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Dependency Changes:</span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          {selectedPR.dependencyChanges.length}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600 dark:text-gray-400">AI Tags:</span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          {selectedPR.aiTags.length}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Dependency Changes */}
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">🔧 Dependency Changes</h3>
                  <div className="space-y-3">
                    {selectedPR.dependencyChanges.map((change, index) => (
                      <div key={index} className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="text-yellow-600 dark:text-yellow-400">📦</span>
                          <span className="font-medium text-yellow-800 dark:text-yellow-300">Package Update</span>
                        </div>
                        <p className="text-sm text-yellow-700 dark:text-yellow-200 font-mono">{change}</p>
                        <div className="mt-2 flex items-center space-x-4 text-xs text-yellow-600 dark:text-yellow-400">
                          <span>• Security impact: Medium</span>
                          <span>• Breaking changes: None detected</span>
                          <span>• Compatibility: ✅ Verified</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* AI Analysis */}
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">🧠 AI Analysis & Recommendations</h3>
                  <div className="space-y-4">
                    <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
                      <div className="flex items-start space-x-2 mb-2">
                        <span className="text-purple-600 dark:text-purple-400 text-lg">💡</span>
                        <div>
                          <p className="text-sm font-semibold text-purple-800 dark:text-purple-300 mb-1">AI Assessment</p>
                          <p className="text-sm text-purple-700 dark:text-purple-200">
                            {selectedPR.riskLevel === 'critical' ? 
                              'This PR addresses a critical security vulnerability. Immediate review and approval recommended.' :
                              selectedPR.riskLevel === 'high' ?
                              'This PR contains high-risk changes that require careful security review before merging.' :
                              selectedPR.riskLevel === 'medium' ?
                              'This PR has moderate security implications. Standard review process recommended.' :
                              'This PR appears to be low-risk with minimal security impact.'
                            }
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                      <div className="flex items-start space-x-2 mb-2">
                        <span className="text-blue-600 dark:text-blue-400 text-lg">🔍</span>
                        <div>
                          <p className="text-sm font-semibold text-blue-800 dark:text-blue-300 mb-1">Security Scan Results</p>
                          <div className="space-y-1 text-sm text-blue-700 dark:text-blue-200">
                            <p>• CVE Analysis: {selectedPR.riskLevel === 'critical' ? 'Critical vulnerabilities detected' : 'No critical vulnerabilities found'}</p>
                            <p>• License Compliance: ✅ All dependencies have compatible licenses</p>
                            <p>• Dependency Graph: ✅ No circular dependencies detected</p>
                            <p>• Version Compatibility: ✅ All versions are compatible</p>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                      <div className="flex items-start space-x-2 mb-2">
                        <span className="text-green-600 dark:text-green-400 text-lg">✅</span>
                        <div>
                          <p className="text-sm font-semibold text-green-800 dark:text-green-300 mb-1">Recommended Actions</p>
                          <div className="space-y-1 text-sm text-green-700 dark:text-green-200">
                            {selectedPR.riskLevel === 'critical' ? (
                              <>
                                <p>• 🚨 Immediate review by security team</p>
                                <p>• 🔒 Test in staging environment</p>
                                <p>• 📋 Document security implications</p>
                                <p>• ⏰ Deploy within 24 hours</p>
                              </>
                            ) : selectedPR.riskLevel === 'high' ? (
                              <>
                                <p>• 🔍 Security review required</p>
                                <p>• 🧪 Run security tests</p>
                                <p>• 📝 Update documentation</p>
                                <p>• ⏳ Deploy within 48 hours</p>
                              </>
                            ) : (
                              <>
                                <p>• ✅ Standard review process</p>
                                <p>• 🧪 Run automated tests</p>
                                <p>• 📋 Update changelog</p>
                                <p>• 🚀 Deploy when ready</p>
                              </>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* AI Tags */}
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">🏷️ AI Tags & Classification</h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedPR.aiTags.map((tag, index) => (
                      <span key={index} className="px-3 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-800 dark:text-purple-300 rounded-full text-xs font-medium border border-purple-200 dark:border-purple-800">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
                  <div className="flex items-center space-x-4">
                    <button className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors duration-200">
                      ✅ Approve PR
                    </button>
                    <button className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors duration-200">
                      ❌ Block PR
                    </button>
                    <button className="px-6 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg font-medium transition-colors duration-200">
                      ⏸️ Request Changes
                    </button>
                  </div>
                  <div className="flex items-center space-x-4">
                    <button className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors duration-200">
                      📊 Generate Report
                    </button>
                    <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200">
                      🔗 View on GitHub
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GitHubInsights; 