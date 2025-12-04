-- Migration: 004_create_items_table.sql
-- Description: Creates the items table for item definitions

CREATE TABLE IF NOT EXISTS test.items (
    item_id INT PRIMARY KEY
);