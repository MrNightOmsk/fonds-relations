export interface User {
  id: string;
  email: string;
  full_name: string;
  fund_id: string;
  fund?: Fund;
  role: 'admin' | 'manager';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Fund {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateUserRequest {
  email: string;
  password: string;
  full_name: string;
  fund_id: string;
  role: 'admin' | 'manager';
  is_active: boolean;
}

export interface UpdateUserRequest {
  email?: string;
  password?: string;
  full_name?: string;
  fund_id?: string;
  role?: 'admin' | 'manager';
  is_active?: boolean;
}

export interface CreateFundRequest {
  name: string;
  description?: string;
}

export interface UpdateFundRequest {
  name?: string;
  description?: string;
}

export interface ApiResponse<T> {
  status: 'success' | 'error';
  data?: T;
  message?: string;
} 