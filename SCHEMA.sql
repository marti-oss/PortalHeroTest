CREATE TABLE IF NOT EXISTS feed_items (
product_id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
price NUMERIC(10,2),
store_id TEXT,
created_at TIMESTAMPTZ DEFAULT now(),
updated_at TIMESTAMPTZ DEFAULT now()
CONSTRAINT price_non_negative CHECK (price IS NULL OR price >= 0)
);

CREATE INDEX IF NOT EXISTS idx_feed_imtes_store ON feed_items(store_id);

CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
NEW.updated_at = now();
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_feed_items_updated_at
BEFORE UPDATE ON feed_items
FOR EACH ROW
EXECUTE FUNCTION trigger_set_updated_at();