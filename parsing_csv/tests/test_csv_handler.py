import unittest
import os
from parsing_csv.csv_handler import CSVHandler
from io import StringIO
from unittest.mock import patch


class TestCSVHandler(unittest.TestCase):
    def setUp(self):
        self.handler = CSVHandler()
        self.csv_feed_items_path = os.path.join(os.path.dirname(__file__), '../../feed_items.csv')
        self.csv_feed_items_path = os.path.abspath(self.csv_feed_items_path)

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.csv_feed_items_path))
    
    def test_read_csv_valid_file_all_rows_completed(self):
        self.handler.read_csv(self.csv_feed_items_path)
        self.assertEqual(len(self.handler.data), 9)
        self.assertEqual(self.handler.data[0]['product_id'], '1084')
        self.assertEqual(self.handler.data[0]['title'], 'PORTATIL MACBOOK AIR 2017/I5/8GB RAM/128GB SSD ( 13 )')
        self.assertEqual(self.handler.data[0]['price'], '599.95')
        self.assertEqual(self.handler.data[0]['store_id'], '1|3')
        self.assertEqual(self.handler.data[1]['product_id'], '1946')
        self.assertEqual(self.handler.data[1]['title'], 'GOOGLE CHROMECAST 3GEN')
        self.assertEqual(self.handler.data[1]['price'], '29.95')
        self.assertEqual(self.handler.data[1]['store_id'], '4|2')
        self.assertEqual(self.handler.data[2]['product_id'], '2194')
        self.assertEqual(self.handler.data[2]['title'], 'MULTIHERRAMIENTA DREMEL 3000 CON MALETIN Y ACCESORIOS')
        self.assertEqual(self.handler.data[2]['price'], '39.95')
        self.assertEqual(self.handler.data[2]['store_id'], '1')
        self.assertEqual(self.handler.data[3]['product_id'], '2213')
        self.assertEqual(self.handler.data[3]['title'], 'TELEFONO MOVIL SAMSUNG GALAXY S21+ 5G 128GB PRECINTADO')
        self.assertEqual(self.handler.data[3]['price'], '699.95')
        self.assertEqual(self.handler.data[3]['store_id'], '0|1')
        self.assertEqual(self.handler.data[4]['product_id'], '2308')
        self.assertEqual(self.handler.data[4]['title'], 'MARTILLO PERCUTOR MILWAUKEE HD18 H M18+BATERIA 12.0AH+MALETIN')
        self.assertEqual(self.handler.data[4]['price'], '314.95')
        self.assertEqual(self.handler.data[4]['store_id'], '3')
        self.assertEqual(self.handler.data[5]['product_id'], '2360')
        self.assertEqual(self.handler.data[5]['title'], 'DISCO DURO MULTIMEDIA GIGA TV HD 730 1TB')
        self.assertEqual(self.handler.data[5]['price'], '32.95')
        self.assertEqual(self.handler.data[5]['store_id'], '2|4')
        self.assertEqual(self.handler.data[6]['product_id'], '2735')
        self.assertEqual(self.handler.data[6]['title'], 'XIAOMI MI TV STICK CON CONTROL REMOTO A ESTRENAR')
        self.assertEqual(self.handler.data[6]['price'], '24.95')
        self.assertEqual(self.handler.data[6]['store_id'], '1|3')
        self.assertEqual(self.handler.data[7]['product_id'], '3924')
        self.assertEqual(self.handler.data[7]['title'], 'AURICULARES BEATS SOLO 3 COLOR ORO ROSA')
        self.assertEqual(self.handler.data[7]['price'], '79.95')
        self.assertEqual(self.handler.data[7]['store_id'], '0|3')
        self.assertEqual(self.handler.data[8]['product_id'], '7525')
        self.assertEqual(self.handler.data[8]['title'], 'CASCO FOX HELMET V3 PILOT / NEGRO Y ROJO')
        self.assertEqual(self.handler.data[8]['price'], '89.95')
        self.assertEqual(self.handler.data[8]['store_id'], '1')
    
    def test_file_no_exist(self):
        invalid_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../no_existe.csv"))
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            self.handler.read_csv(invalid_csv)
            output = fake_out.getvalue().strip()

        self.assertIn("An error occurred", output)
        self.assertEqual(self.handler.data, list())
    
    def test_invalid_naming_header(self):
        invalid_header_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "./files/invalid_header.csv"))
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            self.handler.read_csv(invalid_header_csv)
            output = fake_out.getvalue().strip()

        self.assertIn("An error occurred", output)
        self.assertEqual(self.handler.data, list())

    def test_missing_header(self):
        missing_header_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "./files/missing_header.csv"))
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            self.handler.read_csv(missing_header_csv)
            output = fake_out.getvalue().strip()

        self.assertIn("An error occurred: Wrong header: ['product_id', 'title', 'price', '']", output)
        self.assertEqual(self.handler.data, list())
    
    def test_empty_content(self):
        empty_content_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "./files/empty_content.csv"))
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            self.handler.read_csv(empty_content_csv)
            output = fake_out.getvalue().strip()

        self.assertIn("Missing or empty field 'store_id'", output)
        self.assertEqual(len(self.handler.data), 8)
    
    def test_validate_headers_all_valid(self):
        valid_header = ['product_id', 'title', 'price', 'store_id']
        self.handler.validate_header(valid_header)
    
    def test_validate_header_invalid_missing_field(self):
        header = ['price', 'store_id']
        with self.assertRaises(ValueError):
            self.handler.validate_header(header)
    
    def test_validate_header_invalid_extra_field(self):
        header = ['product_id', 'title', 'price', 'store_id', 'extra_field']
        with self.assertRaises(ValueError):
            self.handler.validate_header(header)

    def test_validate_header_invalid_different_field(self):
        header = ['product_id', 'title', 'precio', 'store_id']
        with self.assertRaises(ValueError):
            self.handler.validate_header(header)
    
    def test_validate_content_valid(self):
        row = {
            "product_id": "123",
            "title": "Camiseta",
            "price": "19.99",
            "store_id": "store_01",
        }
        self.assertTrue(self.handler.validate_content(row))

    def test_validate_content_empty_field(self):
        row = {
            "product_id": "123",
            "title": "",
            "price": "19.99",
            "store_id": "store_01",
        }
        self.assertFalse(self.handler.validate_content(row))

    def test_validate_content_none_field(self):
        row = {
            "product_id": "123",
            "title": "Camiseta",
            "price": None,
            "store_id": "store_01",
        }
        self.assertFalse(self.handler.validate_content(row))

    def test_validate_content_invalid_product_id(self):
        row = {
            "product_id": "abc",
            "title": "Camiseta",
            "price": "19.99",
            "store_id": "store_01",
        }
        self.assertFalse(self.handler.validate_content(row))

    def test_validate_content_invalid_price(self):
        row = {
            "product_id": "123",
            "title": "Camiseta",
            "price": "diecinueve",
            "store_id": "store_01",
        }
        self.assertFalse(self.handler.validate_content(row))

    def test_validate_content_missing_key_raises_keyerror(self):
        row = {
            "product_id": "123",
            "title": "Camiseta",
            "store_id": "store_01",
        }
        with self.assertRaises(KeyError):
            self.handler.validate_content(row)
        

if __name__ == '__main__':
    unittest.main()