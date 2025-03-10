-- SQL-скрипт для удаления и пересоздания таблиц игроков и кейсов
-- Рекомендуется выполнять через PgAdmin или другой SQL-клиент

-- 1. Включаем режим транзакции
BEGIN;

-- 2. Подсчет записей до удаления для контроля
SELECT 'Перед очисткой:' AS info;
SELECT COUNT(*) AS players_count FROM players;
SELECT COUNT(*) AS cases_count FROM cases;

-- 3. Сначала удаляем связанные данные (зависимые таблицы)
-- 3.1. Связанные с кейсами данные
TRUNCATE TABLE case_comments CASCADE;
TRUNCATE TABLE case_evidences CASCADE;
TRUNCATE TABLE case_logs CASCADE;
TRUNCATE TABLE case_history CASCADE;
TRUNCATE TABLE case_actions CASCADE;

-- 3.2. Связанные с игроками данные
TRUNCATE TABLE player_aliases CASCADE;
TRUNCATE TABLE player_contacts CASCADE;
TRUNCATE TABLE player_nicknames CASCADE;
TRUNCATE TABLE player_notes CASCADE;

-- 4. Теперь удаляем основные таблицы
TRUNCATE TABLE cases CASCADE;
TRUNCATE TABLE players CASCADE;

-- 5. Подсчет записей после удаления для контроля
SELECT 'После очистки:' AS info;
SELECT COUNT(*) AS players_count FROM players;
SELECT COUNT(*) AS cases_count FROM cases;

-- 6. Завершаем транзакцию
COMMIT;

-- 7. Сообщение об успешном выполнении
SELECT 'Все таблицы успешно очищены!' AS result; 