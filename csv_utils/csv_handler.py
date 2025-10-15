import csv
import os
from logger import logging

class CSVHandler:
    def __init__(self):
        self.data = list()
        self.header = {'product_id', 'title', 'price', 'store_id'}

    def validate_header(self, header):
        if header != self.header:
            raise ValueError(f"Wrong header: {header}")

    def validate_content(self, row):
        for item in self.header:
            if row[item] == '' or row[item] is None:
                logging.error(f"Missing or empty field in row: {row}")
                return False
        try:
            product_id = int(row['product_id'])
            title = str(row['title'])
            price = float(row['price'])
            store_id = str(row['store_id'])
            if product_id <= 0 or price < 0:
                logging.error(f"Invalid values in row: {row}")
                return False
        except ValueError:
            logging.error(f"Invalid data types in row: {row}")
            return False

        return True

    def read_csv(self, file_path):
        self.data.clear()
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return None

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                header = reader.fieldnames
                self.validate_header(set(header))

                for row in reader:
                    if self.validate_content(row):
                        self.data.append(row)
                    else:
                        logging.warning(f"Invalid row: {row}")
        except Exception as e:
            logging.error(f"An error occurred while reading {file_path}: {e}")
            return None

        logging.info(f"Successfully read {len(self.data)} valid rows from {file_path}.")
        return self.data