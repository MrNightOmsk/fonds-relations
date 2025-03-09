/**
 * Типы данных для результатов поиска
 */

/**
 * Результат поиска по игрокам
 */
export interface SearchPlayer {
  id: string;
  full_name: string;
  first_name?: string;
  last_name?: string;
  middle_name?: string;
  details?: string;
  fund_id?: string;
  fund_name?: string;
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
  created_at: string;
  updated_at?: string;
}

/**
 * Общий результат унифицированного поиска
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