# -*- coding: utf-8 -*-
import os, re
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

_TOKEN_RE = re.compile(r"^\d{6,12}:[A-Za-z0-9_-]{30,}$")

def _clean(v: str | None) -> str:
    return (v or "").strip().strip('"').strip("'")

def _get_token(name: str) -> str:
    v = _clean(os.getenv(name))
    # Web-app-only bo'lsa token bo'sh qolishi mumkin
    if not v:
        return ""
    if not _TOKEN_RE.match(v):
        raise SystemExit(f"[CONFIG] {name} invalid. Fix it in .env")
    return v

@dataclass(frozen=True)
class Settings:
    # Bots
    ADMIN_BOT_TOKEN: str = _get_token("ADMIN_BOT_TOKEN")
    USER_BOT_TOKEN:  str = _get_token("USER_BOT_TOKEN")

    # DB
    DATABASE_URL:    str = _clean(os.getenv("DATABASE_URL") or "sqlite:///./unihero.db")

    # Admin
    ADMIN_TG_ID:     int = int(_clean(os.getenv("ADMIN_TG_ID") or "0"))

    # Web (kelajak uchun)
    ADMIN_USERNAME:  str = _clean(os.getenv("ADMIN_USER") or "admin")
    ADMIN_PASSWORD:  str = _clean(os.getenv("ADMIN_PASS") or "adminpanel@2025!")
    SECRET_KEY:      str = _clean(os.getenv("SECRET_KEY") or "dev-secret")

    @property
    def DB_URL(self) -> str:  # backward compat
        return self.DATABASE_URL

SETTINGS = Settings()

# Tariflar va doimiylar
TARIFFS = {
    "standard": 350_000,
    "premium":  450_000,
    "diamond":  600_000,
}
OVERNIGHT_PC = 30  # %
CURRENCY = "UZS"

NEWS_LINK = "https://t.me/UniHero_news"
PAYMENT_LINK = "https://tirikchilik.uz/unihero"
SUPPORT_USERNAME = "@Unihero_admin"
