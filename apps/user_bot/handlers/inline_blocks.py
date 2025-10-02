# -*- coding: utf-8 -*-
from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton
from sqlalchemy.orm import Session
from apps.shared.db import SessionLocal, InlineBlock
from apps.shared.keyboards import grid2x4, back_menu_row

router = Router(name="inline_blocks")

def _get_block(key: str) -> InlineBlock | None:
    with SessionLocal() as s:
        return s.query(InlineBlock).filter(InlineBlock.key == key).one_or_none()

def _lang_text(block: InlineBlock, lang: str) -> str:
    if lang == "en":
        return block.body_en or block.body_uz
    if lang == "ru":
        return block.body_ru or block.body_uz
    return block.body_uz

@router.callback_query(F.data.startswith("open:"))
async def open_inline_block(cb: types.CallbackQuery):
    # data format: open:<key>:<lang>
    _, key, lang = (cb.data.split(":") + ["uz"])[:3]
    block = _get_block(key)
    if not block:
        await cb.answer("Topilmadi", show_alert=True)
        return

    text = _lang_text(block, lang)

    # Pastga universal Back/Menu
    kb = grid2x4([])  # shu sahifa uchun grid bo'sh bo'lishi mumkin
    kb.inline_keyboard += back_menu_row(lang)
    await cb.message.edit_text(text)
    await cb.message.edit_reply_markup(kb)
    await cb.answer()

@router.callback_query(F.data == "nav:menu")
async def go_menu(cb: types.CallbackQuery):
    # Asosiy menu (2x4) — tilga qarab tugmalar matni
    lang = "uz"
    if ":" in (cb.message.reply_markup.inline_keyboard[-1][0].callback_data or ""):
        # optional: agar tilni oldingi callbackdan ushlamoqchi bo'lsangiz
        pass

    t = {
        "uz": {
            "news": "📰 Yangiliklar",
            "mot": "💡 Motivatsiya",
            "rules": "📜 Qoidalar",
            "pay": "💳 To‘lov",
            "tariffs": "🧩 Tariflar",
            "settings": "⚙️ Sozlamalar",
        },
        "en": {
            "news": "📰 News",
            "mot": "💡 Motivation",
            "rules": "📜 Rules",
            "pay": "💳 Payments",
            "tariffs": "🧩 Plans",
            "settings": "⚙️ Settings",
        },
        "ru": {
            "news": "📰 Новости",
            "mot": "💡 Мотивация",
            "rules": "📜 Правила",
            "pay": "💳 Оплата",
            "tariffs": "🧩 Тарифы",
            "settings": "⚙️ Настройки",
        },
    }[lang]

    btns = [
        InlineKeyboardButton(text=t["news"], callback_data=f"open:news:{lang}"),
        InlineKeyboardButton(text=t["mot"], callback_data=f"open:motivation_01:{lang}"),
        InlineKeyboardButton(text=t["rules"], callback_data=f"open:rules:{lang}"),
        InlineKeyboardButton(text=t["pay"], callback_data=f"open:payments:{lang}"),
        InlineKeyboardButton(text=t["tariffs"], callback_data=f"open:tariffs:{lang}"),
        InlineKeyboardButton(text=t["settings"], callback_data=f"open:settings:{lang}"),
        # kerak bo'lsa qolgan 2 ta slotni boshqa bo'limlar bilan to'ldiring
    ]
    kb = grid2x4(btns)
    # Pastga ham Back/Menu bo'lishi shart emas — bu menu o'zi "root"
    await cb.message.edit_text("Asosiy menu")
    await cb.message.edit_reply_markup(kb)
    await cb.answer()

@router.callback_query(F.data == "nav:back")
async def go_back(cb: types.CallbackQuery):
    # Bir qadam orqaga — real loyihada stack saqlab yuriladi.
    # Soddalashtirilgan: menuga qaytaramiz.
    await go_menu(cb)
