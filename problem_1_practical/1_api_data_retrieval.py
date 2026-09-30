import sqlite3
from typing import Any, Dict, List
import requests
from tabulate import tabulate


class BookDataPipeline:

    def __init__(
        self,
        db_path: str = "books_catalog.db",
        api_url: str = "https://openlibrary.org/search.json",
    ):
        self.db_path = db_path
        self.api_url = api_url
        self._initialize_database()

    def _initialize_database(self) -> None:
        """Create the table schema if it does not exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publication_year INTEGER
                )
            """)
            conn.commit()

    def fetch_and_parse(
        self, query: str = "cloud security", limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Fetch books from REST API and transform to normalized records."""
        params = {"q": query, "limit": limit}
        response = requests.get(self.api_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        parsed_books = []

        for doc in data.get("docs", []):
            book_id = doc.get("key", "").replace("/works/", "")
            title = doc.get("title", "Unknown Title")
            authors = ", ".join(doc.get("author_name", ["Unknown Author"]))
            year = doc.get("first_publish_year", None)

            if book_id and title:
                parsed_books.append({
                    "id": book_id,
                    "title": title,
                    "author": authors,
                    "publication_year": year,
                })
        return parsed_books

    def store_books(self, books: List[Dict[str, Any]]) -> int:
        """Insert records into SQLite with idempotency handling."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(
                """
                INSERT INTO books (id, title, author, publication_year)
                VALUES (:id, :title, :author, :publication_year)
                ON CONFLICT(id) DO UPDATE SET
                    title=excluded.title,
                    author=excluded.author,
                    publication_year=excluded.publication_year
            """,
                books,
            )
            conn.commit()
            return cursor.rowcount

    def display_stored_books(self) -> None:
        """Fetch and print records in a structured tabular format."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, author, publication_year FROM books"
            )
            rows = cursor.fetchall()
            headers = ["ID", "Title", "Author(s)", "Publication Year"]
            print(tabulate(rows, headers=headers, tablefmt="github"))


if __name__ == "__main__":
    pipeline = BookDataPipeline()
    records = pipeline.fetch_and_parse(query="kubernetes runtime", limit=8)
    pipeline.store_books(records)
    print("\n--- Current Books in Database ---")
    pipeline.display_stored_books()
