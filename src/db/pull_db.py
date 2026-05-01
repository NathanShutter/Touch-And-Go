"""
src/db/pull_db.py
Touch & Go — Query Student Records

Utility script to print all student records from the database.
Run directly for quick inspection: python src/db/pull_db.py
"""

import mysql.connector
from config import get_connection


def fetch_all_students() -> list[tuple]:
    """Return all rows from the student table."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    finally:
        if connection.is_connected():
            connection.close()


if __name__ == "__main__":
    rows = fetch_all_students()
    if rows:
        print(f"{'ID':<8} {'First':<15} {'Last':<15} {'Finger ID'}")
        print("-" * 50)
        for row in rows:
            print(row)
    else:
        print("No student records found.")
