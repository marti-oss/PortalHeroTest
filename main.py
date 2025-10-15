import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logger import logging 
from csv_utils.csv_handler import CSVHandler
from database.feed_item import FeedItem


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        if file_path.endswith(".csv"):
            logging.info(f"New file detected: {file_path}")
            action = "feed" if "feed" in file_path else "portal" if "portal" in file_path else None
            if action:
                rows = process_csv(file_path, action)
                if rows:
                    if action == "feed":
                        synchronize_feed_items(rows)
                    elif action == "portal":
                        synchronize_portal_data(rows)

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
    folder_to_watch = os.getenv("FOLDER_TO_WATCH")
    if not os.path.exists(folder_to_watch):
        logging.error(f"Folder not found: {folder_to_watch}")
        return 1

    logging.info(f"Starting folder monitoring: {folder_to_watch}")
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    logging.info("Folder monitoring stopped.")
    return 0

if __name__ == "__main__":
    sys.exit(main())