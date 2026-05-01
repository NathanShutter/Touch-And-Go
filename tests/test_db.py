"""
tests/test_db.py
Touch & Go — Database Integration Tests

Tests the MySQL connection and basic student insertion/deletion.
Requires a running database configured via .env.

Run with: python -m pytest tests/test_db.py -v
"""

import unittest
import mysql.connector
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from db.config import get_connection


def prompt_for_test_student() -> tuple[int, str, str]:
    """Prompt for a test student record, or use defaults."""
    use_custom = input("Use custom test data? (y/n, default n): ").strip().lower()
    if use_custom in ("y", "yes"):
        while True:
            try:
                user_id = int(input("Enter a user ID (number above 100): "))
                if user_id > 100:
                    break
                print("ID must be above 100 to avoid collisions with real records.")
            except ValueError:
                print("Please enter a valid integer.")
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
    else:
        user_id, first_name, last_name = 999, "Test", "User"
        print(f"Using default test record: ID={user_id}, {first_name} {last_name}")
    return user_id, first_name, last_name


class TestDatabaseConnection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = get_connection()
        cls.cursor = cls.connection.cursor()
        cls.user_id, cls.first_name, cls.last_name = prompt_for_test_student()

    @classmethod
    def tearDownClass(cls):
        if cls.connection.is_connected():
            print("\nCleaning up test record...")
            cls.cursor.execute(
                "DELETE FROM student WHERE userId = %s", (cls.user_id,)
            )
            cls.connection.commit()
            cls.connection.close()
            print("Done.")

    def test_connection_is_open(self):
        self.assertTrue(
            self.connection.is_connected(),
            "Database connection should be open."
        )

    def test_insert_student(self):
        self.cursor.execute(
            "INSERT INTO student (userId, firstName, lastName) VALUES (%s, %s, %s)",
            (self.user_id, self.first_name, self.last_name),
        )
        self.connection.commit()
        self.assertEqual(
            self.cursor.rowcount, 1, "Exactly one row should be inserted."
        )

    def test_student_exists_after_insert(self):
        self.cursor.execute(
            "SELECT userId FROM student WHERE userId = %s", (self.user_id,)
        )
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Inserted student should be retrievable.")


if __name__ == "__main__":
    unittest.main()
