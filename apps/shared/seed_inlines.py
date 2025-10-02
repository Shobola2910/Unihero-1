# -*- coding: utf-8 -*-
"""
Inline bloklarni UZ/EN/RU bo'yicha seed qiladi.
Ishga tushirish:  python -m apps.shared.seed_inlines
"""

from datetime import datetime, timezone
from textwrap import dedent
from contextlib import contextmanager

from apps.shared.db import init_db, get_session, InlineBlock

@contextmanager
def session_scope():
    s = get_session()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()

def upsert(key: str, title: str, uz: str, en: str, ru: str):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    with session_scope() as s:
        b = s.query(InlineBlock).filter(InlineBlock.key == key).one_or_none()
        if b is None:
            b = InlineBlock(
                key=key, title=title,
                # ⚠️ Legacy lang ustuni uchun default qiymat ham ketadi
                lang="uz",
                body_uz=uz, body_en=en, body_ru=ru,
                created_at=now, updated_at=now
            )
            s.add(b)
        else:
            b.title    = title
            b.body_uz  = uz
            b.body_en  = en
            b.body_ru  = ru
            b.updated_at = now

def seed_core():
    # --- NEWS ----------------------------------------------------------
    news_uz = dedent("""\
        📢 Hey student!
        Endi siz eng so‘nggi yangiliklardan bevosita xabardor bo‘lasiz!
        UniHero News kanalimizda talabalarga oid barcha muhim voqealarni tezkor ulashamiz.
        Qo‘shiling va birinchi bo‘lib bilib oling! 🎓✨
        👉 UniHero – For Students, By Students 🎓
        🔗 https://t.me/UniHero_news
    """).strip()
    news_en = dedent("""\
        📢 Hey students!
        Stay updated with the latest news and events directly from our UniHero News channel.
        We share everything that matters to students — fast, clear, and useful! 💡🎓
        Join us now and never miss out!
        👉 UniHero – For Students, By Students 🎓
        🔗 https://t.me/UniHero_news
    """).strip()
    news_ru = dedent("""\
        📢 Эй, студент!
        Теперь все самые свежие новости для студентов — в UniHero News!
        Мы делимся только важным: события, объявления и полезные советы 🎓✨
        Подписывайтесь и будьте в курсе первым!
        👉 UniHero – For Students, By Students 🎓
        🔗 https://t.me/UniHero_news
    """).strip()
    upsert("news", "News / Yangiliklar / Новости", news_uz, news_en, news_ru)

    # --- RULES (o‘zgartirmadik) ---------------------------------------
    rules_uz = dedent("""\
        🇺🇿 O‘zbekcha Qoidalar 📜
        1️⃣ Agar siz ushbu servicedan foydalansangiz, biz bergan topshiriqlarni to‘liq va vijdonan bajarishingiz shart.
        2️⃣ Yozuvchi haqida (ismi, familiyasi yoki boshqa shaxsiy ma’lumotlari) bilsangiz ham, uni hech qayerda va hech kimga oshkor etmasligingiz kerak.
        3️⃣ Bizning xizmatlarimizni boshqalarga taqdim qilganingizda, “Bu odam qildi” demang. Faqatgina: @UniHero_BOT Team qildi deb ayting.
        4️⃣ Biz siz uchun qo‘limizdan kelgan barcha ishni qilamiz – hattoki undan ham ortig‘ini. Ammo Turnitin, AI detector yoki plagiat tekshiruvlari natijalari uchun javobgar emasmiz.
        ⚠️ Chunki biz bilamiz: Dehqon tarvuzni bor kuchi bilan parvarishlaydi. Ammo u so‘yilganda oqarib chiqsa yoki mazasi yoqmasa – bu dehqonning aybi emas.
        ✨ UniHero – For Students, By Students
    """).strip()
    rules_en = dedent("""\
        🇬🇧 English Rules 📜
        1️⃣ By using this service, you are expected to complete all assigned tasks fully and honestly.
        2️⃣ Even if you know the writer’s identity (name, surname, or any personal detail), you must never disclose it.
        3️⃣ When presenting our services to others, never say “this person did it.” Always say: @UniHero_BOT Team did it.
        4️⃣ We will do everything possible – even beyond that – for your benefit. However, we are not responsible for Turnitin, AI detector, or plagiarism results.
        ⚠️ Because we know: A farmer nurtures the watermelon with all his strength, but if it turns out pale or tasteless at home – it is not the farmer’s fault.
        ✨ UniHero – For Students, By Students
    """).strip()
    rules_ru = dedent("""\
        🇷🇺 Русский Правила 📜
        1️⃣ Если вы пользуетесь этим сервисом, вы обязаны выполнять все задания честно и полностью.
        2️⃣ Даже если вы знаете личность (имя, фамилию или любую личную информацию) автора, вы не имеете права её разглашать.
        3️⃣ Продвигая наши услуги, никогда не говорите: «этот человек сделал». Говорите только: @UniHero_BOT Team сделал(а).
        4️⃣ Мы сделаем всё возможное для вас – даже больше. Но мы не несем ответственности за результаты в Turnitin, AI-детекторах или проверках на плагиат.
        ⚠️ Потому что мы знаем: Фермер выращивает арбуз с заботой и усилиями, но если дома он окажется бледным или безвкусным – это не вина фермера.
        ✨ UniHero – For Students, By Students
    """).strip()
    upsert("rules", "Rules / Qoidalar / Правила", rules_uz, rules_en, rules_ru)

    # --- PAYMENTS (150–200 so‘z + privacy short) ----------------------
    pay_uz = dedent("""\
        💳 To‘lov — faqat karta orqali: tirikchilik.uz/unihero havolasida buyurtma raqami va summani tasdiqlang.
        To‘lovdan so‘ng kvitansiya (PDF yoki skrinshot)ni botga yuboring. Admin tasdiqlagach, ish boshlanadi.
        🔐 Privacy (qisqa): Ma’lumotlaringiz faqat xizmat ko‘rsatish uchun qayta ishlanadi. Uchinchi tomonga berilmaydi,
        xavfsiz saqlanadi va talab bo‘lmaganda o‘chirib boriladi. Savollar: @Unihero_admin
    """).strip()
    pay_en = dedent("""\
        💳 Payment — cards only: confirm the order ID and amount at tirikchilik.uz/unihero.
        After payment, send the receipt (PDF/screenshot) to the bot. Work starts once an admin verifies it.
        🔐 Privacy (short): Your data is processed solely to deliver the service, never shared with third parties,
        stored securely, and removed when no longer needed. Questions: @Unihero_admin
    """).strip()
    pay_ru = dedent("""\
        💳 Оплата — только картой: подтвердите номер заказа и сумму на tirikchilik.uz/unihero.
        После оплаты отправьте квитанцию (PDF/скрин) в бот. Работа начнётся после проверки админом.
        🔐 Конфиденциальность (кратко): Данные используются только для оказания услуги, не передаются третьим лицам,
        хранятся безопасно и удаляются при отсутствии необходимости. Вопросы: @Unihero_admin
    """).strip()
    upsert("payments", "Payments / To‘lov / Оплата", pay_uz, pay_en, pay_ru)

    # --- TARIFFS (+ overnight +30%) -----------------------------------
    tariffs_uz = dedent("""\
        🧩 Tariflar (o‘rtacha 7–10 kun)
        • Standard — 350 000 so‘m: faqat assignment.
        • Premium — 450 000 so‘m: assignment + presentation.
        • Diamond — 600 000 so‘m: assignment + presentation + darsliklarni tushuntirish + AI yordamida yuqori sifat.
        ⚡ Overnight (tez): tanlangan tarif narxiga +30%. To‘lov kvitansiyasi shart, tasdiqdan so‘ng ish boshlanadi.
    """).strip()
    tariffs_en = dedent("""\
        🧩 Plans (avg 7–10 days)
        • Standard — 350,000 UZS: assignment only.
        • Premium — 450,000 UZS: assignment + presentation.
        • Diamond — 600,000 UZS: assignment + presentation + concept explanations + high-quality AI help.
        ⚡ Overnight (rush): +30% on the selected plan. Work starts after receipt verification.
    """).strip()
    tariffs_ru = dedent("""\
        🧩 Тарифы (в среднем 7–10 дней)
        • Standard — 350 000 сум: только задание.
        • Premium — 450 000 сум: задание + презентация.
        • Diamond — 600 000 сум: задание + презентация + объяснения тем + помощь ИИ высокого качества.
        ⚡ Overnight (срочно): +30% к выбранному тарифу. Работа стартует после проверки квитанции.
    """).strip()
    upsert("tariffs", "Tariffs / Tariflar / Тарифы", tariffs_uz, tariffs_en, tariffs_ru)

    # --- SETTINGS / SUPPORT -------------------------------------------
    settings_uz = "⚙️ Sozlamalar: tilni o‘zgartiring (UZ/EN/RU). Support: @Unihero_admin"
    settings_en = "⚙️ Settings: change language (UZ/EN/RU). Support: @Unihero_admin"
    settings_ru = "⚙️ Настройки: смена языка (UZ/EN/RU). Поддержка: @Unihero_admin"
    upsert("settings", "Settings / Sozlamalar / Настройки", settings_uz, settings_en, settings_ru)

def main():
    init_db()
    seed_core()
    print(">> Seed OK")

if __name__ == "__main__":
    main()
