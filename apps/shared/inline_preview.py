# apps/admin_bot/inline_preview.py
# ---------------------------------------------------------
# (Optional) Admin preview handler to quickly check blocks
# ---------------------------------------------------------

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from apps.shared.inline_repo import InlineRepo, Lang

router = Router()
repo = InlineRepo()

@router.message(Command("preview"))
async def preview(message: Message):
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Usage: /preview <key> <lang: uz|en|ru>")
        return
    key, lang = parts[1], parts[2]
    lmap = {"uz": Lang.UZ, "en": Lang.EN, "ru": Lang.RU}
    if lang not in lmap:
        await message.answer("Lang must be uz|en|ru")
        return
    text = repo.get(key, lmap[lang]) or "—"
    await message.answer(f"[{key} / {lang}]\n\n{text}", disable_web_page_preview=True)
