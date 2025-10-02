# apps/user_bot/motivations.py
# -*- coding: utf-8 -*-
import random

MOT = {
    "uz": [
        "📚 O‘qish — kelajakdagi eng kuchli quroling. Bugun mehnat qil, ertaga porla! 🚀",
        "💡 Orzudan voz kechma. Har sahifa seni maqsadinga yaqinlashtiradi! 📖",
        "🔥 Bugungi qiyinchilik — ertangi kuching. Sabr qil, natija keladi! 💪",
        "🌟 Kichik qadamlar — katta g‘alabalarga olib boradi. ✨",
        "🚪 Bilim eshik ochadi. O‘qishni to‘xtatma! 🔑",
        "⏳ Intizom — muvaffaqiyat kaliti. Hozirdan boshlang! 🚀",
        "💎 Hech kim o‘rningga o‘qimaydi. Bilim — shaxsiy boyliging! 📚",
        "🌍 Har bir kitob — yangi olam. O‘qishni sev! ✨",
        "📈 Kichik odatlar — katta natijalar. Har kuni oz-ozdan! 🌞",
        "🎓 Bilim — eng ishonchli investitsiya. 💡",
    ],
    "en": [
        "📚 Study is your strongest weapon. Work today, shine tomorrow! 🚀",
        "💡 Don’t give up on your dreams. Every page brings you closer! 📖",
        "🔥 Today’s struggle becomes tomorrow’s strength. Be patient! 💪",
        "🌟 Small steps lead to great wins. ✨",
        "🚪 Knowledge opens doors. Keep learning! 🔑",
        "⏳ Discipline is the key to success. Start now! 🚀",
        "💎 No one studies for you. Knowledge is your treasure! 📚",
        "🌍 Every book opens a new world. Read more! ✨",
        "📈 Small habits → big results. 🌞",
        "🎓 Education is an investment that never fails. 💡",
    ],
    "ru": [
        "📚 Учёба — твоё сильнейшее оружие. Трудись сегодня — сияй завтра! 🚀",
        "💡 Не сдавайся. Каждая страница приближает к цели! 📖",
        "🔥 Сегодняшняя борьба — завтрашняя сила. Терпение! 💪",
        "🌟 Маленькие шаги ведут к большим победам. ✨",
        "🚪 Знания открывают двери. Продолжай учиться! 🔑",
        "⏳ Дисциплина — ключ к успеху. Начни сейчас! 🚀",
        "💎 За тебя никто не выучит. Знания — твоё богатство! 📚",
        "🌍 Каждая книга — новый мир. Читай больше! ✨",
        "📈 Маленькие привычки → большие результаты. 🌞",
        "🎓 Образование — лучшая инвестиция. 💡",
    ],
}

_recent = {"uz": [], "en": [], "ru": []}
def pick_random(lang: str) -> str:
    pool = MOT.get(lang, MOT["en"])
    choice = random.choice(pool)
    # oddiy anti-repeat: oxirgi 3 tadan ko‘p takrorlanmasin
    r = _recent[lang]
    if choice in r and len(pool) > 3:
        return pick_random(lang)
    r.append(choice)
    if len(r) > 3: r.pop(0)
    return choice
