from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


FORBIDDEN_MEMORY_TERMS = {"password", "token", "secret", "private key"}


@dataclass
class MemoryStore:
    db_path: str = "raghuvir.db"

    def __post_init__(self) -> None:
        self._ensure_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _ensure_db(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add_memory(self, category: str, content: str) -> int:
        lowered = content.lower()
        if any(term in lowered for term in FORBIDDEN_MEMORY_TERMS):
            raise ValueError("Secrets are not allowed in memory.")
        with self._connect() as conn:
            cur = conn.execute("INSERT INTO memories(category, content) VALUES(?, ?)", (category, content))
            return int(cur.lastrowid)

    def list_memory(self, query: str | None = None) -> list[dict]:
        with self._connect() as conn:
            if query:
                rows = conn.execute(
                    "SELECT id, category, content, created_at FROM memories WHERE content LIKE ? ORDER BY id DESC",
                    (f"%{query}%",),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT id, category, content, created_at FROM memories ORDER BY id DESC"
                ).fetchall()
        return [
            {"id": row[0], "category": row[1], "content": row[2], "created_at": row[3]} for row in rows
        ]

    def delete_memory(self, memory_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            return cur.rowcount > 0
