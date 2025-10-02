# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from apps.shared.config import SETTINGS
from apps.shared.db import (
    init_db, get_session, User, Payment, InlineBlock,
    UserStatus, PaymentStatus
)

app = FastAPI(title="UniHero Admin")
app.add_middleware(SessionMiddleware, secret_key=SETTINGS.SECRET_KEY)
app.mount("/static", StaticFiles(directory="apps/webapp/static"), name="static")


# ---- helpers ----
def _auth(req: Request) -> bool:
    return bool(req.session.get("auth", False))

def _guard(req: Request) -> Optional[RedirectResponse]:
    if not _auth(req):
        return RedirectResponse("/admin", status_code=302)
    return None

def _layout(page_title: str, content_html: str, back_href: str = "", menu_href: str = "/admin/dashboard") -> HTMLResponse:
    # mini animated UI + back/menu
    back_btn = f'<a class="btn ghost" href="{back_href or menu_href}">⬅ Back</a>' if (back_href or menu_href) else ""
    menu_btn = f'<a class="btn outline" href="{menu_href}">🏠 Menu</a>'
    html = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{page_title} · UniHero</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <div class="topbar">
    <div class="brand">UniHero · Admin</div>
    <div class="topnav">
      {back_btn}
      {menu_btn}
      <a class="btn ghost logout" href="/admin/logout">🔒 Logout</a>
    </div>
  </div>
  <div class="page fade">
    {content_html}
  </div>
</body>
</html>
"""
    return HTMLResponse(html)


# ---- routes ----
@app.on_event("startup")
def _startup():
    init_db()


@app.get("/admin", response_class=HTMLResponse)
def login_page(req: Request):
    if _auth(req):
        return RedirectResponse("/admin/dashboard", status_code=302)
    html = f"""
<div class="auth-wrap">
  <div class="card auth-card fade">
    <h2 class="card-title">Sign in</h2>
    <form method="post" action="/admin/login" class="form">
      <label class="label">Username</label>
      <input class="input" type="text" name="username" placeholder="admin" required>
      <label class="label">Password</label>
      <input class="input" type="password" name="password" placeholder="••••••••" required>
      <button class="btn primary w100" type="submit">Sign in</button>
    </form>
    <div class="alert" style="margin-top:10px;color:#a6b0cf">
      Default: <b>{SETTINGS.ADMIN_USERNAME}</b> / <b>{SETTINGS.ADMIN_PASSWORD}</b>
    </div>
  </div>
</div>
"""
    return _layout("Login", html, back_href="", menu_href="/admin")


@app.post("/admin/login")
def login(req: Request, username: str = Form(...), password: str = Form(...)):
    if username == SETTINGS.ADMIN_USERNAME and password == SETTINGS.ADMIN_PASSWORD:
        req.session["auth"] = True
        return RedirectResponse("/admin/dashboard", status_code=302)
    return _layout("Login failed", """
<div class="auth-wrap">
  <div class="card auth-card">
    <div class="alert alert-error">Invalid credentials. Please try again.</div>
    <a class="btn outline w100" href="/admin">Back to login</a>
  </div>
</div>
""", back_href="/admin", menu_href="/admin")


@app.get("/admin/logout")
def logout(req: Request):
    req.session.clear()
    return RedirectResponse("/admin", status_code=302)


@app.get("/admin/dashboard", response_class=HTMLResponse)
def dashboard(req: Request):
    if (r := _guard(req)):
        return r
    s = get_session()
    try:
        users_total = s.query(User).count()
        users_pending = s.query(User).filter(User.status == UserStatus.pending).count()
        pay_pending = s.query(Payment).filter(Payment.status == PaymentStatus.pending).count()
        pay_approved = s.query(Payment).filter(Payment.status == PaymentStatus.approved).count()
    finally:
        s.close()

    html = f"""
<h2 class="page-title">Dashboard</h2>
<div class="grid">
  <div class="card stat">
    <div class="stat-title">Users</div>
    <div class="stat-value">{users_total}</div>
    <a class="stat-link" href="/admin/users">View users →</a>
  </div>
  <div class="card stat">
    <div class="stat-title">Pending users</div>
    <div class="stat-value">{users_pending}</div>
    <a class="stat-link" href="/admin/users">Manage →</a>
  </div>
  <div class="card stat">
    <div class="stat-title">Pending payments</div>
    <div class="stat-value">{pay_pending}</div>
    <a class="stat-link" href="/admin/payments">Review →</a>
  </div>
  <div class="card stat">
    <div class="stat-title">Approved payments</div>
    <div class="stat-value">{pay_approved}</div>
    <a class="stat-link" href="/admin/payments">Open →</a>
  </div>
