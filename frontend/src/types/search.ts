/**
 * Типы данных для результатов поиска
 */

/**
 * Никнейм игрока
 */
export interface PlayerNickname {
  nickname: string;
  room: string;
  discipline?: string;
}

/**
 * Результат поиска по игрокам
 */
export interface SearchPlayer {
  id: string;
  full_name: string;
  first_name?: string;
  last_name?: string;
  middle_name?: string;
  description?: string;
  details?: string;
  fund_id?: string;
  fund_name?: string;
  nicknames?: PlayerNickname[];
  contacts?: string[];
  locations?: string[];
  cases_count?: number;
  latest_case_date?: string;
  updated_at?: string;
}

/**
 * Результат поиска по кейсам
 */
export interface SearchCase {
  id: string;
  title: string;
  status: string;
  player_id?: string;
  player_name?: string;
  fund_id?: string;
  fund_name?: string;
  created_at?: string;
  updated_at?: string;
  created_by?: string;
  updated_by?: string;
}

/**
 * Результат унифицированного поиска (все типы вместе)
 */
export interface UnifiedSearchResult {
  players: SearchPlayer[];
  cases: SearchCase[];
}

/**
 * Обобщенный результат поиска (для API, где нужен единый тип)
 */
export interface SearchResult {
  id: string;
  type: 'player' | 'case';
  title: string;
  details?: string;
  created_at?: string;
  updated_at?: string;
} 