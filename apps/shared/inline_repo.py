# apps/shared/inline_repo.py
# ---------------------------------------------------------
# Helper repository for fetching inline block text by key + language
# Usage:
#   from apps.shared.inline_repo import InlineRepo, Lang
#   text = InlineRepo().get("news", Lang.UZ)
# ---------------------------------------------------------

import os
import sqlite3
from enum import Enum

DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "data", "app.db"))

class Lang(str, Enum):
    UZ = "uz"
    EN = "en"
    RU = "ru"

class InlineRepo:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_conn(self):
        return sqlite3.connect(self.db_path)

    def get(self, key: str, lang: Lang) -> str:
        col = {
            Lang.UZ: "body_uz",
            Lang.EN: "body_en",
            Lang.RU: "body_ru",
        }[lang]
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT {col} FROM inline_blocks WHERE "key"=?', (key,))
            row = cur.fetchone()
            return row[0] if row and row[0] else ""

    def title(self, key: str) -> str:
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute('SELECT title FROM inline_blocks WHERE "key"=?', (key,))
            row = cur.fetchone()
            return row[0] if row and row[0] else key
