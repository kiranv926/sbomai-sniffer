# SBOM AI UI - Backend Development Requirements

## **API Endpoints & Data Models**

### **1. Authentication & Authorization**

#### **Endpoints:**
```
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
GET /api/auth/profile
PUT /api/auth/profile
POST /api/auth/change-password
```

#### **Data Models:**
```typescript
interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'viewer';
  team: string;
  permissions: string[];
  lastLogin: Date;
  createdAt: Date;
  updatedAt: Date;
}

interface Team {
  id: string;
  name: string;
  description: string;
  members: User[];
  permissions: string[];
  createdAt: Date;
}
```

### **2. Project Management**

#### **Endpoints:**
```
GET /api/projects
POST /api/projects
GET /api/projects/{id}
PUT /api/projects/{id}
DELETE /api/projects/{id}
GET /api/projects/{id}/scans
GET /api/projects/{id}/vulnerabilities
GET /api/projects/{id}/dependencies
```

#### **Data Models:**
```typescript
interface Project {
  id: string;
  name: string;
  description: string;
  team: string;
  language: string;
  repository: {
    url: string;
    type: 'github' | 'gitlab' | 'bitbucket';
    branch: string;
  };
  status: 'active' | 'archived' | 'deprecated';
  riskScore: number;
  lastScan: Date;
  vulnerabilityCount: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  dependencyCount: number;
  outdatedDeps: number;
  createdAt: Date;
  updatedAt: Date;
}
```

### **3. Security Scanning**

#### **Endpoints:**
```
POST /api/scans/network
POST /api/scans/web
POST /api/scans/directory
POST /api/scans/os-detection
POST /api/scans/iot
POST /api/scans/configuration
POST /api/scans/application
GET /api/scans/{id}
GET /api/scans/{id}/results
GET /api/scans/{id}/status
DELETE /api/scans/{id}
```

#### **Data Models:**
```typescript
interface Scan {
  id: string;
  projectId: string;
  type: 'network' | 'web' | 'directory' | 'os' | 'iot' | 'config' | 'app';
  status: 'pending' | 'running' | 'completed' | 'failed';
  configuration: ScanConfig;
  results: ScanResult[];
  startedAt: Date;
  completedAt?: Date;
  error?: string;
}

interface ScanConfig {
  targets: string[];
  options: Record<string, any>;
  credentials?: {
    username: string;
    password: string;
  };
}

interface ScanResult {
  id: string;
  scanId: string;
  type: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  details: Record<string, any>;
  recommendations: string[];
  cveIds?: string[];
  createdAt: Date;
}
```

### **4. AI Analysis Service**

#### **Endpoints:**
```
POST /api/ai/analyze-sbom
POST /api/ai/generate-fix-plan
POST /api/ai/prioritize-vulnerabilities
POST /api/ai/analyze-dependencies
GET /api/ai/analysis/{id}
GET /api/ai/metrics
POST /api/ai/chat
```

#### **Data Models:**
```typescript
interface AIAnalysis {
  id: string;
  projectId: string;
  sbomData: SBOMData;
  vulnerabilities: AIVulnerability[];
  dependencies: AIDependency[];
  fixPlans: FixPlan[];
  metrics: AIMetrics;
  createdAt: Date;
}

interface AIVulnerability {
  id: string;
  cveId: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  component: string;
  affectedVersion: string;
  fixedVersion?: string;
  aiSuggestion: string;
  confidence: number;
  priority: number;
  status: 'open' | 'fixed' | 'ignored';
}

interface AIDependency {
  name: string;
  currentVersion: string;
  recommendedVersion?: string;
  usageTrend: 'trending_up' | 'trending_down' | 'stable';
  riskScore: number;
  riskLevel: 'high' | 'medium' | 'low';
  fixAction: 'patch' | 'upgrade' | 'replace' | 'ignore';
  replacement?: string;
  aiInsights: string[];
}

interface FixPlan {
  id: string;
  sbomId: string;
  actions: FixAction[];
  estimatedTime: string;
  riskLevel: 'low' | 'medium' | 'high';
  priority: number;
  status: 'pending' | 'in-progress' | 'completed';
}

interface FixAction {
  type: 'upgrade' | 'remove' | 'replace' | 'add' | 'patch';
  package: string;
  description: string;
  currentVersion?: string;
  targetVersion?: string;
  replacement?: string;
  estimatedTime: string;
}

interface AIMetrics {
  accuracy: number;
  responseTime: number;
  patternsDetected: number;
  confidenceScore: number;
  processedSboms: number;
  suggestionsGenerated: number;
}
```

### **5. Vulnerability Management**

#### **Endpoints:**
```
GET /api/vulnerabilities
GET /api/vulnerabilities/{id}
PUT /api/vulnerabilities/{id}
POST /api/vulnerabilities/{id}/status
GET /api/vulnerabilities/cve/{cveId}
GET /api/vulnerabilities/search
```

#### **Data Models:**
```typescript
interface Vulnerability {
  id: string;
  cveId: string;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  cvssScore: number;
  affectedComponents: string[];
  references: string[];
  status: 'open' | 'fixed' | 'ignored' | 'false-positive';
  assignedTo?: string;
  dueDate?: Date;
  createdAt: Date;
  updatedAt: Date;
}
```

### **6. Repository Integration**

#### **Endpoints:**
```
GET /api/repositories
POST /api/repositories/connect
GET /api/repositories/{id}
GET /api/repositories/{id}/pull-requests
GET /api/repositories/{id}/commits
POST /api/repositories/{id}/webhook
```

