import  shlex
import sys
from parsing_csv.csv_handler import CSVHandler
from database.feed.feed_item import FeedItem

def main() -> int:
    print("Starting program...")
    csv_handler = CSVHandler()
    print("Reading CSV file...")
    csv_handler.read_csv('feed_items.csv')
    print(f"Data read: {len(csv_handler.data)} records.")
    print("Preparing data for insertion...")
    rows = [(int(item['product_id']), item['title'], float(item['price']), item['store_id']) for item in csv_handler.data]
    print(f"Prepared {len(rows)} rows for insertion.")
    print("Inserting data into database...")
    FeedItem.insert_feed_items(rows)
    print("Data insertion complete.")
    return (0)

if __name__ == "__main__":
    sys.exit(main())