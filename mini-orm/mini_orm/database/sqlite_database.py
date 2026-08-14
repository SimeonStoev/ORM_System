import sqlite3


class SqliteDatabase:
    """Thin wrapper around Python's sqlite3 module.

    Provides a minimal, ORM-agnostic interface for executing raw SQL
    against a SQLite database. Upper layers (Model, QuerySet) should
    only depend on this public interface, never on sqlite3 directly.
    """

    def __init__(self, db_path: str = ":memory:"):
        """Opens a connection to the given SQLite database.

        Args:
            db_path: Path to the database file. Defaults to ":memory:",
                which creates a temporary in-memory database.
        """
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute(self, sql: str, params: tuple = ()) -> None:
        """Executes a non-SELECT statement and commits the change.

        Intended for CREATE TABLE, INSERT, UPDATE, DELETE and DROP TABLE.

        Args:
            sql: The SQL statement to execute, with '?' placeholders.
            params: Values to bind to the placeholders in `sql`.

        Raises:
            sqlite3.OperationalError: If the SQL syntax is invalid.
        """
        self.cursor.execute(sql, params)
        self.connection.commit()

    def fetch_all(self, sql: str, params: tuple = ()) -> list[tuple]:
        """Executes a SELECT statement and returns every matching row.

        Args:
            sql: The SELECT statement to execute.
            params: Values to bind to the '?' placeholders in `sql`.

        Returns:
            A list of rows as tuples. Empty list if nothing matches.
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def fetch_one(self, sql: str, params: tuple = ()) -> tuple | None:
        """Executes a SELECT statement and returns the first matching row.

        Args:
            sql: The SELECT statement to execute.
            params: Values to bind to the '?' placeholders in `sql`.

        Returns:
            The first matching row as a tuple, or None if no row matches.
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def close(self) -> None:
        """Closes the underlying database connection."""
        self.connection.close()

    def __enter__(self):
        """Enables use as a context manager: `with SqliteDatabase() as db:`."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the connection automatically when the `with` block exits."""
        self.close()
        return False

    def table_exists(self, table_name: str) -> bool:
        """Checks whether a table with the given name exists in the database.

        Args:
            table_name: Name of the table to look for.

        Returns:
            True if the table exists, False otherwise.
        """
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return self.cursor.fetchone() is not None