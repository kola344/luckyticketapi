from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Управление админами', callback_data='admin.menu.admins')],
                                             [InlineKeyboardButton(text='Управление турами', callback_data=f'admin.menu.tours')],
                                             [InlineKeyboardButton(text='Выбрать главные туры', callback_data=f'admin.menu.maintours')]])

loading_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🕙 Обработка...', callback_data='none')]])