</div>

<div class="grid wide">
  <a class="card panel link" href="/admin/inlines">
    <div class="panel-title">🧩 Inline Blocks</div>
    <div class="panel-sub">Create & edit contents for News / Motivation / Rules</div>
  </a>
  <div class="card panel">
    <div class="panel-title">Tips</div>
    <div class="panel-sub">Use inline blocks to feed the bots text per language.</div>
    <ul style="margin:0; padding-left:20px;">
      <li>Keys: <b>news</b>, <b>motivation</b>, <b>rules</b> (or custom)</li>
      <li>Each has EN/UZ/RU bodies</li>
    </ul>
  </div>
</div>
"""
    return _layout("Dashboard", html, back_href="/admin", menu_href="/admin/dashboard")


@app.get("/admin/users", response_class=HTMLResponse)
def users_list(req: Request):
    if (r := _guard(req)):
        return r
    s = get_session()
    try:
        users = s.query(User).order_by(User.created_at.desc()).limit(100).all()
    finally:
        s.close()

    rows = "".join(
        f"<div class='tr'><div>#{u.id}</div><div>{u.first_last or '-'}</div>"
        f"<div>@{u.username or '-'}</div><div>{u.lang}</div><div>{u.status.value}</div>"
        f"<div>{u.created_at.strftime('%Y-%m-%d')}</div></div>"
        for u in users
    ) or "<div class='empty'>No users.</div>"

    html = f"""
<h2 class="page-title">Users</h2>
<div class="table">
  <div class="tr head"><div>ID</div><div>Name</div><div>Username</div><div>Lang</div><div>Status</div><div>Created</div></div>
  {rows}
</div>
"""
    return _layout("Users", html, back_href="/admin/dashboard", menu_href="/admin/dashboard")


@app.get("/admin/payments", response_class=HTMLResponse)
def payments_list(req: Request):
    if (r := _guard(req)):
        return r
    s = get_session()
    try:
        pays = s.query(Payment).order_by(Payment.created_at.desc()).limit(100).all()
    finally:
        s.close()

    def _plan(p):
        return getattr(p.plan, "value", "-") if p.plan else "-"

    rows = "".join(
        f"<div class='tr'><div>#{p.id}</div><div>U#{p.user_id}</div>"
        f"<div>{_plan(p)}</div><div>{p.amount} {p.currency}</div><div>{p.status.value}</div>"
        f"<div>{p.created_at.strftime('%Y-%m-%d')}</div></div>"
        for p in pays
    ) or "<div class='empty'>No payments.</div>"

    html = f"""
<h2 class="page-title">Payments</h2>
<div class="table">
  <div class="tr head"><div>ID</div><div>User</div><div>Plan</div><div>Amount</div><div>Status</div><div>Created</div></div>
  {rows}
</div>
"""
    return _layout("Payments", html, back_href="/admin/dashboard", menu_href="/admin/dashboard")


@app.get("/admin/inlines", response_class=HTMLResponse)
def inlines_list(req: Request):
    if (r := _guard(req)):
        return r
    s = get_session()
    try:
        blocks = s.query(InlineBlock).order_by(InlineBlock.key.asc()).all()
    finally:
        s.close()

    items = "".join(
        f"<tr><td><span class='badge'>{b.key}</span></td><td>{b.title}</td>"
        f"<td style='text-align:right'><a class='btn outline' href='/admin/inlines/{b.key}'>Edit</a></td></tr>"
        for b in blocks
    ) or "<tr><td colspan='3' class='empty'>No inline blocks yet.</td></tr>"

    html = f"""
<h2 class="page-title">Inline Blocks</h2>
<div class="card">
  <div class="inline" style="justify-content:space-between">
    <div class="panel-title">Manage inline content</div>
    <a class="btn primary" href="/admin/inlines/new">＋ New</a>
  </div>
  <table class="tbl" style="margin-top:10px">
    <thead><tr><th>Key</th><th>Title</th><th style="text-align:right">Actions</th></tr></thead>
    <tbody>{items}</tbody>
  </table>
</div>
"""
    return _layout("Inlines", html, back_href="/admin/dashboard", menu_href="/admin/dashboard")


@app.get("/admin/inlines/new", response_class=HTMLResponse)
def inlines_new(req: Request):
    if (r := _guard(req)):
        return r
    html = """
