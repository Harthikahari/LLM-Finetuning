"""SQL execution utilities for validation."""

import logging
import sqlite3
from typing import Any, Optional, List, Tuple

logger = logging.getLogger(__name__)


class SQLExecutor:
    """Execute SQL queries for validation."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Connect to database."""
        self.connection = sqlite3.connect(self.db_path)
        logger.info(f"Connected to database: {self.db_path}")

    def execute(self, query: str) -> Tuple[bool, Any]:
        """Execute SQL query."""
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return True, results
        except Exception as e:
            logger.warning(f"SQL execution failed: {e}")
            return False, str(e)

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None


def execute_sql(query: str, db_path: str) -> Tuple[bool, Any]:
    """Execute SQL query."""
    executor = SQLExecutor(db_path)
    success, result = executor.execute(query)
    executor.close()
    return success, result
