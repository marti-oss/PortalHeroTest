import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from logger import logging

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

    @staticmethod
    def upsert_feed_item_query() -> str:
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

    @staticmethod
    def execute_query(sql, params=None, fetch=False):
        conn = psycopg2.connect(DSN)
        try:
            with conn:
                with conn.cursor() as cur:
                    if params:
                        cur.execute(sql, params)
                    else:
                        cur.execute(sql)
                    if fetch:
                        return cur.fetchall()
                    return cur.rowcount
        except Exception as e:
            logging.error(f"Database query failed: {e}")
            raise
        finally:
            conn.close()

    @staticmethod
    def execute_values_query(sql, rows):
        conn = psycopg2.connect(DSN)
        try:
            with conn:
                with conn.cursor() as cur:
                    execute_values(cur, sql, rows)
                    logging.info(f"Executed batch query with {len(rows)} rows.")
                    return cur.fetchall()
        except Exception as e:
            logging.error(f"Batch query failed: {e}")
            raise
        finally:
            conn.close()

    @classmethod
    def insert_feed_items(cls, rows):
        sql = cls.upsert_feed_item_query()
        logging.info(f"Inserting/Updating {len(rows)} feed items.")
        return cls.execute_values_query(sql, rows)

    @classmethod
    def get_product_id_feed_items(cls):
        sql = "SELECT product_id FROM feed_items"
        logging.info("Fetching product IDs from the database.")
        result = cls.execute_query(sql, fetch=True)
        return [row[0] for row in result]

    @classmethod
    def delete_feed_items(cls, product_ids):
        sql = "DELETE FROM feed_items WHERE product_id = ANY(%s)"
        logging.info(f"Deleting {len(product_ids)} feed items.")
        return cls.execute_query(sql, (product_ids,))