-- Migration: 004_create_player_inventory_table.sql
-- Description: Creates the player_inventory table for storing player belongings

CREATE TABLE IF NOT EXISTS test.player_inventory (
	user_id BIGINT REFERENCES test.player_info(user_id) NOT NULL,
	item_id INT REFERENCES test.items(item_id) NOT NULL,
	quntity BIGINT NOT NULL DEFAULT 0,

	PRIMARY KEY (user_id, item_id)
);