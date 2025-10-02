# -*- coding: utf-8 -*-
from __future__ import annotations
import hashlib, hmac, time
from urllib.parse import urlencode

from apps.shared.config import SETTINGS

def _calc_telegram_hash(data: dict) -> str:
    """Telegram Login Widget hash hisoblash."""
    # 1) sign data (keys sorted, join with \n)
    pairs = [f"{k}={data[k]}" for k in sorted(data.keys()) if k != "hash"]
    data_check_string = "\n".join(pairs)

    # 2) secret key = sha256(bot_token)
    secret_key = hashlib.sha256(SETTINGS.USER_BOT_TOKEN.encode()).digest()
    # 3) HMAC-SHA256
    return hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

def verify_telegram_login(query: dict, max_age: int = 86400) -> dict | None:
    """
    Telegram Login Widget dan kelgan query stringni tekshiradi.
    True bo'lsa, foydalanuvchi ma'lumotlarini dict qilib qaytaradi.
    """
    if not SETTINGS.USER_BOT_TOKEN:
        return None

    if "hash" not in query or "id" not in query or "auth_date" not in query:
        return None

    # time check
    try:
        auth_date = int(query["auth_date"])
    except Exception:
        return None
    if int(time.time()) - auth_date > max_age:
        return None

    # calc hash
    expected = _calc_telegram_hash(query)
    if not hmac.compare_digest(expected, query["hash"]):
        return None

    # minimal user payload
    return {
        "telegram_id": int(query["id"]),
        "first_name": query.get("first_name", ""),
        "last_name": query.get("last_name", ""),
        "username": query.get("username", ""),
        "photo_url": query.get("photo_url", ""),
    }

def bot_deeplink(start_param: str = "") -> str:
    """@USER_BOT_USERNAME uchun deep-link yaratish."""
    uname = (getattr(SETTINGS, "USER_BOT_USERNAME", "") or "").lstrip("@")
    if not uname:
        return ""
    if start_param:
        return f"https://t.me/{uname}?start={start_param}"
    return f"https://t.me/{uname}"
