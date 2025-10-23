# - *- coding: utf- 8 - *-
from aiogram import BaseMiddleware, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.data.config import get_required_channels, get_admins


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        bot: Bot = data.get("bot")
        user_id = data.get("event_from_user").id
        
        if user_id in get_admins():
            return await handler(event, data)
        
        required_channels = get_required_channels()
        
        if not required_channels:
            return await handler(event, data)
        
        unsubscribed_channels = []
        channel_buttons = []
        
        for channel_id in required_channels:
            try:
                member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
                
                if member.status in ['left', 'kicked']:
                    unsubscribed_channels.append(channel_id)
                    
                    try:
                        chat = await bot.get_chat(channel_id)
                        chat_title = chat.title
                        chat_username = chat.username
                        
                        if chat_username:
                            channel_buttons.append([
                                InlineKeyboardButton(
                                    text=f"📢 {chat_title}",
                                    url=f"https://t.me/{chat_username}"
                                )
                            ])
                        else:
                            invite_link = await bot.create_chat_invite_link(channel_id)
                            channel_buttons.append([
                                InlineKeyboardButton(
                                    text=f"📢 {chat_title}",
                                    url=invite_link.invite_link
                                )
                            ])
                    except:
                        pass
            except:
                pass
        
        if unsubscribed_channels:
            channel_buttons.append([
                InlineKeyboardButton(text="✅ Я подписался", callback_data="check_subscription")
            ])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=channel_buttons)
            
            if hasattr(event, 'message'):
                await event.message.answer(
                    "⚠️ <b>Для использования бота необходимо подписаться на наши каналы:</b>\n\n"
                    "После подписки нажмите кнопку <b>✅ Я подписался</b>",
                    reply_markup=keyboard
                )
            elif hasattr(event, 'answer'):
                await event.answer(
                    "⚠️ Для использования бота необходимо подписаться на наши каналы!",
                    show_alert=True
                )
            
            return
        
        return await handler(event, data)
