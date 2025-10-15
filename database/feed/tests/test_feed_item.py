# tests/test_feed_item_unittest.py
import unittest
from unittest.mock import patch, MagicMock

# Ajuste esta importación al path real de su módulo
from database.feed.feed_item import FeedItem


def make_mock_conn(fetchall_return):
    mock_conn = MagicMock(name="connection")
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.__exit__.return_value = False

    mock_cursor_cm = MagicMock(name="cursor_cm")
    mock_cursor = MagicMock(name="cursor")
    mock_cursor.fetchall.return_value = fetchall_return
    mock_cursor_cm.__enter__.return_value = mock_cursor
    mock_cursor_cm.__exit__.return_value = False

    mock_conn.cursor.return_value = mock_cursor_cm
    return mock_conn, mock_cursor


class TestFeedItem(unittest.TestCase):

    def setUp(self):
        self.default_fetch = [(1,), (2,)]
        self.mock_conn, self.mock_cursor = make_mock_conn(self.default_fetch)

    def test_upsert_feed_item_query_contains_on_conflict(self):
        sql = FeedItem.upsert_feed_item_query()
        self.assertIn("ON CONFLICT (product_id)", sql)
        self.assertIn("DO UPDATE SET", sql)
        self.assertIn("RETURNING product_id", sql)

    @patch("database.feed.feed_item.execute_values")
    @patch("database.feed.feed_item.psycopg2.connect")
    def test_insert_feed_items_success(self, mock_connect, mock_execute_values):
        rows = [(1, "Title 1", 9.99, 10), (2, "Title 2", 19.99, 10)]
        mock_connect.return_value = self.mock_conn
        mock_execute_values.return_value = None

        result = FeedItem.insert_feed_items(rows)

        mock_execute_values.assert_called_once()
        args, kwargs = mock_execute_values.call_args
        called_cursor = args[0]
        called_sql = args[1]
        called_rows = args[2]

        self.assertIs(called_cursor, self.mock_conn.cursor().__enter__())
        self.assertIsInstance(called_sql, str)
        self.assertIn("INSERT INTO feed_items", called_sql)
        self.assertEqual(called_rows, rows)

        self.assertEqual(result, self.default_fetch)

        self.mock_conn.close.assert_called_once()

    @patch("database.feed.feed_item.execute_values")
    @patch("database.feed.feed_item.psycopg2.connect")
    def test_insert_feed_items_execute_values_raises(self, mock_connect, mock_execute_values):
        rows = [(1, "Title", 9.99, 10)]
        mock_conn_err, _ = make_mock_conn(None)
        mock_connect.return_value = mock_conn_err

        mock_execute_values.side_effect = RuntimeError("boom")

        with self.assertRaises(RuntimeError):
            FeedItem.insert_feed_items(rows)

        mock_conn_err.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
