// API Configuration
export const API_CONFIG = {
  // Base URLs for different services
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8081/api/v1',
  PARSER_URL: import.meta.env.VITE_PARSER_URL || 'http://localhost:8081/api/v1',
  ANALYSIS_URL: import.meta.env.VITE_ANALYSIS_URL || 'http://localhost:8081/api/v1',
  AI_URL: import.meta.env.VITE_AI_URL || 'http://localhost:8081/api/v1/ai',
  
  // Timeouts
  TIMEOUT: 30000,
  
  // Retry configuration
  MAX_RETRIES: 3,
  RETRY_DELAY: 1000,
};

// Common headers
export const getAuthHeaders = () => {
  const token = localStorage.getItem('auth_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : '',
  };
};

// API response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
  timestamp: string;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    size: number;
    total: number;
    totalPages: number;
  };
}

// Error handling
export class ApiError extends Error {
  status: number;
  code?: string;

  constructor(status: number, message: string, code?: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }
} 