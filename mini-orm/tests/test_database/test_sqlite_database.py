from mini_orm.database.sqlite_database import SqliteDatabase
from unittest import TestCase, main
import sqlite3


class TestSqliteDatabase(TestCase):
    def setUp(self):
        self.db = SqliteDatabase(":memory:")

    def test_execute_creates_table(self):
        self.db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        result = self.db.fetch_all(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        self.assertIn(("users",), result)

    def test_execute_insert_and_fetch_all(self):
        self.db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        self.db.execute("INSERT INTO users (name) VALUES (?)", ("Ivan",))
        result = self.db.fetch_all("SELECT * FROM users")
        self.assertEqual(result, [(1, "Ivan")])

    def test_fetch_one_returns_none_when_no_result(self):
        self.db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        result = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (999,))
        self.assertIsNone(result)

    def test_fetch_all_returns_empty_list_when_no_results(self):
        self.db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        result = self.db.fetch_all("SELECT * FROM users")
        self.assertEqual(result, [])

    def test_invalid_sql_raises_operational_error(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.db.execute("CREATE TABLE users id INTEGER")  # умишлено грешен синтаксис


if __name__ == "__main__":
    main()