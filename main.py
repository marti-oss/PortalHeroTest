import  shlex
import sys
from parsing_csv.csv_handler import CSVHandler

def main() -> int:
    print("Starting program...")
    csv_handler = CSVHandler()
    print("Reading CSV file...")
    csv_handler.read_csv('feed_items.csv')
    print(f"Data read: {len(csv_handler.data)} records.")
    return (0)

if __name__ == "__main__":
    sys.exit(main())