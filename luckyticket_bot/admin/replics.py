from luckyticket_bot import temp, keygen
from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import db

replic_403 = 'Отказано в доступе'
replic_admin_reg_success = 'Вы были зарегистрированы в как администратор'
replic_admin_cannot_delete_self = 'Вы не можете удалить себя'
replic_admin_panel = 'Админ панель'
replic_edit_tour_name = 'Введите новое название тура'
replic_edit_tour_description = 'Введите новое описание тура'
replic_edit_tour_duration = 'Введите новую длительность тура'
replic_edit_tour_important_text = 'Введите новую важную информацию о туре'
replic_edit_tour_image = 'Пришлите новое изображение'
replic_edit_day_info = 'Введите новое описание дня'
replic_edit_dep_bus = 'Введите новое названия автобуса'
replic_edit_dep_occupied_seats = 'Введите новое количество занятых мест'
replic_edit_dep_seats = 'Введите новое значение мест'
replic_edit_dep_arrival_time = 'Введите новую дату прибытия'
replic_edit_dep_departure_time = 'Введите новую дату отправления'
replic_edit_dep_price = 'Введите новую цену для вариации'
replic_edit_dep_variation = 'Введите новое название вариации'
replic_edit_dep_int_error = 'Введенное значение должно быть числом'
replic_edit_dep_occupied_seats_error = 'Число занятых мест не должно превышать общее число мест'
replic_edit_dep_seats_error = 'Общее число мест не должно быть меньше занятого числа мест'

def replic_del_tour_confirmation(tour_id):
    text = 'Вы действительно хотите удалить тур?'
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='❌ Удалить', callback_data=f'admin.deltconfirm.{tour_id}')],
                                                   [InlineKeyboardButton(text='⬅️ Назад', callback_data=f'admin.tour.{tour_id}')]])
    return text, markup

def replic_reg_new_admin_keygen():
    temp.reg_admin_key = f'reg_admin_' + keygen.generate_password(12)
    return f'Ссылка на регистрацию нового администратор:\nhttps://t.me/lucky_ticket_bot?start={temp.reg_admin_key}'


async def replic_menu_admins():
    admins = await db.tg_admins.get_admins_list()
    keyboard = []
    for i in admins:
        keyboard.append([InlineKeyboardButton(text=i['name'], callback_data=f"admin.del.{i['id']}")])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data='admin.main.main')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Управление админами (Нажмите, чтобы удалить)'
    return text, markup

async def replic_menu_tours():
    tours = await db.tours.get_tours_list()
    keyboard = []
    for i in tours:
        keyboard.append([InlineKeyboardButton(text=i["name"], callback_data=f"admin.tour.{i['id']}")])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить', callback_data=f'admin.add.tour')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data='admin.main.main')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Управление турами'
    return text, markup

async def replic_menu_maintours():
    tours = await db.tours.get_tours_list()
    keyboard = []
    for i in tours:
        print(i)
        if i['main_card'] is None or i["main_card"] == 0:
            keyboard.append([InlineKeyboardButton(text=f'🔴 {i["name"]}', callback_data=f"admin.updatemain.{i['id']}")])
        else:
            keyboard.append([InlineKeyboardButton(text=f'🟢 {i["name"]}', callback_data=f"admin.updatemain.{i['id']}")])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data='admin.main.main')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Управление главными турами'
    return text, markup

