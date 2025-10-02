# -*- coding: utf-8 -*-
import asyncio, logging, random
from decimal import Decimal

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from apps.shared.config import (
    SETTINGS, TARIFFS, OVERNIGHT_PC, CURRENCY,
    NEWS_LINK, PAYMENT_LINK, SUPPORT_USERNAME
)
from apps.shared.db import (
    init_db, get_session, User, InlineBlock, Payment,
    UserStatus, PaymentStatus, Plan, DeliveredFile
)
from apps.shared.keyboards import (
    main_menu, back_menu, language_keyboard,
    phone_share_kb, tariffs_kb, overnight_kb
)

logging.basicConfig(level=logging.INFO)

BOT = Bot(SETTINGS.USER_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp  = Dispatcher()

# ---------------- FSM: Registration ----------------
class Reg(StatesGroup):
    lang = State()
    full = State()
    phone = State()
    username = State()
    student = State()

def _get_lang(tg_id: int) -> str:
    s = get_session()
    try:
        u = s.query(User).filter(User.telegram_id == tg_id).one_or_none()
        return u.lang if (u and u.lang in ("uz","en","ru")) else "uz"
    finally: s.close()

def _ensure_user(tg_id: int, full_name: str | None, username: str | None) -> User:
    s = get_session()
    try:
        u = s.query(User).filter(User.telegram_id == tg_id).one_or_none()
        if not u:
            u = User(
                telegram_id=tg_id,
                first_last=full_name or "",
                username=username or "",
                lang="uz",
                status=UserStatus.pending,
            ); s.add(u); s.commit()
        return u
    finally: s.close()

def _inline_text(key: str, lang: str) -> str:
    s = get_session()
    try:
        b = s.query(InlineBlock).filter(InlineBlock.key == key).one_or_none()
        if not b: return "…"
        return {"uz": b.body_uz, "en": b.body_en, "ru": b.body_ru}.get(lang, b.body_en)
    finally: s.close()

# ---------------- Handlers ----------------
@dp.message(CommandStart())
async def on_start(m: Message, state: FSMContext):
    u = _ensure_user(m.from_user.id, m.from_user.full_name, m.from_user.username)
    lang = _get_lang(m.from_user.id)

    if u.first_last and u.phone and u.student_id:
        if u.status == UserStatus.approved:
            await m.answer(f"📍 <b>Asosiy menyu</b>", reply_markup=main_menu(lang))
        elif u.status == UserStatus.rejected:
            await m.answer("❌ Arizangiz rad etilgan. Support: "+SUPPORT_USERNAME)
        else:
            await m.answer("⏳ Profilingiz admin tasdiqlovida. /start orqali menyuga qaytishingiz mumkin.")
        return

    # til tanlashdan boshlaymiz
    await state.set_state(Reg.lang)
    await m.answer("🌐 Tilni tanlang / Choose language / Выберите язык", reply_markup=language_keyboard(lang))

@dp.callback_query(F.data.startswith("lang:set:"))
async def set_lang(cq: CallbackQuery, state: FSMContext):
    _,_,lang = cq.data.split(":")
    if lang not in ("uz","en","ru"): return await cq.answer("Unknown")
    # DB yangilaymiz
    s = get_session()
    try:
        u = s.query(User).filter(User.telegram_id == cq.from_user.id).one()
        u.lang = lang; s.commit()
    finally: s.close()

    await state.set_state(Reg.full)
    txt = {
        "uz":"✍️ Ism va familiyangizni kiriting:",
        "en":"✍️ Enter your first and last name:",
        "ru":"✍️ Введите имя и фамилию:",
    }[lang]
    await cq.message.edit_text(txt, reply_markup=back_menu(lang))
    await cq.answer()

@dp.callback_query(F.data == "nav:menu")
async def to_menu(cq: CallbackQuery, state: FSMContext):
    lang = _get_lang(cq.from_user.id)
    await state.clear()
    await cq.message.edit_text("📍 <b>Asosiy menyu</b>", reply_markup=main_menu(lang))
    await cq.answer()

@dp.callback_query(F.data == "nav:back")
async def go_back(cq: CallbackQuery, state: FSMContext):
    st = await state.get_state()
    lang = _get_lang(cq.from_user.id)
    if st == Reg.full.state:
        await cq.message.edit_text("🌐 Til / Language / Язык", reply_markup=language_keyboard(lang))
    elif st == Reg.phone.state:
        await state.set_state(Reg.full)
        await cq.message.edit_text({"uz":"✍️ Ismingiz?","en":"✍️ Your full name?","ru":"✍️ Имя Фамилия?"}[lang], reply_markup=back_menu(lang))
    elif st == Reg.username.state:
        await state.set_state(Reg.phone)
        await cq.message.edit_text({"uz":"📲 Telefon raqamingizni yuboring","en":"📲 Share your phone","ru":"📲 Отправьте номер"}[lang], reply_markup=back_menu(lang))
    elif st == Reg.student.state:
        await state.set_state(Reg.username)
        await cq.message.edit_text({"uz":"🔗 @username (bo‘lsa)","en":"🔗 @username (if any)","ru":"🔗 @username (если есть)"}[lang], reply_markup=back_menu(lang))
    else:
        await to_menu(cq, state)

# --- Reg steps
@dp.message(Reg.full)
async def reg_full(m: Message, state: FSMContext):
    lang = _get_lang(m.from_user.id)
    s = get_session()
    try:
        u = s.query(User).filter(User.telegram_id == m.from_user.id).one()
        u.first_last = (m.text or "").strip()
        s.commit()
    finally: s.close()

    await state.set_state(Reg.phone)
    await m.answer({"uz":"📲 Raqamni ulashing","en":"📲 Share phone number","ru":"📲 Поделитесь номером"}[lang],
                   reply_markup=phone_share_kb(lang))

@dp.message(Reg.phone, F.contact)
async def reg_phone_contact(m: Message, state: FSMContext):
    lang = _get_lang(m.from_user.id)
    phone = m.contact.phone_number
    s = get_session()
    try:
        u = s.query(User).filter(User.telegram_id == m.from_user.id).one()
        u.phone = phone; s.commit()
    finally: s.close()
    await state.set_state(Reg.username)
    await m.answer({"uz":"🔗 @username (bo‘lsa) yozing","en":"🔗 Enter @username (if any)","ru":"🔗 Введите @username (если есть)"}[lang],
                   reply_markup=back_menu(lang))

@dp.message(Reg.phone)
async def reg_phone_text(m: Message, state: FSMContext):
    # Agar qo'lda yozsa ham qabul qilamiz
    await reg_phone_contact(m, state)

@dp.message(Reg.username)
async def reg_username(m: Message, state: FSMContext):
    lang = _get_lang(m.from_user.id)
    un = (m.text or "").strip().lstrip("@")
    s = get_session()
    try:
        u = s.query(User).filter(User.telegram_id == m.from_user.id).one()
        u.username = un; s.commit()
    finally: s.close()
    await state.set_state(Reg.student)
    await m.answer({"uz":"🆔 Student ID ni kiriting","en":"🆔 Enter Student ID","ru":"🆔 Введите Student ID"}[lang],
                   reply_markup=back_menu(lang))

@dp.message(Reg.student)
async def reg_student(m: Message, state: FSMContext):
    lang = _get_lang(m.from_user.id)
    sid = (m.text or "").strip()
    s = get_session()
    try:
        u = s.query(User).filter(User.telegram_id == m.from_user.id).one()
        u.student_id = sid
        u.status = UserStatus.pending
        s.commit()
        user_db_id = u.id
    finally: s.close()

    await state.clear()
    await m.answer("✅ Ro‘yxatdan o‘tish yakunlandi!\n⏳ Admin 5 soat ichida ko‘rib chiqadi.",
                   reply_markup=back_menu(lang))

    # Admin'ga xabar
    try:
        await BOT.send_message(
            SETTINGS.ADMIN_TG_ID,
            f"🆕 Yangi user (#ID {user_db_id})\n"
            f"TG: {m.from_user.id} @{(m.from_user.username or '-')}\n"
            f"Ism: {m.from_user.full_name}\n"
            f"Tel: {sid}\n"
            f"Approve/Reject pastda.",
            reply_markup=approve_reject_markup(user_db_id)
        )
    except Exception:
        pass

def approve_reject_markup(user_db_id: int):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Approve", callback_data=f"adm:approve:{user_db_id}"),
        InlineKeyboardButton(text="❌ Reject",  callback_data=f"adm:reject:{user_db_id}"),
    ]])

