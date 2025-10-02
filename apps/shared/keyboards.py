# -*- coding: utf-8 -*-
from __future__ import annotations
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

# ---------- Asosiy 2x4 menu ----------
def main_menu(lang: str) -> InlineKeyboardMarkup:
    # ko'rsatiladigan matnlar soddalashtirildi
    t = {
        "news": {"uz":"📰 Yangiliklar","en":"📰 News","ru":"📰 Новости"},
        "mot":  {"uz":"💡 Motivatsiya","en":"💡 Motivation","ru":"💡 Мотивация"},
        "rules":{"uz":"📜 Qoidalar","en":"📜 Rules","ru":"📜 Правила"},
        "pay":  {"uz":"💳 To‘lov","en":"💳 Payment","ru":"💳 Оплата"},
        "qa":   {"uz":"❓ Q&A","en":"❓ Q&A","ru":"❓ Вопрос-Ответ"},
        "tasks":{"uz":"📥 Topshiriq","en":"📥 Assignment","ru":"📥 Задание"},
        "prof": {"uz":"👤 Profil","en":"👤 Profile","ru":"👤 Профиль"},
        "set":  {"uz":"⚙️ Sozlamalar","en":"⚙️ Settings","ru":"⚙️ Настройки"},
    }
    rows = [
        [InlineKeyboardButton(text=t["news"][lang], callback_data="menu:news"),
         InlineKeyboardButton(text=t["mot"][lang],  callback_data="menu:mot")],
        [InlineKeyboardButton(text=t["rules"][lang],callback_data="menu:rules"),
         InlineKeyboardButton(text=t["pay"][lang],  callback_data="menu:payment")],
        [InlineKeyboardButton(text=t["qa"][lang],   callback_data="menu:qa"),
         InlineKeyboardButton(text=t["tasks"][lang],callback_data="menu:tasks")],
        [InlineKeyboardButton(text=t["prof"][lang], callback_data="menu:profile"),
         InlineKeyboardButton(text=t["set"][lang],  callback_data="menu:settings")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def back_menu(lang: str) -> InlineKeyboardMarkup:
    txt = {"uz":"⬅️ Orqaga","en":"⬅️ Back","ru":"⬅️ Назад"}
    home= {"uz":"🏠 Menu","en":"🏠 Menu","ru":"🏠 Меню"}
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=txt[lang], callback_data="nav:back"),
        InlineKeyboardButton(text=home[lang],callback_data="nav:menu"),
    ]])

# ---------- Language ----------
def language_keyboard(current: str) -> InlineKeyboardMarkup:
    rows = [[
        InlineKeyboardButton(text=f"🇺🇿 O‘zbekcha{' ✅' if current=='uz' else ''}", callback_data="lang:set:uz"),
        InlineKeyboardButton(text=f"🇬🇧 English{' ✅' if current=='en' else ''}",   callback_data="lang:set:en"),
        InlineKeyboardButton(text=f"🇷🇺 Русский{' ✅' if current=='ru' else ''}",   callback_data="lang:set:ru"),
    ], back_menu(current).inline_keyboard[0]]
    return InlineKeyboardMarkup(inline_keyboard=rows)

# ---------- Registration ----------
def phone_share_kb(lang: str) -> ReplyKeyboardMarkup:
    label = {"uz":"📲 Raqamni ulashish","en":"📲 Share phone","ru":"📲 Поделиться номером"}[lang]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=label, request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )

# ---------- Payment (tariffs + overnight) ----------
def tariffs_kb(lang: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="Standard — 350 000 so‘m", callback_data="pay:standard")],
        [InlineKeyboardButton(text="Premium — 450 000 so‘m",   callback_data="pay:premium")],
        [InlineKeyboardButton(text="Diamond — 600 000 so‘m",   callback_data="pay:diamond")],
        back_menu(lang).inline_keyboard[0],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def overnight_kb(lang: str) -> InlineKeyboardMarkup:
    rows = [[
        InlineKeyboardButton(text="⚡ Overnight (+30%)", callback_data="pay_ov:1"),
        InlineKeyboardButton(text="⏳ Oddiy muddat",      callback_data="pay_ov:0"),
    ], back_menu(lang).inline_keyboard[0]]
    return InlineKeyboardMarkup(inline_keyboard=rows)

# ---------- Admin ----------
def approve_reject_kb(user_db_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Approve", callback_data=f"adm:approve:{user_db_id}"),
        InlineKeyboardButton(text="❌ Reject",  callback_data=f"adm:reject:{user_db_id}"),
    ]])