<div class="card">
  <div class="panel-title">New inline block</div>
  <form method="post" action="/admin/inlines/new" class="form">
    <label class="label">Key (unique)</label>
    <input class="input" type="text" name="key" placeholder="news / motivation / rules ..." required>
    <label class="label">Title</label>
    <input class="input" type="text" name="title" placeholder="Block title">
    <div class="grid wide">
      <div>
        <label class="label">Body (EN)</label>
        <textarea class="input" name="body_en" placeholder="English content"></textarea>
      </div>
      <div>
        <label class="label">Body (UZ)</label>
        <textarea class="input" name="body_uz" placeholder="Uzbek content"></textarea>
      </div>
    </div>
    <label class="label">Body (RU)</label>
    <textarea class="input" name="body_ru" placeholder="Russian content"></textarea>
    <div style="display:flex; gap:8px; margin-top:10px">
      <button class="btn primary" type="submit">Save</button>
      <a class="btn ghost" href="/admin/inlines">Cancel</a>
    </div>
  </form>
</div>
"""
    return _layout("New inline", html, back_href="/admin/inlines", menu_href="/admin/dashboard")


@app.post("/admin/inlines/new")
def inlines_new_post(
    req: Request,
    key: str = Form(...),
    title: str = Form(""),
    body_en: str = Form(""),
    body_uz: str = Form(""),
    body_ru: str = Form(""),
):
    if (r := _guard(req)):
        return r
    s = get_session()
    try:
        exists = s.query(InlineBlock).filter(InlineBlock.key == key).one_or_none()
        if exists:
            return _layout("Inline exists", f"""
<div class="card">
  <div class="alert">Inline with key '<b>{key}</b>' already exists.</div>
  <div style="display:flex; gap:8px">
    <a class="btn outline" href="/admin/inlines/{key}">Open</a>
    <a class="btn ghost" href="/admin/inlines">Back</a>
  </div>
</div>
""", back_href="/admin/inlines", menu_href="/admin/dashboard")

        b = InlineBlock(
            key=key, title=title,
            body_en=body_en, body_uz=body_uz, body_ru=body_ru,
            created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        )
        s.add(b); s.commit()
    finally:
        s.close()
    return RedirectResponse(f"/admin/inlines/{key}", status_code=302)


@app.get("/admin/inlines/{key}", response_class=HTMLResponse)
def inlines_edit(req: Request, key: str):
    if (r := _guard(req)):
        return r
    s = get_session()
    try:
        b = s.query(InlineBlock).filter(InlineBlock.key == key).one_or_none()
    finally:
        s.close()
    if not b:
        return _layout("Not found", f"""
<div class="card"><div class="alert">Inline '{key}' not found.</div>
<a class="btn outline" href="/admin/inlines">Back</a></div>
""", back_href="/admin/inlines", menu_href="/admin/dashboard")

    html = f"""
<div class="card">
  <div class="panel-title">Edit: {b.key}</div>
  <form method="post" action="/admin/inlines/{b.key}" class="form">
    <label class="label">Title</label>
    <input class="input" type="text" name="title" value="{(b.title or '').replace('"','&quot;')}">
    <div class="grid wide">
      <div>
        <label class="label">Body (EN)</label>
        <textarea class="input" name="body_en">{(b.body_en or '')}</textarea>
      </div>
      <div>
        <label class="label">Body (UZ)</label>
        <textarea class="input" name="body_uz">{(b.body_uz or '')}</textarea>
      </div>
    </div>
    <label class="label">Body (RU)</label>
    <textarea class="input" name="body_ru">{(b.body_ru or '')}</textarea>

    <div class="muted" style="margin-top:8px">Updated at: {b.updated_at}</div>
    <div style="display:flex; gap:8px; margin-top:10px">
      <button class="btn primary" type="submit">Save</button>
      <a class="btn ghost" href="/admin/inlines">Back</a>
    </div>
  </form>
</div>
"""
    return _layout(f"Edit {b.key}", html, back_href="/admin/inlines", menu_href="/admin/dashboard")


@app.post("/admin/inlines/{key}")
def inlines_edit_post(
    req: Request, key: str,
    title: str = Form(""),
    body_en: str = Form(""),
    body_uz: str = Form(""),
    body_ru: str = Form(""),
):
    if (r := _guard(req)):
        return r
    s = get_session()
    try:
        b = s.query(InlineBlock).filter(InlineBlock.key == key).one_or_none()
        if not b:
            s.close()
            return RedirectResponse("/admin/inlines", status_code=302)
        b.title = title
        b.body_en = body_en
        b.body_uz = body_uz
        b.body_ru = body_ru
        b.updated_at = datetime.utcnow()
        s.commit()
    finally:
        s.close()
    return RedirectResponse(f"/admin/inlines/{key}", status_code=302)
