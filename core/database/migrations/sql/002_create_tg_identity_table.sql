-- Migration: 003_create_tg_identity_table.sql
-- Description: Creates the tg_identity table for storing Telegram identity data
CREATE TABLE IF NOT EXISTS test.tg_identity (
    user_id BIGSERIAL PRIMARY KEY,
    telegram_user_id BIGINT NOT NULL UNIQUE
)