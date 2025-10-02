# apps/shared/texts.py
from random import choice

SUPPORT_HANDLE = "@Unihero_admin"
NEWS_CHANNEL = "https://t.me/UniHero_news"

REG_DONE = (
    "🎉 Ro'yxatga olish yakunlandi!\n"
    "Endi admin tasdiqlovini kuting.\n\n"
    "<i>P.S. Admin tasdiqlovi odatda 5 soat ichida bo‘ladi. "
    "/start tugmasini bosib menyuga qaytishingiz mumkin.</i>"
)

RULES = {
    "uz": (
        "📜 <b>Qoidalar</b>\n"
        "1) Xizmatdan foydalansangiz, topshiriqlarni vijdonan bajaring.\n"
        "2) Muallif(lar) haqidagi shaxsiy ma’lumotlarni oshkor qilmang.\n"
        "3) Xizmatni boshqalarga taqdim etganda: <b>@UniHero_BOT Team</b> deb ayting.\n"
        "4) Turnitin/AI-detector/plagiat natijalari uchun javobgar emasmiz.\n\n"
        "🌾 Dehqon tarvuzni mehr bilan parvarishlaydi, ammo u uyda mazasi bo‘lmasa — bu dehqon aybi emas."
    ),
    "en": (
        "📜 <b>Rules</b>\n"
        "1) Complete all tasks honestly and fully.\n"
        "2) Never disclose the writer’s identity or personal details.\n"
        "3) When referring to our service, say <b>@UniHero_BOT Team</b>.\n"
        "4) We are not responsible for Turnitin/AI-detector/plagiarism outcomes.\n\n"
        "🌾 A farmer nurtures the watermelon; if it tastes bland at home, it’s not the farmer’s fault."
    ),
    "ru": (
        "📜 <b>Правила</b>\n"
        "1) Выполняйте задания честно и полностью.\n"
        "2) Не разглашайте личность автора.\n"
        "3) Упоминая нас, говорите <b>@UniHero_BOT Team</b>.\n"
        "4) Мы не отвечаем за результаты Turnitin/AI-детекторов/плагиата.\n\n"
        "🌾 Фермер растит арбуз с заботой: если дома он безвкусный — это не вина фермера."
    ),
}

FAQ = {
    "uz": [
        ("Biz qanday servicemiz?", "🎯 Biz — talabalar uchun 'assignment/presentation' tayyorlashga yordam beruvchi jamoamiz. Sifat, muddat va maxfiylik — ustuvor."),
        ("Resurslar qayerdan olinadi?", "📚 Akademik bazalar, darsliklar, ochiq ma’lumotlar va ekspert tajribasidan foydalanamiz."),
        ("Assignmentlar nech pul?", "💳 Topshiriq turi va murakkabligiga qarab. <b>To‘lov</b> bo‘limidan tariflarni ko‘ring."),
        ("Botning maqsadi?", "🤖 Jarayonni soddalashtirish: buyurtma, fayl almashish, to‘lov va e’lonlar bir joyda."),
    ],
    "en": [
        ("What service is this?", "🎯 A student-focused team for assignments/presentations with quality, deadlines and privacy."),
        ("Where are resources from?", "📚 Academic databases, textbooks, open data and expert curation."),
        ("How much do assignments cost?", "💳 Depends on scope and complexity. See <b>Payment</b> for plans."),
        ("What’s the goal of the bot?", "🤖 Streamlined ordering, file sharing, payments and updates."),
    ],
    "ru": [
        ("Что это за сервис?", "🎯 Команда, помогающая со студенческими работами и презентациями."),
        ("Откуда ресурсы?", "📚 Академические базы, учебники, открытые источники и экспертиза."),
        ("Сколько стоит?", "💳 Зависит от объёма и сложности. См. раздел <b>Оплата</b>."),
        ("Цель бота?", "🤖 Упростить заказ, обмен файлами, оплату и уведомления."),
    ],
}

MOTIVATION = [
    "🌟 Har bir kichik qadam — katta natijaning boshlanishi.",
    "🚀 Knowledge compounds. Learn a little every day.",
    "🧠 Focus beats talent when talent doesn’t focus.",
    "⏱️ 25 daqiqa diqqat — 5 daqiqa tanaffus. Pomodoro sinab ko‘ring!",
    "🌿 Sabr + tartib = natija.",
]

PAYMENT_INTRO = {
    "uz": (
        "💳 <b>To‘lov</b>\n"
        "To‘lov faqat karta orqali amalga oshiriladi: <a href='https://tirikchilik.uz/unihero'>tirikchilik.uz/unihero</a>\n\n"
        "<b>Maxfiylik & siyosat:</b> ma’lumotlaringiz shaxsiy. Ishni faqat to‘lov tasdiqlangach boshlaymiz."
    ),
    "en": (
        "💳 <b>Payment</b>\n"
        "We accept card payments only: <a href='https://tirikchilik.uz/unihero'>tirikchilik.uz/unihero</a>\n\n"
        "<b>Privacy & policy:</b> your data stays private. Work starts after payment confirmation."
    ),
    "ru": (
        "💳 <b>Оплата</b>\n"
        "Оплата картой: <a href='https://tirikchilik.uz/unihero'>tirikchilik.uz/unihero</a>\n\n"
        "<b>Конфиденциальность:</b> данные приватны. Работа начинается после подтверждения оплаты."
    ),
}

TARIFFS = {
    "standard": "⭐ <b>Standard</b> — topshiriqni talablarga mos, ixcham va aniq yozib beramiz. 7–10 kun.",
    "premium": "🚀 <b>Premium</b> — assignment + professional presentation. Ko‘proq tahlil, vizual. 7–10 kun.",
    "diamond": "💎 <b>Diamond</b> — assignment + presentation + murakkab mavzularni onlayn tushuntirish; kuchli AI yordami. 7–10 kun.",
}

OVERNIGHT_NOTE = {
    "uz": "⚡ <b>Tezlashtirilgan</b> rejim ish narxiga ~30% qo‘shilishi mumkin.",
    "en": "⚡ <b>Overnight</b> may add ~30% to the price.",
    "ru": "⚡ <b>Срочно</b> — надбавка около 30%.",
}

def pick_motivation() -> str:
    return choice(MOTIVATION)
