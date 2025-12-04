-- Migration: 002_create_tg_identity_table.sql
-- Description: Creates the tg_identity table for storing Telegram identity data
CREATE TABLE IF NOT EXISTS test.tg_identity (
    user_id BIGINT PRIMARY KEY,
    telegram_user_id BIGINT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES test.player_info(user_id) ON DELETE CASCADE
)