# --- Menu router
@dp.callback_query(F.data.startswith("menu:"))
async def open_menu(cq: CallbackQuery, state: FSMContext):
    lang = _get_lang(cq.from_user.id)
    key = cq.data.split(":")[1]

    if key == "news":
        txt = f"📰 Yangiliklar kanali: {NEWS_LINK}"
        await cq.message.edit_text(txt, reply_markup=back_menu(lang))
    elif key == "mot":
        msgs = [
            "Bugungi kichik qadam — ertangi katta natija. Davom et! 🚀",
            "Har sahifa seni maqsadga yaqinlashtiradi. 📖",
            "Qiyinchilik — kuch beradi. Sabrlilik bilan! 💪",
        ]
        await cq.message.edit_text(random.choice(msgs), reply_markup=back_menu(lang))
    elif key == "rules":
        await cq.message.edit_text(_inline_text("rules", lang), reply_markup=back_menu(lang))
    elif key == "payment":
        txt = (f"💳 To‘lov: {PAYMENT_LINK}\n\n"
               f"Tarifni tanlang (keyin Overnight tanlaysiz):")
        await cq.message.edit_text(txt, reply_markup=tariffs_kb(lang))
    elif key == "qa":
        kb = {
            "inline_keyboard":[
                [{"text":"🧩 Biz qanday servicemiz?","callback_data":"qa:service"}],
                [{"text":"🔎 Resurslar qayerdan?","callback_data":"qa:resources"}],
                [{"text":"💰 Narxlar?","callback_data":"qa:price"}],
                [{"text":"🎯 Maqsad?","callback_data":"qa:goal"}],
                back_menu(lang).inline_keyboard[0]
            ]
        }
        await cq.message.edit_text("❓ Savol-Javob", reply_markup=kb)
    elif key == "tasks":
        s = get_session()
        try:
            u = s.query(User).filter(User.telegram_id == cq.from_user.id).one()
            files = s.query(DeliveredFile).filter(DeliveredFile.user_id==u.id).order_by(DeliveredFile.id.desc()).all()
        finally: s.close()
        if not files:
            await cq.message.edit_text("📥 Hozircha fayl yo‘q.", reply_markup=back_menu(lang)); return
        await cq.message.edit_text("📦 Fayllaringiz quyida:", reply_markup=back_menu(lang))
        for f in files:
            try:
                if f.file_type == "photo":
                    await BOT.send_photo(cq.from_user.id, f.file_id, caption=f.caption or "")
                else:
                    await BOT.send_document(cq.from_user.id, f.file_id, caption=f.caption or "")
            except Exception: pass
    elif key == "profile":
        s = get_session()
        try:
            u = s.query(User).filter(User.telegram_id == cq.from_user.id).one()
        finally: s.close()
        txt = (f"👤 <b>Profil</b>\n"
               f"Ism: {u.first_last or '-'}\n"
               f"Username: @{u.username or '-'}\n"
               f"Tel: {u.phone or '-'}\n"
               f"Student ID: {u.student_id or '-'}\n"
               f"Holat: {u.status.value}")
        await cq.message.edit_text(txt, reply_markup=back_menu(lang))
    elif key == "settings":
        await cq.message.edit_text(
            f"⚙️ Sozlamalar\n🌐 Tilni o‘zgartirish\n🆘 Support: {SUPPORT_USERNAME}",
            reply_markup=language_keyboard(lang)
        )

