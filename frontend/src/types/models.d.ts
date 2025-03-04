// Пользователь
export interface User {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  funds: string[];
  created_at: string;
}

export interface CreateUserRequest {
  username: string;
  email: string;
  password: string;
  is_active?: boolean;
  is_superuser?: boolean;
  funds?: string[];
}

export interface UpdateUserRequest {
  username?: string;
  email?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
  funds?: string[];
}

// Фонд
export interface Fund {
  id: string;
  name: string;
  description?: string;
  location?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateFundRequest {
  name: string;
  description?: string;
  location?: string;
}

export interface UpdateFundRequest {
  name?: string;
  description?: string;
  location?: string;
}

// Кейс
export interface Case {
  id: string;
  title: string;
  description?: string;
  status: CaseStatus;
  created_by_fund_id?: string;
  fund_id: string;
  player_id?: string;
  created_at: string;
  updated_at: string;
}

export type CaseStatus = 'open' | 'in_progress' | 'closed';

export interface CreateCaseRequest {
  title: string;
  description?: string;
  status?: CaseStatus;
  fund_id: string;
  player_id?: string;
}

export interface UpdateCaseRequest {
  title?: string;
  description?: string;
  status?: CaseStatus;
  fund_id?: string;
  player_id?: string;
}

// Алиасы типов для совместимости со старым кодом
export type CaseCreate = CreateCaseRequest;
export type CaseUpdate = UpdateCaseRequest;

// Игрок
export interface Player {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  created_by_fund_id: string;
  created_at: string;
  updated_at: string;
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

// Авторизация
export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

// Общие типы для API
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
} 