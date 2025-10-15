import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

DSN = os.getenv("DATABASE_URL") or (
    f"host={os.getenv('PGHOST')} "
    f"port={os.getenv('PGPORT')} "
    f"dbname={os.getenv('PGDATABASE')} "
    f"user={os.getenv('PGUSER')} "
    f"password={os.getenv('PGPASSWORD')}"
)

class FeedItem:
    def __init__(self, product_id, title, price, store_id):
        self.product_id = product_id
        self.title = title
        self.price = price
        self.store_id = store_id

    def upsert_feed_item_query()->str:
        return """
            INSERT INTO feed_items (product_id, title, price, store_id)
            VALUES %s
            ON CONFLICT (product_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                price = EXCLUDED.price,
                store_id = EXCLUDED.store_id,
                updated_at = now()
            RETURNING product_id
            """

    def insert_feed_items(rows):
        conn = psycopg2.connect(DSN)
        sql = FeedItem.upsert_feed_item_query()
        
        try:
            with conn:
                with conn.cursor() as cur:
                    execute_values(cur, sql, rows)
                    result = cur.fetchall()
                    return result
        finally:
            conn.close()
