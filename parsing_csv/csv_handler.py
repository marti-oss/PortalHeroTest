import csv

class CSVHandler:
    def __init__(self):
        self.data = list()
        self.header = {'product_id','title','price','store_id'}

    def validate_header(self, header):
        if set(header) != self.header:
            raise ValueError(f'Wrong header: {header}')
    
    def validate_content(self, row):
        for item in self.header:
            if row[item] == '' or row[item] is None:
                print(f"Missing or empty field '{item}' in row: {row}")
                return False
        try:
            product_id = int(row['product_id'])
            title = str(row['title'])
            price = float(row['price'])
            store_id = str(row['store_id'])
        except ValueError:
            print(f"Invalid data types in row: {row}")
            return False
        return True
    
    def read_csv(self, file_path):
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                header = reader.fieldnames
                self.validate_header(header)
                for row in reader:
                    if self.validate_content(row):
                        self.data.append(row)
                    else:
                        print(f"Invalid row: {row}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None