async def replic_menu_edit_tour(tour_id):
    tour_data = await db.tours.get_tour_info(tour_id)
    text = f'{tour_data["name"]}\n{tour_data["description"]}\nДлительность: {tour_data["duration"]}'
    keyboard = []
    keyboard.append([InlineKeyboardButton(text='Название', callback_data=f'admin.etourname.{tour_id}')])
    keyboard.append([InlineKeyboardButton(text='Описание', callback_data=f'admin.etourdesc.{tour_id}')])
    keyboard.append([InlineKeyboardButton(text='Длительность', callback_data=f'admin.etoirdur.{tour_id}')])
    keyboard.append([InlineKeyboardButton(text='Описание дней', callback_data=f'admin.etourdays.{tour_id}')])
    keyboard.append([InlineKeyboardButton(text='Важный текст', callback_data=f'admin.etourimp.{tour_id}')])
    keyboard.append([InlineKeyboardButton(text='🖼️ Карточка', callback_data=f'admin.etourcard.{tour_id}')])
    keyboard.append([InlineKeyboardButton(text='🖼️ Фон', callback_data=f'admin.etourback.{tour_id}')])
    for i in tour_data["info_table"]:
        if i["departure_time"] == None:
            inline_text = 'Отправление'
        else:
            inline_text = i["departure_time"]
        keyboard.append([InlineKeyboardButton(text=inline_text, callback_data=f'admin.dep:{tour_id}.{i["id"]}')])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить', callback_data=f'admin.adddep.{tour_id}')])
    keyboard.append([InlineKeyboardButton(text='❌ Удалить тур', callback_data=f'admin.deltour.{tour_id}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'admin.menu.tours')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return text, markup

async def replic_menu_editor_days_info(tour_id):
    days_info = await db.tours.get_days_info(tour_id)
    keyboard = []
    for i in range(len(days_info)):
        keyboard.append([InlineKeyboardButton(text=str(i+1), callback_data=f'admin.etd:{tour_id}.{i}')])
    keyboard.append([InlineKeyboardButton(text='❌', callback_data=f'admin.etdel:{tour_id}.{len(days_info) - 1}')])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить', callback_data=f'admin.adayinfo.{tour_id}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'admin.tour.{tour_id}')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Редактирование дней тура'
    return text, markup

async def replic_menu_editor_departure(tour_id, departure_id):
    data = await db.info_table.get_item_info(departure_id)
    keyboard = []
    print(data)
    print(data['prices'])
    for i in range(len(data["prices"])):
        print(data["prices"][i])
        keyboard.append([InlineKeyboardButton(text=data["prices"][i]["variation"], callback_data=f'admin.edepv:{tour_id}.{departure_id}:{i}'),
                         InlineKeyboardButton(text=str(data["prices"][i]["price"]), callback_data=f'admin.edepp:{tour_id}.{departure_id}:{i}')])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить вариацию', callback_data=f'admin.edepav:{tour_id}.{departure_id}')])
    keyboard.append([InlineKeyboardButton(text='➖ Убрать вариацию', callback_data=f'admin.edepdv:{tour_id}.{departure_id}')])
    keyboard.append([InlineKeyboardButton(text='Дата отправления', callback_data=f'admin.edeptd:{tour_id}.{departure_id}')])
    keyboard.append([InlineKeyboardButton(text='Дата прибытия', callback_data=f'admin.edepta:{tour_id}.{departure_id}')])
    keyboard.append([InlineKeyboardButton(text='Всего мест', callback_data=f'admin.edeps:{tour_id}.{departure_id}')])
    keyboard.append([InlineKeyboardButton(text='Мест занято', callback_data=f'admin.edepoc:{tour_id}.{departure_id}')])
    keyboard.append([InlineKeyboardButton(text='Автобус', callback_data=f'admin.edepbus:{tour_id}.{departure_id}')])
    keyboard.append([InlineKeyboardButton(text='❌ Удалить', callback_data=f'admin.deldep:{tour_id}.{departure_id}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'admin.tour.{tour_id}')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    if data["seats"] is None:
        data["seats"] = 0
    if data["occupied_seats"] is None:
        data['occupied_seats'] = 0
    text = (f'Отправление от: {data["departure_time"]}\nДо: {data["arrival_time"]}\nАвтобус: {data["bus"]}\nЗанято мест: {data["occupied_seats"]}\nСвободных мест: {data["seats"] - data["occupied_seats"]}\nВсего мест: {data["seats"]}')
    return text, markup


