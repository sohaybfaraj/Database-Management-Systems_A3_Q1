# Assignment 3 - Question 1

Sohayb Faraj  
CUID: 101333119

Python application for managing student records in PostgreSQL.

## Requirements

Python 3.10 or later, PostgreSQL, and pgAdmin 4.

## Database setup

Create a database named `assignment3` in pgAdmin. Open its Query Tool and run `database/setup.sql` once. This creates the students table and inserts the three provided records.

## Installation

Run from the project folder in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No compilation is required.

## Run

```powershell
.\.venv\Scripts\python.exe app/main.py
```

Enter the PostgreSQL password at the prompt.

Default connection settings:

- Host: localhost
- Port: 5432
- Database: assignment3
- User: postgres

Connection settings can be changed using the `PGHOST`, `PGPORT`, `PGDATABASE`, and `PGUSER` environment variables.

## Functions

- `getAllStudents()` displays all students ordered by ID.
- `addStudent(first_name, last_name, email, enrollment_date)` inserts a student and returns the new ID.
- `updateStudentEmail(student_id, new_email)` updates a student's email.
- `deleteStudent(student_id)` deletes a student.

Menu options 1 to 4 run these functions. Option 0 exits. Dates use YYYY-MM-DD. A blank date is stored as NULL.

Queries use bound parameters. Successful operations are committed, and failed operations are rolled back. The program handles invalid input, duplicate emails, missing IDs, and database errors.

## Verification

Run this query in pgAdmin after an operation:

```sql
SELECT * FROM students ORDER BY student_id;
```

## Demonstration video

[Demonstration video](https://www.youtube.com/watch?v=mDfWpwnJ-g8)
