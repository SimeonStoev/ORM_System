import sqlite3

class SqliteDatabase:
    def __init__(self, db_path: str = ":memory:"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute(self, sql: str, params: tuple = ()) -> None:
        self.cursor.execute(sql, params)
        self.connection.commit()

    def fetch_all(self, sql: str, params: tuple=()) -> list[tuple]:
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def fetch_one(self, sql: str, params: tuple=()) -> tuple | None:
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def table_exists(self, table_name: str) -> bool:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return self.cursor.fetchone() is not None

