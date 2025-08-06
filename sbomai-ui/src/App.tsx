
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './layout/Layout';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Vulnerabilities from './pages/Vulnerabilities';
import AIRepositoryAnalysis from './pages/AIRepositoryAnalysis';
import LiveFeed from './pages/LiveFeed';
import PolicyEngine from './pages/PolicyEngine';

import WebScan from './pages/WebScan';
import Integrations from './pages/Integrations';
import ModelConfiguration from './pages/ModelConfiguration';
import BreadcrumbDemo from './pages/BreadcrumbDemo';
import AIAssist from './pages/AIAssist';
import Administration from './pages/Administration';
import Projects from './pages/Projects';
import SecurityInsights from './pages/SecurityInsights';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
                        <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/vulnerabilities" element={<Vulnerabilities />} />
                      <Route path="/ai-repository-analysis" element={<AIRepositoryAnalysis />} />
                  <Route path="/ai-assist" element={<AIAssist />} />
            <Route path="/live-feed" element={<LiveFeed />} />
                              <Route path="/policy-engine" element={<PolicyEngine />} />
                  <Route path="/web-scan" element={<WebScan />} />
                                   <Route path="/integrations" element={<Integrations />} />
                                     <Route path="/model-configuration" element={<ModelConfiguration />} />
                    <Route path="/breadcrumb-demo" element={<BreadcrumbDemo />} />
                            <Route path="/administration" element={<Administration />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/security-insights" element={<SecurityInsights />} />
          {/* Add more routes as needed */}
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
