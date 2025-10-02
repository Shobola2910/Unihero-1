# -*- coding: utf-8 -*-
"""
SQLite uchun: jadval yo'q bo'lsa yaratadi, bor bo'lsa yetishmayotgan ustunlarni qo'shadi.
"""
import sqlalchemy as sa
from sqlalchemy import text
from .db import engine, Base, InlineBlock


def _column_exists(table: str, column: str) -> bool:
    with engine.connect() as conn:
        info = conn.execute(text(f'PRAGMA table_info("{table}")')).mappings().all()
        return any(row["name"] == column for row in info)


def ensure_schema():
    # Jadval yo'q bo'lsa - create_all bilan yaratamiz
    Base.metadata.create_all(bind=engine)

    # Yetishmayotgan ustunlar bo'lsa, SQLite uchun ALTER TABLE bilan qo'shamiz
    cols = {
        "body_uz": 'TEXT NOT NULL DEFAULT ""',
        "body_en": 'TEXT NOT NULL DEFAULT ""',
        "body_ru": 'TEXT NOT NULL DEFAULT ""',
        "title":   'VARCHAR(255) NOT NULL DEFAULT ""',
        "created_at": 'DATETIME',
        "updated_at": 'DATETIME'
    }

    with engine.begin() as conn:
        for col, ddl in cols.items():
            if not _column_exists("inline_blocks", col):
                conn.execute(text(f'ALTER TABLE inline_blocks ADD COLUMN {col} {ddl}'))


if __name__ == "__main__":
    ensure_schema()
    print(">> Schema ensured.")
