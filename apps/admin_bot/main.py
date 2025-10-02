# -*- coding: utf-8 -*-
import asyncio, logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from apps.shared.config import SETTINGS
from apps.shared.db import (
    init_db, get_session, User, Payment, DeliveredFile,
    UserStatus, PaymentStatus
)

logging.basicConfig(level=logging.INFO)
BOT = Bot(SETTINGS.ADMIN_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp  = Dispatcher()

ADMIN_ID = SETTINGS.ADMIN_TG_ID

def only_admin(handler):
    async def wrap(event, *a, **kw):
        uid = getattr(event.from_user, "id", 0)
        if uid != ADMIN_ID:
            msg = "⛔️ Ruxsat yo‘q."
            if isinstance(event, Message): await event.answer(msg)
            else: await event.answer(msg, show_alert=True)
            return
        return await handler(event, *a, **kw)
    return wrap

@dp.message(Command("start"))
@only_admin
async def start_cmd(m: Message):
    s = get_session()
    try:
        up = s.query(User).filter(User.status==UserStatus.pending).count()
        pp = s.query(Payment).filter(Payment.status==PaymentStatus.pending).count()
    finally: s.close()
    await m.answer(
        "👋 <b>UniHero Admin</b>\n"
        f"Pending users: <b>{up}</b>\nPending payments: <b>{pp}</b>\n\n"
        "/pending — kutayotgan userlar\n"
        "/pay — kutayotgan to‘lovlar\n"
        "/payapprove <id> — to‘lovni tasdiqlash\n"
        "/payreject <id> — to‘lovni rad etish\n"
        "Fayl yuborish: hujjat/rasmni caption bilan: /sendto <tg_id> [matn]"
    )

@dp.message(Command("pending"))
@only_admin
async def list_pending(m: Message):
    s = get_session()
    try:
        users = s.query(User).filter(User.status==UserStatus.pending).order_by(User.id.asc()).all()
    finally: s.close()
    if not users:
        return await m.answer("✅ Pending users yo‘q.")
    for u in users[:50]:
        kb = {"inline_keyboard":[
            [{"text":"✅ Approve","callback_data":f"adm:approve:{u.id}"},
             {"text":"❌ Reject","callback_data":f"adm:reject:{u.id}"}]
        ]}
        await m.answer(f"#{u.id} — {u.first_last} (@{u.username or '-'})\nTG: {u.telegram_id}", reply_markup=kb)

@dp.callback_query(F.data.startswith("adm:approve:"))
@only_admin
async def approve_user(cq: CallbackQuery):
    uid = int(cq.data.split(":")[-1])
    s = get_session()
    try:
        u = s.query(User).get(uid)
        if not u: return await cq.answer("Topilmadi")
        u.status = UserStatus.approved; s.commit()
        tg = u.telegram_id
    finally: s.close()
    await cq.message.edit_text(f"✅ Approved: #{uid}")
    try:
        await BOT.send_message(tg, "🎉 Tabriklaymiz! Siz tasdiqlandingiz. /start ni bosing.")
    except Exception: pass

@dp.callback_query(F.data.startswith("adm:reject:"))
@only_admin
async def reject_user(cq: CallbackQuery):
    uid = int(cq.data.split(":")[-1])
    s = get_session()
    try:
        u = s.query(User).get(uid)
        if not u: return await cq.answer("Topilmadi")
        u.status = UserStatus.rejected; s.commit()
        tg = u.telegram_id
    finally: s.close()
    await cq.message.edit_text(f"❌ Rejected: #{uid}")
    try:
        await BOT.send_message(tg, "❌ Afsus, arizangiz rad etildi.")
    except Exception: pass

@dp.message(Command("pay"))
@only_admin
async def list_payments(m: Message):
    s = get_session()
    try:
        pays = s.query(Payment).filter(Payment.status==PaymentStatus.pending).all()
    finally: s.close()
    if not pays: return await m.answer("✅ Pending payments yo‘q.")
    for p in pays[:30]:
        await m.answer(f"Payment #{p.id} | user_id={p.user_id} | {p.amount} {p.currency}\n"
                       f"overnight={bool(p.overnight)} | plan={getattr(p.plan,'value',p.plan)}")

@dp.message(Command("payapprove"))
@only_admin
async def payapprove(m: Message):
    parts = m.text.split()
    if len(parts)<2: return await m.answer("Foydalanish: /payapprove <payment_id>")
    pid = int(parts[1])
    s = get_session()
    try:
        p = s.query(Payment).get(pid)
        if not p: return await m.answer("Topilmadi.")
        p.status = PaymentStatus.approved; s.commit()
        tg = s.query(User).get(p.user_id).telegram_id
    finally: s.close()
    await m.answer(f"✅ Payment #{pid} approved")
    try: await BOT.send_message(tg, "💳 To‘lov tasdiqlandi. Rahmat!")
    except Exception: pass

@dp.message(Command("payreject"))
@only_admin
async def payreject(m: Message):
    parts = m.text.split()
    if len(parts)<2: return await m.answer("Foydalanish: /payreject <payment_id>")
    pid = int(parts[1])
    s = get_session()
    try:
        p = s.query(Payment).get(pid)
        if not p: return await m.answer("Topilmadi.")
        p.status = PaymentStatus.rejected; s.commit()
        tg = s.query(User).get(p.user_id).telegram_id
    finally: s.close()
    await m.answer(f"❌ Payment #{pid} rejected")
    try: await BOT.send_message(tg, "💳 To‘lov rad etildi. Iltimos, qayta urinib ko‘ring.")
    except Exception: pass

# Admin fayl yuboradi: caption = /sendto <tg_id> [matn]
@dp.message(F.document | F.photo)
@only_admin
async def admin_send_file(m: Message):
    if not m.caption or not m.caption.startswith("/sendto"):
        return await m.answer("Caption: /sendto <tg_id> [matn]")
    parts = m.caption.split(maxsplit=2)
    if len(parts) < 2: return await m.answer("Foydalanish: /sendto <tg_id> [matn]")
    tg_id = int(parts[1]); note = parts[2] if len(parts)>2 else ""

    file_id, ftype = ("","document")
    if m.document:
        file_id, ftype = m.document.file_id, "document"
    elif m.photo:
        file_id, ftype = m.photo[-1].file_id, "photo"

    s = get_session()
    try:
        u = s.query(User).filter(User.telegram_id == tg_id).one_or_none()
        if not u: return await m.answer("User topilmadi.")
        s.add(DeliveredFile(user_id=u.id, file_id=file_id, file_type=ftype, caption=note))
        s.commit()
    finally: s.close()

    # Userga yetkazamiz
    try:
        if ftype == "photo":
            await BOT.send_photo(tg_id, file_id, caption=note or "📥 Topshiriq fayli")
        else:
            await BOT.send_document(tg_id, file_id, caption=note or "📥 Topshiriq fayli")
        await m.answer("Yuborildi ✅")
    except Exception:
        await m.answer("Userga yuborib bo‘lmadi (TG ID ni tekshiring).")

async def main():
    init_db()
    await dp.start_polling(BOT, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
