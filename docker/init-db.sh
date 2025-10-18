#!/bin/bash
set -e

# Подключаемся к базе postgres
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    -- Создаем пользователя только если он не существует
    DO
    \$do\$
    BEGIN
       IF NOT EXISTS (
          SELECT
          FROM   pg_catalog.pg_roles
          WHERE  rolname = 'ai_chat_user') THEN

          CREATE USER ai_chat_user WITH PASSWORD '$POSTGRES_PASSWORD';
       END IF;
    END
    \$do\$;

    -- Создаем базу только если ее нет
    DO
    \$do\$
    BEGIN
       IF NOT EXISTS (
          SELECT FROM pg_database WHERE datname = 'ai_chat') THEN
          CREATE DATABASE ai_chat OWNER ai_chat_user;
       END IF;
    END
    \$do\$;

    -- Даем привилегии на базу
    GRANT ALL PRIVILEGES ON DATABASE ai_chat TO ai_chat_user;
EOSQL
