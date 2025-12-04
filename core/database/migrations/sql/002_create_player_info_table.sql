-- Migration: 003_create_player_info_table.sql
-- Description: Creates the player_info table for storing player data

CREATE TABLE IF NOT EXISTS test.player_info (
    user_id BIGSERIAL PRIMARY KEY,
    character_name VARCHAR(50),
    language VARCHAR(10) NOT NULL DEFAULT 'en' CHECK (language IN ('en', 'ru')), 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on language for filtering
CREATE INDEX IF NOT EXISTS idx_player_info_language 
    ON test.player_info(language);

