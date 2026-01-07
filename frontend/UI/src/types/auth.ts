export interface Role {
  id: number;
  name: 'Admin' | 'Analyst' | 'Partner';
  hierarchy_level: number;
  permissions: string[];
}

export interface User {
  id: number;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  role: Role | null;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

