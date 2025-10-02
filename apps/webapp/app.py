# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from apps.shared.config import SETTINGS
from apps.shared.db import init_db, get_session
from apps.shared.models import InlineBlock, User, Payment  # re-export works
from .auth import verify_telegram_login, bot_deeplink

# --- App init ---------------------------------------------------------------
init_db()
app = FastAPI(title="UniHero Web")

app.add_middleware(SessionMiddleware, secret_key=SETTINGS.SECRET_KEY, same_site="lax")

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# --- Dependencies -----------------------------------------------------------
def db():
    s = get_session()
    try:
        yield s
    finally:
        s.close()

def current_user(request: Request, s=Depends(db)) -> Optional[User]:
    uid = request.session.get("uid")
    if not uid:
        return None
    return s.query(User).get(uid)

# --- Routes -----------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request, user: Optional[User] = Depends(current_user)):
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {
        "request": request,
        "tg_bot_username": (getattr(SETTINGS, "USER_BOT_USERNAME", "") or "").lstrip("@"),
    })

@app.get("/auth/telegram", response_class=HTMLResponse)
def auth_telegram(request: Request, **query):
    """
    Telegram Login Widget callback (GET).
    Browser -> /auth/telegram?id=...&first_name=...&hash=...
    """
    data = verify_telegram_login(query)
    if not data:
        raise HTTPException(status_code=400, detail="Telegram login failed")

    s = next(db())  # quick session
    user = s.query(User).filter(User.telegram_id == data["telegram_id"]).one_or_none()
    if not user:
        user = User(
            telegram_id=data["telegram_id"],
            full_name=f"{data.get('first_name','')} {data.get('last_name','')}".strip(),
            username=data.get("username") or "",
            lang="uz",
        )
        s.add(user); s.commit()
    else:
        # keep profile fresh
        user.full_name = user.full_name or f"{data.get('first_name','')} {data.get('last_name','')}".strip()
        if data.get("username"):
            user.username = data["username"]
        s.commit()

    request.session["uid"] = user.id
    return RedirectResponse(url="/dashboard", status_code=302)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, s=Depends(db), user: Optional[User] = Depends(current_user)):
    if not user:
        return RedirectResponse(url="/", status_code=302)

    blocks = (
        s.query(InlineBlock)
         .filter(InlineBlock.key.in_(["news", "rules", "payments", "tariffs", "settings", "sem1", "sem2"]))
         .all()
    )
    # payments list (oxirgi 10 ta)
    payments = (
        s.query(Payment).filter(Payment.user_id == user.id)
         .order_by(Payment.id.desc()).limit(10).all()
    )

    # deep-link (botga bog‘lash)
    deeplink = bot_deeplink(start_param=f"web{user.id}")

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "blocks": blocks,
        "payments": payments,
        "deeplink": deeplink,
        "now": datetime.now(),
    })

@app.post("/lang")
def set_lang(request: Request, lang: str = Form(...), s=Depends(db), user: Optional[User] = Depends(current_user)):
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if lang not in ("uz", "en", "ru"):
        raise HTTPException(status_code=400, detail="Lang invalid")
    u = s.query(User).get(user.id)
    u.lang = lang
    s.commit()
    return RedirectResponse(url="/dashboard", status_code=303)
