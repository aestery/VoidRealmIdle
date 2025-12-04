-- Migration: 004_create_team_in_void_table.sql
-- Description: Creates the team_in_void table for storing info about teams in Void

CREATE TABLE IF NOT EXISTS test.player_teams (
    user_id BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES test.player_info(user_id) ON DELETE CASCADE
);
