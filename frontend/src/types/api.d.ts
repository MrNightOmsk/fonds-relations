/* Объявления типов для API взаимодействия */

// Типы для аутентификации
interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface LoginCredentials {
  username: string;
  password: string;
}

// Типы для пользователя
interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  fund_id?: string;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
}

// Типы для фонда
interface Fund {
  id: string;
  name: string;
  description?: string;
  created_at?: string;
  updated_at?: string;
}

// Типы для игрока
interface Player {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  created_by_fund_id?: string;
  created_at?: string;
  updated_at?: string;
}

interface PlayerCreate {
  name: string;
  email?: string;
  phone?: string;
}

interface PlayerUpdate {
  name?: string;
  email?: string;
  phone?: string;
}

// Типы для кейса
interface Case {
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

interface CaseCreate {
  title: string;
  description: string;
  player_id: string;
  status: string;
}

interface CaseUpdate {
  title?: string;
  description?: string;
  player_id?: string;
  status?: string;
}

// Экспорт типов
export {
  LoginResponse,
  LoginCredentials,
  User,
  Fund,
  Player,
  PlayerCreate,
  PlayerUpdate,
  Case,
  CaseCreate,
  CaseUpdate
} 