# --- Q&A javoblari
@dp.callback_query(F.data.startswith("qa:"))
async def qa_answers(cq: CallbackQuery):
    lang = _get_lang(cq.from_user.id)
    m = {
        "service":"🎓 Talabalarga assignment/presentation va ilmiy yordam beramiz.",
        "resources":"📚 Rasmiy darsliklar, maqolalar va ochiq bazalar; manbalar ko‘rsatiladi.",
        "price":"💵 Standard 350k, Premium 450k, Diamond 600k (+ Overnight 30%).",
        "goal":"🎯 Tez, xavfsiz va sifatli natija.",
    }[cq.data.split(":")[1]]
    await cq.message.edit_text(m, reply_markup=back_menu(lang))

# --- Payment tanlash
@dp.callback_query(F.data.startswith("pay:"))
async def choose_plan(cq: CallbackQuery, state: FSMContext):
    plan = cq.data.split(":")[1]  # standard/premium/diamond
    lang = _get_lang(cq.from_user.id)
    await state.update_data(plan=plan)
    await cq.message.edit_text(f"✅ {plan.title()} tanlandi.\nOvernight rejimini yoqasizmi?",
                               reply_markup=overnight_kb(lang))

@dp.callback_query(F.data.startswith("pay_ov:"))
async def choose_ov(cq: CallbackQuery, state: FSMContext):
    ov = int(cq.data.split(":")[1])
    data = await state.get_data()
    plan = data.get("plan","standard")
    base = TARIFFS[plan]
    amount = base + (base * OVERNIGHT_PC // 100 if ov else 0)

    # DB yozamiz
    s = get_session()
    try:
        u = s.query(User).filter(User.telegram_id == cq.from_user.id).one()
        p = Payment(
            user_id=u.id, plan=Plan(plan), overnight=bool(ov),
            amount=Decimal(amount), currency=CURRENCY,
            status=PaymentStatus.pending
        )
        s.add(p); s.commit()
    finally: s.close()

    lang = _get_lang(cq.from_user.id)
    await cq.message.edit_text(
        f"💳 Yakuniy summa: <b>{amount:,} {CURRENCY}</b>\n\n"
        f"To‘lov: {PAYMENT_LINK}\n\n"
        f"🧾 Kvitansiyani shu chatga yuboring (PDF/rasm).",
        reply_markup=back_menu(lang)
    )

# --- Receipt qabul qilish
@dp.message(F.document | F.photo)
async def on_receipt(m: Message):
    lang = _get_lang(m.from_user.id)
    file_id, file_name = ("","")

    if m.document:
        file_id = m.document.file_id
        file_name = m.document.file_name or "receipt.pdf"
    elif m.photo:
        file_id = m.photo[-1].file_id
        file_name = "receipt.jpg"

    if not file_id:
        return

    s = get_session()
    try:
        u = s.query(User).filter(User.telegram_id == m.from_user.id).one()
        p = (s.query(Payment)
               .filter(Payment.user_id==u.id, Payment.status==PaymentStatus.pending)
               .order_by(Payment.id.desc()).first())
        if p:
            p.receipt_file_id = file_id
            p.receipt_file_name = file_name
            s.commit()
            ok = True
        else:
            ok = False
    finally: s.close()

    if ok:
        await m.answer("✅ Kvitansiya qabul qilindi. Admin tasdiqlaguncha kuting.")
        # Admin'ga uzatamiz
        try:
            await BOT.send_document(
                SETTINGS.ADMIN_TG_ID, file_id,
                caption=f"🧾 Receipt from user {m.from_user.id}"
            )
        except Exception: pass
    else:
        await m.answer("ℹ️ Kutilayotgan to‘lov topilmadi. Avval tarifni tanlang.")

async def main():
    init_db()
    await dp.start_polling(BOT, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
