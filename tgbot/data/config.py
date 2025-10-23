# - *- coding: utf- 8 - *-
import configparser

from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_CONFIG = configparser.ConfigParser()
BOT_CONFIG.read("settings.ini")

# Образы и конфиги
BOT_TOKEN = BOT_CONFIG['settings']['token'].strip().replace(' ', '')  # Токен бота
BOT_TIMEZONE = "Europe/Moscow"  # Временная зона бота
BOT_SCHEDULER = AsyncIOScheduler(timezone=BOT_TIMEZONE)  # Образ шедулера
BOT_VERSION = 4.0  # Версия бота

# Пути к файлам
PATH_DATABASE = "tgbot/data/database.db"  # Путь к БД
PATH_LOGS = "tgbot/data/logs.log"  # Путь к Логам


# Получение администраторов бота
def get_admins() -> list[int]:
    read_admins = configparser.ConfigParser()
    read_admins.read("settings.ini")

    admins = read_admins['settings']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins: admins.remove("")
    while " " in admins: admins.remove(" ")
    while "\r" in admins: admins.remove("\r")
    while "\n" in admins: admins.remove("\n")

    admins = list(map(int, admins))

    return admins


# Получение ссылки на чат
def get_chat_url() -> str:
    read_config = configparser.ConfigParser()
    read_config.read("settings.ini")
    
    chat_url = read_config['settings'].get('chat_url', 'None').strip()
    
    if chat_url and chat_url != "None" and chat_url != "":
        return chat_url
    
    return None


# Получение ссылки на канал с бесплатными подарками
def get_free_gifts_url() -> str:
    read_config = configparser.ConfigParser()
    read_config.read("settings.ini")
    
    url = read_config['settings'].get('free_gifts_url', '').strip()
    
    if url and url != "None" and url != "":
        return url
    
    return None


# Получение ссылки на канал с играми
def get_games_url() -> str:
    read_config = configparser.ConfigParser()
    read_config.read("settings.ini")
    
    url = read_config['settings'].get('games_url', '').strip()
    
    if url and url != "None" and url != "":
        return url
    
    return None


# Получение списка обязательных каналов
def get_required_channels() -> list[int]:
    read_config = configparser.ConfigParser()
    read_config.read("settings.ini")
    
    channels = read_config['settings'].get('required_channels', '').strip().replace(" ", "")
    
    if not channels or channels == "None" or channels == "":
        return []
    
    if "," in channels:
        channels = channels.split(",")
    else:
        channels = [channels]
    
    while "" in channels: channels.remove("")
    while " " in channels: channels.remove(" ")
    while "\r" in channels: channels.remove("\r")
    while "\n" in channels: channels.remove("\n")
    
    channels = list(map(int, channels))
    
    return channels


# Получение описания
def get_desc() -> str:
    from tgbot.utils.const_functions import ded

    # УДАЛИШЬ ИЛИ ИЗМЕНИШЬ ССЫЛКИ НА ДОНАТ, КАНАЛ И ТЕМУ БОТА - КАСТРИРУЮ НАХУЙ <3

    return ded(f"""
        <b>♻️ Bot Version: <code>{BOT_VERSION}</code>
        👑 Bot posted @end_soft
        🍩 Donate to the author: <a href='https://yoomoney.ru/to/410012580032553'>Click me</a>
        🤖 Bot channel [NEWS | UPDATES]: <a href='https://t.me/DJIMBO_SHOP'>Click me</a>
        🔗 Topic Link: <a href='https://lolz.guru/threads/1888814'>Click me</a></b>
    """).strip()