#### **Data Models:**
```typescript
interface Repository {
  id: string;
  name: string;
  owner: string;
  url: string;
  type: 'github' | 'gitlab' | 'bitbucket';
  language: string;
  dependencyCount: number;
  cveCount: number;
  riskScore: number;
  lastScanned: Date;
  lastCommit: Date;
  team: string;
  isActive: boolean;
  prCount: number;
  outdatedDeps: number;
  webhookUrl?: string;
  accessToken?: string;
}

interface PullRequest {
  id: string;
  repositoryId: string;
  title: string;
  author: string;
  status: 'open' | 'merged' | 'closed';
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
  sbomChanges: boolean;
  dependencyChanges: string[];
  aiTags: string[];
  createdAt: Date;
  updatedAt: Date;
}
```

### **7. Policy Engine**

#### **Endpoints:**
```
GET /api/policies
POST /api/policies
GET /api/policies/{id}
PUT /api/policies/{id}
DELETE /api/policies/{id}
POST /api/policies/{id}/evaluate
GET /api/policies/compliance
```

#### **Data Models:**
```typescript
interface Policy {
  id: string;
  name: string;
  description: string;
  type: 'security' | 'compliance' | 'quality';
  rules: PolicyRule[];
  status: 'active' | 'inactive' | 'draft';
  priority: number;
  createdAt: Date;
  updatedAt: Date;
}

interface PolicyRule {
  id: string;
  condition: string;
  action: 'block' | 'warn' | 'allow';
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;
}

interface ComplianceReport {
  id: string;
  projectId: string;
  policyId: string;
  status: 'compliant' | 'non-compliant' | 'partial';
  violations: PolicyViolation[];
  score: number;
  createdAt: Date;
}
```

### **8. Integration Management**

#### **Endpoints:**
```
GET /api/integrations
POST /api/integrations
GET /api/integrations/{id}
PUT /api/integrations/{id}
DELETE /api/integrations/{id}
POST /api/integrations/{id}/test
GET /api/integrations/{id}/status
```

#### **Data Models:**
```typescript
interface Integration {
  id: string;
  name: string;
  type: 'vulnerability-scanner' | 'ci-cd' | 'monitoring' | 'notification';
  provider: string;
  configuration: Record<string, any>;
  credentials: {
    apiKey?: string;
    username?: string;
    password?: string;
    url?: string;
  };
  status: 'active' | 'inactive' | 'error';
  lastSync: Date;
  createdAt: Date;
  updatedAt: Date;
}
```

### **9. Real-time Events & Notifications**

#### **Endpoints:**
```
GET /api/events
POST /api/events
GET /api/events/stream
GET /api/notifications
POST /api/notifications
PUT /api/notifications/{id}/read
```

#### **Data Models:**
```typescript
interface Event {
  id: string;
  type: 'scan-completed' | 'vulnerability-detected' | 'policy-violation' | 'integration-error';
  severity: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  metadata: Record<string, any>;
  projectId?: string;
  userId?: string;
  createdAt: Date;
}

interface Notification {
  id: string;
  userId: string;
  type: 'email' | 'slack' | 'webhook' | 'in-app';
  title: string;
  message: string;
  read: boolean;
  metadata: Record<string, any>;
  createdAt: Date;
}
```

### **10. AI Chat Assistant**

#### **Endpoints:**
```
POST /api/ai/chat/message
GET /api/ai/chat/history
POST /api/ai/chat/context
```

#### **Data Models:**
```typescript
interface ChatMessage {
  id: string;
  userId: string;
  type: 'user' | 'bot';
  content: string;
  context?: {
    projectId?: string;
    vulnerabilityId?: string;
    scanId?: string;
  };
  timestamp: Date;
}

interface ChatSession {
  id: string;
  userId: string;
  messages: ChatMessage[];
  context: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}
```

## **Database Schema Recommendations**

### **Primary Tables:**
- `users`, `teams`, `projects`
- `scans`, `scan_results`, `vulnerabilities`
- `ai_analyses`, `ai_vulnerabilities`, `ai_dependencies`, `fix_plans`
- `repositories`, `pull_requests`
- `policies`, `policy_rules`, `compliance_reports`
- `integrations`, `events`, `notifications`
- `chat_sessions`, `chat_messages`

### **Indexing Strategy:**
- Primary keys on all tables
- Foreign key indexes for relationships
- Composite indexes for common queries
- Full-text search on vulnerability descriptions
- Time-based indexes for events and scans

## **Security Requirements**

### **Authentication:**
- JWT-based authentication
- Role-based access control (RBAC)
- API key management for integrations
- OAuth2 for repository connections

### **Data Protection:**
- Encryption at rest for sensitive data
- TLS for all API communications
- Input validation and sanitization
- Rate limiting and DDoS protection
- Audit logging for all operations

## **Performance Requirements**

### **Response Times:**
- API endpoints: < 200ms for simple operations
- Scan operations: Async with status polling
- AI analysis: < 30 seconds for standard analysis
- Real-time events: < 100ms latency

### **Scalability:**
- Horizontal scaling support
- Database connection pooling
- Caching layer (Redis)
- Message queue for async operations
- CDN for static assets

## **Monitoring & Observability**

### **Metrics:**
- API response times and error rates
- Database query performance
- AI model accuracy and response times
- Scan completion rates and durations
- User activity and engagement

### **Logging:**
- Structured logging (JSON)
- Log aggregation and analysis
- Error tracking and alerting
- Performance monitoring
- Security event logging

This comprehensive specification should provide all the details needed for backend development, including specific data models, API endpoints, security requirements, and performance considerations. 