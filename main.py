import sys
from logger import logging 
from csv_utils.csv_handler import CSVHandler
from database.feed_item import FeedItem

def process_csv(file_path, action)->list:
    logging.info(f"Processing CSV file: {file_path}")
    csv_handler = CSVHandler()
    data = csv_handler.read_csv(file_path)

    if not data:
        logging.warning(f"No valid data found in {file_path}.")
        return []

    rows = [(int(item['product_id']), item['title'], float(item['price']), item['store_id']) for item in data]
    logging.info(f"Prepared {len(rows)} rows for {action}.")
    return rows

def synchronize_feed_items(feed_rows):
    logging.info("Synchronizing feed items...")
    FeedItem.insert_feed_items(feed_rows)
    logging.info("Feed items synchronization complete.")

def synchronize_portal_data(portal_rows):
    logging.info("Starting portal data synchronization...")
    db_items = FeedItem.get_product_id_feed_items()
    portal_product_ids = [row[0] for row in portal_rows]

    products_to_delete = [product_id for product_id in db_items if product_id not in portal_product_ids]
    if products_to_delete:
        logging.info(f"Deleting {len(products_to_delete)} products from the database.")
        FeedItem.delete_feed_items(products_to_delete)

    logging.info(f"Inserting/Updating {len(portal_rows)} products in the database.")
    FeedItem.insert_feed_items(portal_rows)
    logging.info("Portal data synchronization complete.")

def main() -> int:
    logging.info("Starting program...")

    feed_rows = process_csv('feed_items.csv', action='feed')
    if feed_rows:
        synchronize_feed_items(feed_rows)
    portal_rows = process_csv('portal_items.csv', action='portal')
    if portal_rows:
        synchronize_portal_data(portal_rows)

    logging.info("Program execution complete.")
    return 0

if __name__ == "__main__":
    sys.exit(main())