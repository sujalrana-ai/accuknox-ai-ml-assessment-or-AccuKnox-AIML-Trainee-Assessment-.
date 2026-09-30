import csv
import re
import sqlite3
from typing import Iterator, Tuple

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


def validate_row(row: dict) -> Tuple[bool, str]:
    if not row.get("name") or not row.get("name").strip():
        return False, "Empty name"
    email = row.get("email", "").strip()
    if not email or not EMAIL_REGEX.match(email):
        return False, f"Invalid email format: {email}"
    return True, "Valid"


def stream_csv_records(
    file_path: str,
) -> Iterator[Tuple[str, str, str, str]]:
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):
            is_valid, reason = validate_row(row)
            if not is_valid:
                print(f"[Line {line_no} SKIPPED] {reason} | Row: {dict(row)}")
                continue
            yield (
                row["name"].strip(),
                row["email"].strip().lower(),
                row.get("role", "User").strip(),
                row.get("department", "Engineering").strip(),
            )


def ingest_csv_to_sqlite(csv_file_path: str, db_file_path: str = "users.db"):
    create_schema_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        role TEXT DEFAULT 'User',
        department TEXT DEFAULT 'Engineering',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    """

    insert_sql = """
    INSERT INTO users (name, email, role, department)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(email) DO UPDATE SET
        name = excluded.name,
        role = excluded.role,
        department = excluded.department;
    """

    with sqlite3.connect(db_file_path) as conn:
        cursor = conn.cursor()
        cursor.executescript(create_schema_sql)

        batch = []
        batch_size = 500
        total_ingested = 0

        for record in stream_csv_records(csv_file_path):
            batch.append(record)
            if len(batch) >= batch_size:
                cursor.executemany(insert_sql, batch)
                conn.commit()
                total_ingested += len(batch)
                batch.clear()

        if batch:
            cursor.executemany(insert_sql, batch)
            conn.commit()
            total_ingested += len(batch)

        print(f"Successfully synced {total_ingested} records into '{db_file_path}'.")


if __name__ == "__main__":
    ingest_csv_to_sqlite("users_sample.csv")
