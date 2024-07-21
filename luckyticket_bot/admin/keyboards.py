import db
from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Управление админами', callback_data='admin.menu.admins')],
                                             [InlineKeyboardButton(text='Управление турами', callback_data=f'admin.menu.tours')],
                                             [InlineKeyboardButton(text='Выбрать главные туры', callback_data=f'admin.menu.maintours')]])

loading_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🕙 Обработка...', callback_data='none')]])

reservation_accepted = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅ Бронь принята', callback_data='none')]])
reservation_cancelled = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='❌ Бронь отменена', callback_data='none')]])

none_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='❌ Кнопка не нажимается', callback_data='none')]])

async def get_reservations_markup_accepted(departure_id):
    departure_data = await db.info_table.get_item_info(departure_id)
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅ Бронь принята', callback_data='none')],
                                                   [InlineKeyboardButton(
                                                       text=f'Свободно мест: {departure_data["seats"] - departure_data["occupied_seats"]}',
                                                       callback_data='none')]
                                                   ])
    return markup