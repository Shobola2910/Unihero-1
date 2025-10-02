# -*- coding: utf-8 -*-
"""
Simple i18n helper.
Usage:
    from apps.shared.locales import tr, TXT

    lang = "uz"
    title = tr(lang, "menu.title")
    btn   = tr(lang, "buttons.back")
"""

from __future__ import annotations

# You can freely edit/extend these strings.
TXT = {
    "uz": {
        "app.name": "UniHero",
        # ---------- Buttons ----------
        "buttons.menu": "🏠 Menu",
        "buttons.back": "⬅️ Orqaga",
        "buttons.lang": "🌐 Til",
        "buttons.support": "🆘 Aloqa",
        "buttons.share_phone": "📲 Raqamni ulashish",
        "buttons.tariff.standard": "Standard — 350 000 so‘m",
        "buttons.tariff.premium":  "Premium — 450 000 so‘m",
        "buttons.tariff.diamond":  "Diamond — 600 000 so‘m",
        "buttons.overnight.on":  "⚡ Overnight (+30%)",
        "buttons.overnight.off": "⏳ Oddiy muddat",

        # ---------- Menu (2x4) ----------
        "menu.title": "Asosiy menyu",
        "menu.news": "📰 Yangiliklar",
        "menu.mot":  "💡 Motivatsiya",
        "menu.rules":"📜 Qoidalar",
        "menu.pay":  "💳 To‘lov",
        "menu.qa":   "❓ Q&A",
        "menu.tasks":"📥 Topshiriqni olish",
        "menu.profile":"👤 Profil",
        "menu.settings":"⚙️ Sozlamalar",

        # ---------- Registration ----------
        "reg.choose_lang": "🌐 Tilni tanlang / Choose language / Выберите язык",
        "reg.ask_full": "✍️ Ism va familiyangizni kiriting:",
        "reg.ask_phone": "📲 Telefon raqamingizni yuboring (tugma orqali ulashing yoki yozing):",
        "reg.ask_username": "🔗 Telegram @username (bo‘lsa) yozing:",
        "reg.ask_student": "🆔 Student ID ni kiriting:",
        "reg.done": "✅ Ro‘yxatdan o‘tish yakunlandi! Admin 5 soat ichida ko‘rib chiqadi.",
        "reg.pending": "⏳ Profilingiz admin tasdiqlovida. /start orqali menyuga qaytishingiz mumkin.",
        "reg.rejected": "❌ Afsus, arizangiz rad etildi. Qo‘llab-quvvatlash: {support}",
        "reg.approved": "🎉 Tabriklaymiz! Siz tasdiqlandingiz. /start ni bosing.",

        # ---------- Sections ----------
        "section.news": "📰 Yangiliklar kanali: {link}",
        "section.mot.examples": [
            "Bugungi kichik qadam — ertangi katta natija. Davom et! 🚀",
            "Har sahifa seni maqsadga yaqinlashtiradi. 📖",
            "Qiyinchilik — kuch beradi. Sabrlilik bilan! 💪",
        ],
        "section.rules": (
            "📜 Qoidalar\n"
            "1) Topshiriqlarni halol va muddatida bajaring.\n"
            "2) Shaxsiy ma’lumotni oshkor etmang.\n"
            "3) Ishni taqdim etishda “@UniHero_BOT Team” deb ayting.\n"
            "4) Turnitin/AI-detektor/plagiat natijalari uchun kafolat yo‘q.\n"
            "✨ UniHero — For Students, By Students."
        ),
        "section.payment.intro": "💳 To‘lov havolasi: {link}\nTarifni tanlang (keyin Overnight +30% ni tanlaysiz).",
        "section.payment.final": "💳 Yakuniy summa: <b>{amount:,} {currency}</b>\nTo‘lov: {link}\n🧾 Kvitansiyani shu chatga yuboring (PDF/rasm).",
        "section.qa.title": "❓ Savol-Javob",
        "section.qa.items": [
            ("🧩 Biz qanday servicemiz?", "🎓 Talabalarga assignment/presentation va ilmiy yordam beramiz."),
            ("🔎 Resurslar qayerdan?",  "📚 Rasmiy darsliklar, maqolalar va ochiq bazalar; manbalar ko‘rsatiladi."),
            ("💰 Narxlar?",            "💵 Standard 350k, Premium 450k, Diamond 600k (+ Overnight 30%)."),
            ("🎯 Maqsad?",             "⚡ Tez, xavfsiz va sifatli natija."),
        ],
        "section.tasks.none": "📥 Hozircha fayl yo‘q. Tayyor bo‘lganda shu bo‘limga tushadi.",
        "section.profile.fmt": (
            "👤 <b>Profil</b>\n"
            "Ism: {full}\n"
            "Username: @{user}\n"
            "Tel: {phone}\n"
            "Student ID: {sid}\n"
            "Holat: {status}"
        ),
        "section.settings": "⚙️ Sozlamalar\n🌐 Tilni o‘zgartirish • 🆘 Support: {support}",

        # ---------- Receipts / payments ----------
        "receipt.ask": "🧾 Kvitansiyani yuboring (PDF/JPG/PNG).",
        "receipt.ok":  "✅ Kvitansiya qabul qilindi. Admin tasdiqlaguncha kuting.",
        "receipt.none": "ℹ️ Kutilayotgan to‘lov topilmadi. Avval tarifni tanlang.",
    },

    "en": {
        "app.name": "UniHero",
        "buttons.menu": "🏠 Menu",
        "buttons.back": "⬅️ Back",
        "buttons.lang": "🌐 Language",
        "buttons.support": "🆘 Support",
        "buttons.share_phone": "📲 Share phone number",
        "buttons.tariff.standard": "Standard — 350,000 so'm",
        "buttons.tariff.premium":  "Premium — 450,000 so'm",
        "buttons.tariff.diamond":  "Diamond — 600,000 so'm",
        "buttons.overnight.on":  "⚡ Overnight (+30%)",
        "buttons.overnight.off": "⏳ Normal",

        "menu.title": "Main menu",
        "menu.news": "📰 News",
        "menu.mot":  "💡 Motivation",
        "menu.rules":"📜 Rules",
        "menu.pay":  "💳 Payment",
        "menu.qa":   "❓ Q&A",
        "menu.tasks":"📥 Get assignment",
        "menu.profile":"👤 Profile",
        "menu.settings":"⚙️ Settings",

        "reg.choose_lang": "🌐 Choose language / Til / Язык",
        "reg.ask_full": "✍️ Enter your first and last name:",
        "reg.ask_phone": "📲 Share your phone number (button or type):",
        "reg.ask_username": "🔗 Telegram @username (if any):",
        "reg.ask_student": "🆔 Enter Student ID:",
        "reg.done": "✅ Registration completed! Admin will review within 5 hours.",
        "reg.pending": "⏳ Waiting for admin approval. You can /start to return.",
        "reg.rejected": "❌ Sorry, your request was rejected. Support: {support}",
        "reg.approved": "🎉 Approved! Press /start to open the menu.",

        "section.news": "📰 News channel: {link}",
        "section.mot.examples": [
            "Small steps today lead to big wins tomorrow. Keep going! 🚀",
            "Every page brings you closer to your goal. 📖",
            "Struggles forge strength. Stay patient! 💪",
        ],
        "section.rules": (
            "📜 Rules\n"
            "1) Complete tasks honestly and on time.\n"
            "2) Never disclose personal data.\n"
            "3) Present work as “@UniHero_BOT Team”.\n"
            "4) No guarantee for Turnitin/AI-detector/plagiarism results.\n"
            "✨ UniHero — For Students, By Students."
        ),
        "section.payment.intro": "💳 Pay here: {link}\nChoose a plan (then decide Overnight +30%).",
        "section.payment.final": "💳 Final amount: <b>{amount:,} {currency}</b>\nPayment: {link}\n🧾 Send the receipt in this chat (PDF/image).",
        "section.qa.title": "❓ Q&A",
        "section.qa.items": [
            ("🧩 What service is this?","🎓 Academic help for students: assignments, presentations and guidance."),
            ("🔎 Where are resources from?","📚 Official textbooks, papers and reputable open sources (cited)."),
            ("💰 Pricing?","💵 Standard 350k, Premium 450k, Diamond 600k (+30% Overnight)."),
            ("🎯 Purpose?","⚡ Fast, safe, and high-quality outcomes."),
        ],
        "section.tasks.none": "📥 No files yet. You'll see them here once ready.",
        "section.profile.fmt": (
            "👤 <b>Profile</b>\n"
            "Name: {full}\n"
            "Username: @{user}\n"
            "Phone: {phone}\n"
            "Student ID: {sid}\n"
            "Status: {status}"
        ),
        "section.settings": "⚙️ Settings\n🌐 Change language • 🆘 Support: {support}",

        "receipt.ask": "🧾 Please upload the receipt (PDF/JPG/PNG).",
        "receipt.ok":  "✅ Receipt received. Wait for admin approval.",
        "receipt.none":"ℹ️ No pending payment found. Pick a plan first.",
    },

    "ru": {
        "app.name": "UniHero",
        "buttons.menu": "🏠 Меню",
        "buttons.back": "⬅️ Назад",
        "buttons.lang": "🌐 Язык",
        "buttons.support": "🆘 Поддержка",
        "buttons.share_phone": "📲 Поделиться номером",
        "buttons.tariff.standard": "Standard — 350 000 сум",
        "buttons.tariff.premium":  "Premium — 450 000 сум",
        "buttons.tariff.diamond":  "Diamond — 600 000 сум",
        "buttons.overnight.on":  "⚡ Overnight (+30%)",
        "buttons.overnight.off": "⏳ Обычный срок",

        "menu.title": "Главное меню",
        "menu.news": "📰 Новости",
        "menu.mot":  "💡 Мотивация",
        "menu.rules":"📜 Правила",
        "menu.pay":  "💳 Оплата",
        "menu.qa":   "❓ Вопрос-Ответ",
        "menu.tasks":"📥 Получить задание",
        "menu.profile":"👤 Профиль",
        "menu.settings":"⚙️ Настройки",

        "reg.choose_lang": "🌐 Выберите язык / Til / Language",
        "reg.ask_full": "✍️ Введите имя и фамилию:",
        "reg.ask_phone": "📲 Отправьте номер телефона (кнопка или текст):",
        "reg.ask_username": "🔗 Telegram @username (если есть):",
        "reg.ask_student": "🆔 Введите Student ID:",
        "reg.done": "✅ Регистрация завершена! Админ проверит в течение 5 часов.",
        "reg.pending": "⏳ Ожидается подтверждение администратора. /start — вернуться.",
        "reg.rejected": "❌ Заявка отклонена. Поддержка: {support}",
        "reg.approved": "🎉 Одобрено! Нажмите /start, чтобы открыть меню.",

        "section.news": "📰 Канал новостей: {link}",
        "section.mot.examples": [
            "Маленькие шаги сегодня — большие победы завтра. Вперёд! 🚀",
            "Каждая страница приближает к цели. 📖",
            "Трудности закаляют. Терпения! 💪",
        ],
        "section.rules": (
            "📜 Правила\n"
            "1) Выполняйте задания честно и в срок.\n"
            "2) Не раскрывайте личные данные.\n"
            "3) Представляйте работу как «@UniHero_BOT Team».\n"
            "4) Нет гарантий по Turnitin/детекторам ИИ/плагиату.\n"
            "✨ UniHero — For Students, By Students."
        ),
        "section.payment.intro": "💳 Оплата: {link}\nВыберите тариф (затем — Overnight +30%).",
        "section.payment.final": "💳 Итоговая сумма: <b>{amount:,} {currency}</b>\nОплата: {link}\n🧾 Отправьте квитанцию (PDF/изображение).",
        "section.qa.title": "❓ Вопрос-Ответ",
        "section.qa.items": [
            ("🧩 Что это за сервис?","🎓 Академическая помощь студентам: задания, презентации, консультации."),
            ("🔎 Откуда ресурсы?","📚 Учебники, научные статьи и проверенные открытые источники (с указанием)."),
            ("💰 Цены?","💵 Standard 350k, Premium 450k, Diamond 600k (+30% Overnight)."),
            ("🎯 Зачем бот?","⚡ Быстро, безопасно и качественно."),
        ],
        "section.tasks.none": "📥 Файлов пока нет. Готовые появятся здесь.",
        "section.profile.fmt": (
            "👤 <b>Профиль</b>\n"
            "Имя: {full}\n"
            "Username: @{user}\n"
            "Телефон: {phone}\n"
            "Student ID: {sid}\n"
            "Статус: {status}"
        ),
        "section.settings": "⚙️ Настройки\n🌐 Сменить язык • 🆘 Поддержка: {support}",

        "receipt.ask": "🧾 Загрузите квитанцию (PDF/JPG/PNG).",
        "receipt.ok":  "✅ Квитанция получена. Ожидайте подтверждения.",
        "receipt.none":"ℹ️ Не найден ожидаемый платёж. Сначала выберите тариф.",
    },
}

# ---- helper -----------------------------------------------------------
def tr(lang: str, path: str, **fmt) -> str:
    """
    Nested-dict getter with dotted path.
    Example: tr("uz", "menu.title") -> "Asosiy menyu"
    """
    lang = (lang if lang in TXT else "uz")
    node = TXT[lang]
    for part in path.split("."):
        node = node[part]
    if isinstance(node, str):
        return node.format(**fmt)
    return node  # for lists/tuples (e.g., motivation examples, qa items)
