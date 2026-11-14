"""Database Management Systems - Assignment 3, Question 1.
Sohayb Faraj
CUID: 101333119
"""

import os
from datetime import date
from getpass import getpass

import psycopg


# Default database settings. The password is entered when the program starts.
DB_CONFIG = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432"),
    "dbname": os.getenv("PGDATABASE", "assignment3"),
    "user": os.getenv("PGUSER", "postgres"),
    "connect_timeout": 5,
}


def connect():
    """Connect to PostgreSQL."""
    # Each with block commits on success, rolls back on error, and closes the connection.
    return psycopg.connect(**DB_CONFIG)


def getAllStudents():
    """Retrieve, display, and return every student in primary-key order."""
    with connect() as connection:
        rows = connection.execute(
            "SELECT student_id, first_name, last_name, email, enrollment_date "
            "FROM students ORDER BY student_id"
        ).fetchall()
    if not rows:
        print("No students found.")
    else:
        for student_id, first, last, email, enrolled in rows:
            print(f"\nStudent ID: {student_id}")
            print(f"Name: {first} {last}")
            print(f"Email: {email}")
            print(f"Enrollment date: {enrolled if enrolled is not None else 'NULL'}")
    return rows


def addStudent(first_name, last_name, email, enrollment_date):
    """Insert a student using bound parameters and return the generated ID."""
    # Pass values separately so user input is treated as data, not SQL.
    with connect() as connection:
        row = connection.execute(
            "INSERT INTO students (first_name, last_name, email, enrollment_date) "
            "VALUES (%s, %s, %s, %s) RETURNING student_id",
            (first_name, last_name, email, enrollment_date),
        ).fetchone()
    print(f"Student added. Student ID: {row[0]}")
    return row[0]


def updateStudentEmail(student_id, new_email):
    """Update one student's email and report whether the ID exists."""
    with connect() as connection:
        row = connection.execute(
            "UPDATE students SET email = %s WHERE student_id = %s "
            "RETURNING student_id", (new_email, student_id),
        ).fetchone()
    print("Email updated." if row else "No student found with that ID.")
    return row is not None


def deleteStudent(student_id):
    """Delete one student and report whether the ID exists."""
    with connect() as connection:
        row = connection.execute(
            "DELETE FROM students WHERE student_id = %s RETURNING student_id",
            (student_id,),
        ).fetchone()
    print("Student deleted." if row else "No student found with that ID.")
    return row is not None


def required(prompt):
    """Reject blank required fields before sending a query."""
    value = input(prompt).strip()
    if not value:
        raise ValueError("This field cannot be blank.")
    return value


def read_id():
    """Accept only positive integer student IDs."""
    value = int(required("Student ID: "))
    if value <= 0:
        raise ValueError("Student ID must be a positive integer.")
    return value


def main():
    """Run the interactive menu and keep database errors from ending the session."""
    print("Student Database - Assignment 3 Q1")
    print(f"Database: {DB_CONFIG['dbname']}")
    print(f"Server: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    DB_CONFIG["password"] = getpass("PostgreSQL password (hidden): ")
    while True:
        print("\n1. getAllStudents\n2. addStudent\n3. updateStudentEmail\n4. deleteStudent\n0. Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "0":
                print("Goodbye.")
                return
            if choice == "1":
                getAllStudents()
            elif choice == "2":
                first = required("First name: ")
                last = required("Last name: ")
                email = required("Email: ")
                entered_date = input("Enrollment date (YYYY-MM-DD, blank for NULL): ").strip()
                enrolled = date.fromisoformat(entered_date) if entered_date else None
                addStudent(first, last, email, enrolled)
            elif choice == "3":
                updateStudentEmail(read_id(), required("New email: "))
            elif choice == "4":
                deleteStudent(read_id())
            else:
                print("Choose 0, 1, 2, 3, or 4.")
        except ValueError as error:
            print(f"Invalid input: {error}")
        except psycopg.errors.UniqueViolation:
            print("That email is already used by another student. No change was saved.")
        except psycopg.OperationalError:
            print("Cannot connect. Check that PostgreSQL is running and verify your database, user, port, and password.")
        except psycopg.errors.UndefinedTable:
            print("The students table is missing. Run database/setup.sql in this database first.")
        except psycopg.Error as error:
            print(f"Database error: {error.diag.message_primary or 'Operation failed'}. No change was saved.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nApplication closed.")
