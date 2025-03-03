-- НЕ ИСПОЛЬЗУЕТСЯ. 
-- Этот скрипт заменен системой миграций Alembic.
-- См. директорию backend/alembic/versions для текущих миграций.

/*
-- Переименование таблицы fund в funds
ALTER TABLE fund RENAME TO funds;

-- Обновление последовательностей и индексов (если они есть)
ALTER INDEX IF EXISTS fund_pkey RENAME TO funds_pkey;
ALTER INDEX IF EXISTS fund_name_key RENAME TO funds_name_key;

-- Обновление внешних ключей, которые ссылаются на таблицу fund
ALTER TABLE users
DROP CONSTRAINT IF EXISTS users_fund_id_fkey,
ADD CONSTRAINT users_fund_id_fkey FOREIGN KEY (fund_id) REFERENCES funds(id);

ALTER TABLE players
DROP CONSTRAINT IF EXISTS players_created_by_fund_id_fkey,
ADD CONSTRAINT players_created_by_fund_id_fkey FOREIGN KEY (created_by_fund_id) REFERENCES funds(id);

ALTER TABLE cases
DROP CONSTRAINT IF EXISTS cases_created_by_fund_id_fkey,
ADD CONSTRAINT cases_created_by_fund_id_fkey FOREIGN KEY (created_by_fund_id) REFERENCES funds(id);
*/ 