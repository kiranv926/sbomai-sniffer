import axios, { type AxiosInstance, type AxiosResponse, type AxiosError } from 'axios';
import { API_CONFIG, getAuthHeaders, ApiError, type ApiResponse } from './config';

class ApiClient {
  private client: AxiosInstance;
  private retryCount = 0;

  constructor() {
    this.client = axios.create({
      baseURL: API_CONFIG.BASE_URL,
      timeout: API_CONFIG.TIMEOUT,
      headers: getAuthHeaders(),
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth headers to every request
        const headers = getAuthHeaders();
        if (config.headers) {
          Object.assign(config.headers, headers);
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        this.retryCount = 0; // Reset retry count on success
        return response;
      },
      async (error: AxiosError) => {
        return this.handleError(error);
      }
    );
  }

  private async handleError(error: AxiosError): Promise<never> {
    const { response, request } = error;

    if (response) {
      // Server responded with error status
      const errorData = response.data as any;
      throw new ApiError(
        response.status,
        errorData?.message || 'Server error',
        errorData?.code
      );
    } else if (request) {
      // Request was made but no response received
      if (this.retryCount < API_CONFIG.MAX_RETRIES) {
        this.retryCount++;
        await this.delay(API_CONFIG.RETRY_DELAY * this.retryCount);
        return this.client.request(request);
      }
      throw new ApiError(0, 'Network error - no response received');
    } else {
      // Something else happened
      throw new ApiError(0, 'Request configuration error');
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Generic HTTP methods
  async get<T>(url: string, params?: any): Promise<ApiResponse<T>> {
    const response = await this.client.get(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: any): Promise<ApiResponse<T>> {
    const response = await this.client.post(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: any): Promise<ApiResponse<T>> {
    const response = await this.client.put(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<ApiResponse<T>> {
    const response = await this.client.delete(url);
    return response.data;
  }

  async patch<T>(url: string, data?: any): Promise<ApiResponse<T>> {
    const response = await this.client.patch(url, data);
    return response.data;
  }

  // File upload
  async upload<T>(url: string, file: File, onProgress?: (progress: number) => void): Promise<ApiResponse<T>> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.client.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(progress);
        }
      },
    });

    return response.data;
  }
}

// Export singleton instance
export const apiClient = new ApiClient();
export default apiClient; 