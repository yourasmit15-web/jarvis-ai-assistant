import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from backend.utils.helpers import utc_now_iso

FORBIDDEN_TERMS = ("password", "token", "secret", "private key")


@dataclass
class MemoryStore:
    db_path: str

    def __post_init__(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def _validate_content(self, content: str) -> None:
        lower = content.lower()
        if any(term in lower for term in FORBIDDEN_TERMS):
            raise ValueError("Refusing to store secrets in memory")

    def add(self, category: str, content: str) -> dict[str, Any]:
        self._validate_content(content)
        now = utc_now_iso()
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO memory (category, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (category, content, now, now),
            )
            memory_id = cursor.lastrowid
        return {"id": memory_id, "category": category, "content": content, "created_at": now, "updated_at": now}

    def list(self, search: str | None = None) -> list[dict[str, Any]]:
        query = "SELECT id, category, content, created_at, updated_at FROM memory"
        params: tuple = ()
        if search:
            query += " WHERE content LIKE ? OR category LIKE ?"
            params = (f"%{search}%", f"%{search}%")
        query += " ORDER BY id DESC"
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [
            {
                "id": row[0],
                "category": row[1],
                "content": row[2],
                "created_at": row[3],
                "updated_at": row[4],
            }
            for row in rows
        ]

    def update(self, memory_id: int, content: str) -> dict[str, Any] | None:
        self._validate_content(content)
        now = utc_now_iso()
        with self._connect() as conn:
            conn.execute("UPDATE memory SET content = ?, updated_at = ? WHERE id = ?", (content, now, memory_id))
            row = conn.execute(
                "SELECT id, category, content, created_at, updated_at FROM memory WHERE id = ?",
                (memory_id,),
            ).fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "category": row[1],
            "content": row[2],
            "created_at": row[3],
            "updated_at": row[4],
        }

    def delete(self, memory_id: int) -> bool:
        with self._connect() as conn:
            result = conn.execute("DELETE FROM memory WHERE id = ?", (memory_id,))
            return result.rowcount > 0
