# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.database.db_payments import Paymentsx
from tgbot.database.db_settings import Settingsx
from tgbot.utils.const_functions import ikb


################################################################################
#################################### ПРОЧЕЕ ####################################
# Удаление сообщения
def close_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("❌ Закрыть", data="close_this"),
    )

    return keyboard.as_markup()


# Рассылка
def mail_confirm_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Отправить", data="confirm_mail:yes"),
        ikb("❌ Отменить", data="confirm_mail:not")
    )

    return keyboard.as_markup()


# Поиск профиля пользователя
def profile_search_finl(user_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💰 Изменить баланс", data=f"admin_user_balance_set:{user_id}"),
        ikb("💰 Выдать баланс", data=f"admin_user_balance_add:{user_id}")
    ).row(
        ikb("🎁 Покупки", data=f"admin_user_purchases:{user_id}"),
        ikb("💌 Отправить СМС", data=f"admin_user_message:{user_id}")
    ).row(
        ikb("🔄 Обновить", data=f"admin_user_refresh:{user_id}")
    )

    return keyboard.as_markup()


# Возвращение к профилю пользователя
def profile_search_return_finl(user_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("❌ Отменить", data=f"admin_user_refresh:{user_id}"),
    )

    return keyboard.as_markup()


################################################################################
############################## ПЛАТЕЖНЫЕ СИСТЕМЫ ###############################
# Способы пополнения
def payment_method_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_payments = Paymentsx.get()

    status_qiwi_kb = ikb("✅", data="payment_method:QIWI:False")
    status_yoomoney_kb = ikb("✅", data="payment_method:Yoomoney:False")
    status_cryptobot_kb = ikb("✅", data="payment_method:CryptoBot:False")

    if get_payments.way_qiwi == "False":
        status_qiwi_kb = ikb("❌", data="payment_method:QIWI:True")
    if get_payments.way_yoomoney == "False":
        status_yoomoney_kb = ikb("❌", data="payment_method:Yoomoney:True")
    if get_payments.way_cryptobot == "False":
        status_cryptobot_kb = ikb("❌", data="payment_method:CryptoBot:True")

    keyboard.row(
        ikb("🥝 QIWI", url="https://vk.cc/csUUYy"), status_qiwi_kb
    ).row(
        ikb("🔮 ЮMoney", url="https://vk.cc/csUUXt"), status_yoomoney_kb
    ).row(
        ikb("💎 CryptoBot", url="https://t.me/CryptoBot"), status_cryptobot_kb
    )

    return keyboard.as_markup()


# Управление ЮMoney
def payment_yoomoney_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🔮 Баланс 💰", data="payment_yoomoney_balance"),
    ).row(
        ikb("🔮 Проверить ♻️", data="payment_yoomoney_check"),
    ).row(
        ikb("🔮 Изменить 🖍", data="payment_yoomoney_edit"),
    )

    return keyboard.as_markup()


# Управление QIWI
def payment_qiwi_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🥝 Баланс 💰", data="payment_qiwi_balance"),
    ).row(
        ikb("🥝 Проверить ♻️", data="payment_qiwi_check"),
    ).row(
        ikb("🥝 Изменить 🖍", data="payment_qiwi_edit"),
    )

    return keyboard.as_markup()


# Кнопки статистики
def statistics_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("📥 Экспорт пользователей", data="admin_export_users"),
    )

    return keyboard.as_markup()


################################################################################
################################## НАСТРОЙКИ ###################################
# Кнопки с настройками
def settings_open_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_settings = Settingsx.get()

    # Поддержка
    if get_settings.misc_support == "None":
        support_kb = ikb("Не установлена ❌", data="settings_edit_support")
    else:
        support_kb = ikb(f"@{get_settings.misc_support} ✅", data="settings_edit_support")

    # FAQ
    if get_settings.misc_faq == "None":
        faq_kb = ikb("Не установлено ❌", data="settings_edit_faq")
    else:
        faq_kb = ikb(f"{get_settings.misc_faq[:15]}... ✅", data="settings_edit_faq")

    keyboard.row(
        ikb("❔ FAQ", data="..."), faq_kb
    ).row(
        ikb("☎️ Поддержка", data="..."), support_kb
    )

    return keyboard.as_markup()


# Выключатели
def turn_open_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_settings = Settingsx.get()

    status_work_kb = ikb("Включены ✅", data="turn_work:False")
    status_buy_kb = ikb("Включены ✅", data="turn_buy:False")
    status_refill_kb = ikb("Включены ✅", data="turn_pay:False")
    status_stars_buy_kb = ikb("Включена ✅", data="turn_stars_buy:False")

    if get_settings.status_buy == "False":
        status_buy_kb = ikb("Выключены ❌", data="turn_buy:True")
    if get_settings.status_work == "False":
        status_work_kb = ikb("Выключены ❌", data="turn_work:True")
    if get_settings.status_refill == "False":
        status_refill_kb = ikb("Выключены ❌", data="turn_pay:True")
    if get_settings.status_stars_buy == "False":
        status_stars_buy_kb = ikb("Выключена ❌", data="turn_stars_buy:True")

    keyboard.row(
        ikb("⛔ Тех. работы", data="..."), status_work_kb
    ).row(
        ikb("💰 Пополнения", data="..."), status_refill_kb
    ).row(
        ikb("🎁 Покупки", data="..."), status_buy_kb
    ).row(
        ikb("⭐ Купить звезды", data="..."), status_stars_buy_kb
    )

    return keyboard.as_markup()


# Наценка на звезды
def stars_markup_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_settings = Settingsx.get()

    keyboard.row(
        ikb("⭐ Текущая наценка", data="..."), 
        ikb(f"{get_settings.stars_markup}%", data="stars_markup_current")
    ).row(
        ikb("🖍 Изменить наценку", data="stars_markup_edit")
    ).row(
        ikb("❌ Закрыть", data="close_this")
    )

    return keyboard.as_markup()
