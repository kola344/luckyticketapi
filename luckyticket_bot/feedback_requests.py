from luckyticket_bot.bot_init import bot
import config
import db
from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

async def send_feedback_request_to_chat(name, email, phone_number, message):
    text = f'Новая заявка на связь с поддержкой\nИмя: {name}\nЭл. почта, {email}\nТелефон: {phone_number}\n\n{message}'
    await bot.send_message(chat_id=config.feedback_requests_chat, text=text)
