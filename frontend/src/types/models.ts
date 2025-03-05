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
  first_name: string;
  last_name: string;
  middle_name?: string;
  full_name: string;
  birth_date?: string;
  contact_info?: Record<string, any>;
  additional_info?: Record<string, any>;
  health_notes?: string;
  created_by_user_id: string;
  created_by_fund_id: string;
  created_at: string;
  updated_at: string;
  nicknames?: PlayerNickname[];
  contacts?: PlayerContact[];
  locations?: PlayerLocation[];
  payment_methods?: PlayerPaymentMethod[];
  social_media?: PlayerSocialMedia[];
  poker_ids?: PlayerPokerId[];
}

export interface PlayerNickname {
  id?: string;
  player_id: string;
  nickname: string;
  room?: string;
  discipline?: string;
  created_at?: string;
  updated_at?: string;
}

export interface PlayerContact {
  id?: string;
  player_id: string;
  type: string;
  value: string;
  description?: string;
  created_at?: string;
  updated_at?: string;
}

export interface PlayerLocation {
  id: string;
  player_id: string;
  country?: string;
  city?: string;
  address?: string;
  created_at: string;
  updated_at: string;
}

export interface PlayerPaymentMethod {
  id: string;
  player_id: string;
  type: string;
  value: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface PlayerSocialMedia {
  id?: string;
  player_id: string;
  type: string;
  platform?: string;
  value: string;
  username?: string;
  description?: string;
  created_at?: string;
  updated_at?: string;
}

export interface PlayerPokerId {
  id: string;
  player_id: string;
  room: string;
  nickname: string;
  description?: string;
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
  first_name: string;
  last_name: string;
  middle_name?: string;
  birth_date?: string;
  health_notes?: string;
  contact_info?: Record<string, any>;
  additional_info?: Record<string, any>;
  nicknames?: Partial<PlayerNickname>[];
  contacts?: Partial<PlayerContact>[];
  locations?: Partial<PlayerLocation>[];
  payment_methods?: Partial<PlayerPaymentMethod>[];
  social_media?: Partial<PlayerSocialMedia>[];
  poker_ids?: Partial<PlayerPokerId>[];
}

export interface UpdatePlayerRequest {
  first_name?: string;
  last_name?: string;
  middle_name?: string;
  full_name?: string;
  birth_date?: string;
  health_notes?: string;
  contact_info?: Record<string, any>;
  additional_info?: Record<string, any>;
  nicknames?: Partial<PlayerNickname>[];
  contacts?: Partial<PlayerContact>[];
  locations?: Partial<PlayerLocation>[];
  payment_methods?: Partial<PlayerPaymentMethod>[];
  social_media?: Partial<PlayerSocialMedia>[];
  poker_ids?: Partial<PlayerPokerId>[];
}

// Типы для кейса
export interface Case {
  id: string;
  title: string;
  description: string;
  status: 'open' | 'closed';
  player_id: string;
  arbitrage_type?: string;
  arbitrage_amount?: number;
  arbitrage_currency?: string;
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
  status: 'open' | 'closed';
  arbitrage_type?: string;
  arbitrage_amount?: number;
  arbitrage_currency?: string;
}

export interface CaseUpdate {
  title?: string;
  description?: string;
  player_id?: string;
  status?: 'open' | 'closed';
  arbitrage_type?: string;
  arbitrage_amount?: number;
  arbitrage_currency?: string;
}

export interface CaseComment {
  id?: string;
  case_id: string;
  comment: string;
  text?: string;
  created_by_id: string;
  created_by?: string;
  created_at?: string;
  updated_at?: string;
}

export interface CaseCommentCreate {
  comment: string;
  case_id: string;
}

export interface CaseEvidence {
  id?: string;
  case_id: string;
  type: string;
  title?: string;
  description?: string;
  file_path: string;
  file_url?: string;
  file_type?: string;
  uploaded_by_id: string;
  created_at?: string;
  updated_at?: string;
}

export interface ApiResponse<T> {
  status: 'success' | 'error';
  data?: T;
  message?: string;
} 