"""
src/db/push_db.py
Touch & Go — Insert a Student Record

Utility script to manually add a student to the database.
Run directly: python src/db/push_db.py
"""

import mysql.connector
from config import get_connection


def insert_student(user_id: int, first_name: str, last_name: str) -> None:
    """Insert a new student row into the student table."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO student (userId, firstName, lastName) VALUES (%s, %s, %s)",
            (user_id, first_name, last_name),
        )
        connection.commit()
        print(f"Student '{first_name} {last_name}' (ID: {user_id}) added successfully.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if connection.is_connected():
            connection.close()


if __name__ == "__main__":
    print("Add a new student record")
    print("------------------------")
    try:
        user_id = int(input("Enter user ID: ").strip())
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()
        insert_student(user_id, first_name, last_name)
    except ValueError:
        print("Invalid user ID — must be a number.")
