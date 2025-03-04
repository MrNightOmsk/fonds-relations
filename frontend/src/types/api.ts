// Общие типы
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Типы для пользователей
export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  fund_id: string;
  is_active: boolean;
  created_at: string;
}

export interface UserCreate {
  email: string;
  password: string;
  full_name: string;
  role: string;
  fund_id: string;
}

export interface UserUpdate {
  email?: string;
  full_name?: string;
  password?: string;
  role?: string;
  is_active?: boolean;
}

// Типы для фондов
export interface Fund {
  id: string;
  name: string;
  description?: string;
  contact_info?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface FundCreate {
  name: string;
  description?: string;
  contact_info?: Record<string, any>;
}

export interface FundUpdate {
  name?: string;
  description?: string;
  contact_info?: Record<string, any>;
}

// Типы для игроков
export interface Player {
  id: string;
  full_name: string;
  birth_date?: string;
  contact_info?: Record<string, any>;
  additional_info?: Record<string, any>;
  created_by_user_id: string;
  created_by_fund_id: string;
  created_at: string;
  updated_at: string;
}

export interface PlayerCreate {
  full_name: string;
  birth_date?: string;
  contact_info?: Record<string, any>;
  additional_info?: Record<string, any>;
}

export interface PlayerUpdate {
  full_name?: string;
  birth_date?: string;
  contact_info?: Record<string, any>;
  additional_info?: Record<string, any>;
}

// Типы для кейсов
export interface Case {
  id: string;
  player_id: string;
  title: string;
  description?: string;
  status: string;
  created_by_user_id: string;
  created_by_fund_id: string;
  closed_at?: string;
  closed_by_user_id?: string;
  created_at: string;
  updated_at: string;
}

export interface CaseCreate {
  player_id: string;
  title: string;
  description?: string;
  status: string;
}

export interface CaseUpdate {
  title?: string;
  description?: string;
  status?: string;
}

// Типы для доказательств
export interface CaseEvidence {
  id: string;
  case_id: string;
  type: string;
  file_path: string;
  uploaded_by_id: string;
  created_at: string;
}

export interface CaseEvidenceCreate {
  case_id: string;
  type: string;
  description: string;
  file: File;
} 