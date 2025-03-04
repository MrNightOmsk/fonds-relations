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

export interface Player {
  id: string;
  name: string;
  email: string | null;
  phone: string | null;
  created_by_fund_id: string;
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

export interface CreatePlayerRequest {
  name: string;
  email?: string;
  phone?: string;
}

export interface UpdatePlayerRequest {
  name?: string;
  email?: string;
  phone?: string;
}

// Типы для кейса
export interface Case {
  id: string;
  title: string;
  description: string;
  status: string;
  player_id: string;
  created_by_fund_id: string;
  created_by_user_id?: string;
  created_at: string;
  updated_at?: string;
  closed_at?: string;
  closed_by_user_id?: string;
}

export interface CaseCreate {
  title: string;
  description: string;
  player_id: string;
  status: string;
}

export interface CaseUpdate {
  title?: string;
  description?: string;
  player_id?: string;
  status?: string;
}

export interface ApiResponse<T> {
  status: 'success' | 'error';
  data?: T;
  message?: string;
} 