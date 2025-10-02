# apps/user_bot/inline_handlers.py
# ---------------------------------------------------------
# Example handlers to show how to display inline contents with
# 2x4 menu and proper Back/Menu behavior (no duplicates)
# ---------------------------------------------------------

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton
from apps.shared.keyboards import grid_2x4, with_nav, language_keyboard
from apps.shared.inline_repo import InlineRepo, Lang

router = Router()
repo = InlineRepo()

def get_lang(data: dict) -> str:
    # your session/user storage; replace with actual storage
    return data.get("lang", "uz")

def set_lang(data: dict, lang: str):
    data["lang"] = lang

@router.message(CommandStart())
async def start(message: Message, state):
    data = await state.get_data()
    lang = get_lang(data)
    kb = grid_2x4([
        InlineKeyboardButton("📰 News", callback_data="open:news"),
        InlineKeyboardButton("💡 Motivation", callback_data="open:motivation"),
        InlineKeyboardButton("📜 Rules", callback_data="open:rules"),
        InlineKeyboardButton("💳 Payments", callback_data="open:payments"),
        InlineKeyboardButton("🗂 Tariffs", callback_data="open:tariffs"),
        InlineKeyboardButton("⚙️ Settings", callback_data="open:settings"),
        InlineKeyboardButton("🌐 Language", callback_data="open:lang"),
        InlineKeyboardButton("ℹ️ About", callback_data="open:about"),
    ])
    kb = with_nav(kb, lang, back_cb="nav:noop", menu_cb="nav:menu")  # Back disabled on root
    await message.answer("🏠 Main Menu", reply_markup=kb)

@router.callback_query(F.data.startswith("nav:menu"))
async def on_menu(call: CallbackQuery, state):
    await start(call.message, state)

@router.callback_query(F.data.startswith("open:"))
async def open_block(call: CallbackQuery, state):
    key = call.data.split(":", 1)[1]
    data = await state.get_data()
    lang = get_lang(data)

    if key == "lang":
        await call.message.edit_text("🌐 Select language:", reply_markup=language_keyboard(lang))
        await call.answer()
        return
    if key == "about":
        text = {"uz": "✨ UniHero – For Students, By Students", "en": "✨ UniHero – For Students, By Students", "ru": "✨ UniHero – For Students, By Students"}[lang]
        kb = with_nav(grid_2x4([]), lang, back_cb="nav:back", menu_cb="nav:menu")
        await call.message.edit_text(text, reply_markup=kb)
        await call.answer()
        return

    # map lang
    lmap = {"uz": Lang.UZ, "en": Lang.EN, "ru": Lang.RU}
    body = repo.get(key, lmap[lang]) or "—"
    kb = with_nav(grid_2x4([]), lang, back_cb="nav:back", menu_cb="nav:menu")
    await call.message.edit_text(body, disable_web_page_preview=True, reply_markup=kb)
    await call.answer()

@router.callback_query(F.data == "nav:back")
async def on_back(call: CallbackQuery, state):
    # in a real app, use your own stack/history; here we go to menu
    await on_menu(call, state)

@router.callback_query(F.data.startswith("lang:"))
async def on_lang(call: CallbackQuery, state):
    lang = call.data.split(":", 1)[1]
    data = await state.get_data()
    set_lang(data, lang)
    await state.set_data(data)
    await call.message.edit_text("✅ Language updated.", reply_markup=language_keyboard(lang))
    await call.answer()
