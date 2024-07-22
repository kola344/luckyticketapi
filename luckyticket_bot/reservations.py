from luckyticket_bot.bot_init import bot
import config
import db
from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

async def send_reservation_to_chat(tour_id, departure_id, name, phone_number, email, telegram, comment, variations):
    tour_name = await db.tours.get_tour_name_by_id(tour_id)
    departure_data = await db.info_table.get_item_info(departure_id)
    text = (f'ТУР {tour_id}. Отправление от: {departure_data["departure_time"]}\n{tour_name}\nНовая бронь на имя {name}\nemail: {email}\ntelegram: {telegram}\nТелефон: {phone_number}\n\n{comment}\n\n')
    variations_data = await db.info_table.get_prices(departure_id)
    print(variations_data)
    price = 0
    count = 0
    for i in range(len(variations)):
        variation_data = variations_data[i]
        print(variation_data)
        variation_person = variations[i].name
        count += 1
        variation_name = variation_data["variation"]
        variation_price = variation_data["price"]
        price += variation_price
        text += f'{variation_person} - {variation_name}: {variation_price}\n'
    text += f'ИТОГО: {price}'

    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅ Принять бронь', callback_data=f'res.accept:{departure_id}.{count}')],
                                                    [InlineKeyboardButton(text='❌ Отменить бронь', callback_data=f'res.do.cancel')],
                                                   [InlineKeyboardButton(text=f'Свободно мест: {departure_data["seats"] - departure_data["occupied_seats"]}', callback_data='none')]])

    await bot.send_message(chat_id=config.reservations_chat, text=text, reply_markup=markup)
