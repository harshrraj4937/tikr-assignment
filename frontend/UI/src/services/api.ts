import axios from 'axios';
import type { LoginRequest, LoginResponse, User } from '../types/auth';
import type { Deal, DealCreate, DealUpdate, DealStageUpdate, Activity } from '../types/deals';

// Create axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API functions
export const authAPI = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/api/auth/login', credentials);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/api/auth/me');
    return response.data;
  },
};

// Deals API functions
export const dealsAPI = {
  listDeals: async (): Promise<Deal[]> => {
    const response = await api.get<Deal[]>('/api/deals');
    return response.data;
  },

  getDeal: async (dealId: number): Promise<Deal> => {
    const response = await api.get<Deal>(`/api/deals/${dealId}`);
    return response.data;
  },

  createDeal: async (dealData: DealCreate): Promise<Deal> => {
    const response = await api.post<Deal>('/api/deals', dealData);
    return response.data;
  },

  updateDeal: async (dealId: number, dealData: DealUpdate): Promise<Deal> => {
    const response = await api.patch<Deal>(`/api/deals/${dealId}`, dealData);
    return response.data;
  },

  updateDealStage: async (dealId: number, stage: string): Promise<Deal> => {
    const stageData: DealStageUpdate = { stage };
    const response = await api.patch<Deal>(`/api/deals/${dealId}/stage`, stageData);
    return response.data;
  },

  archiveDeal: async (dealId: number): Promise<{ message: string }> => {
    const response = await api.delete<{ message: string }>(`/api/deals/${dealId}`);
    return response.data;
  },

  getDealActivities: async (dealId: number): Promise<Activity[]> => {
    const response = await api.get<Activity[]>(`/api/deals/${dealId}/activities`);
    return response.data;
  },
};

export default api;

