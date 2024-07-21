import asyncio
import traceback

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile
from luckyticket_bot.admin.replics import *
from luckyticket_bot.admin import keyboards, models
import db
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os
from luckyticket_bot import temp
from luckyticket_bot.bot_init import bot

router = Router()

@router.message(models.departure_editorState.edit_price, F.text)
async def edit_dep_priceFunc(message: Message, state: FSMContext):
    try:
        validate = int(message.text)
        user = models.editor_departure[message.chat.id]
        tour_id = user.tour_id
        departure_id = user.departure_id
        variation_id = user.variation_id
        await db.info_table.update_price(departure_id, variation_id, validate)
        text, markup = await replic_menu_editor_departure(tour_id, departure_id)
        await message.answer(text, reply_markup=markup)
        await state.clear()
    except Exception as e:
        print(e)
        await message.answer(replic_edit_dep_int_error)

@router.message(models.departure_editorState.edit_variation, F.text)
async def edit_dep_variationFunc(message: Message, state: FSMContext):
    user = models.editor_departure[message.chat.id]
    tour_id = user.tour_id
    departure_id = user.departure_id
    variation_id = user.variation_id
    await db.info_table.update_variation(departure_id, variation_id, message.text)
    text, markup = await replic_menu_editor_departure(tour_id, departure_id)
    await message.answer(text, reply_markup=markup)
    await state.clear()

@router.message(models.departure_editorState.edit_departure_time, F.text)
async def edit_dep_departure_timeFunc(message: Message, state: FSMContext):
    user = models.editor_departure[message.chat.id]
    tour_id = user.tour_id
    departure_id = user.departure_id
    await db.info_table.update_departure_time(departure_id, message.text)
    text, markup = await replic_menu_editor_departure(tour_id, departure_id)
    await message.answer(text, reply_markup=markup)
    await state.clear()

@router.message(models.departure_editorState.edit_arrival_time, F.text)
async def edit_dep_arrival_timeFunc(message: Message, state: FSMContext):
    user = models.editor_departure[message.chat.id]
    tour_id = user.tour_id
    departure_id = user.departure_id
    await db.info_table.update_arrival_time(departure_id, message.text)
    text, markup = await replic_menu_editor_departure(tour_id, departure_id)
    await message.answer(text, reply_markup=markup)
    await state.clear()

@router.message(models.departure_editorState.edit_seats, F.text)
async def edit_dep_seatsFunc(message: Message, state: FSMContext):
    try:
        validate = int(message.text)
        user = models.editor_departure[message.chat.id]
        tour_id = user.tour_id
        departure_id = user.departure_id
        departure_data = await db.info_table.get_item_info(departure_id)
        if departure_data["occupied_seats"] is None:
            departure_data["occupied_seats"] = 0
        if validate < departure_data["occupied_seats"]:
            await message.answer(replic_edit_dep_seats_error)
        else:
            await db.info_table.update_seats(departure_id, validate)
            text, markup = await replic_menu_editor_departure(tour_id, departure_id)
            await message.answer(text, reply_markup=markup)
            await state.clear()
    except Exception as e:
        print(e)
        await message.answer(replic_edit_dep_int_error)

@router.message(models.departure_editorState.edit_occupied_seats, F.text)
async def edit_dep_occupied_seatsFunc(message: Message, state: FSMContext):
    try:
        validate = int(message.text)
        user = models.editor_departure[message.chat.id]
        tour_id = user.tour_id
        departure_id = user.departure_id
        departure_data = await db.info_table.get_item_info(departure_id)
        if departure_data["seats"] is None:
            departure_data["seats"] = 0
        if validate > departure_data["seats"]:
            await message.answer(replic_edit_dep_occupied_seats_error)
        else:
            await db.info_table.update_occupied_seats(departure_id, validate)
            text, markup = await replic_menu_editor_departure(tour_id, departure_id)
            await message.answer(text, reply_markup=markup)
            await state.clear()
    except Exception as e:
        print(e)
        await message.answer(replic_edit_dep_int_error)

@router.message(models.departure_editorState.edit_bus, F.text)
async def edit_dep_busFunc(message: Message, state: FSMContext):
    user = models.editor_departure[message.chat.id]
    tour_id = user.tour_id
    departure_id = user.departure_id
    await db.info_table.update_bus(departure_id, message.text)
    text, markup = await replic_menu_editor_departure(tour_id, departure_id)
    await message.answer(text, reply_markup=markup)
    await state.clear()

@router.message(models.tour_editorState.edit_day_info, F.text)
async def edit_day_infoFunc(message: Message, state: FSMContext):
    user = models.editor_days_info[message.chat.id]
    tour_id = user.tour_id
    day_id = user.day_id
    await db.tours.update_day_info(tour_id, day_id, message.text)
    text, markup = await replic_menu_editor_days_info(tour_id)
    await message.answer(text, reply_markup=markup)
    await state.clear()

@router.message(models.tour_editorState.edit_background_image, F.photo)
async def edit_tour_descriptionFunc(message: Message, state: FSMContext):
    tour_id = models.editor_tour_id[message.chat.id]
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    await bot.download_file(file_path, f'images/backgrounds/{tour_id}.png')
    with open(f'images/backgrounds/{tour_id}.png', 'rb') as f:
        await db.background_images.add_image(tour_id, f.read())
    await db.tours.update_duration(tour_id, message.text)
    await state.clear()
    text, markup = await replic_menu_edit_tour(tour_id)
    if os.path.exists(f'images/cards/{tour_id}.png'):
        await message.answer_photo(photo=FSInputFile(f'images/cards/{tour_id}.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)

@router.message(models.tour_editorState.edit_card_image, F.photo)
async def edit_tour_descriptionFunc(message: Message, state: FSMContext):
    tour_id = models.editor_tour_id[message.chat.id]
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    await bot.download_file(file_path, f'images/cards/{tour_id}.png')
    with open(f'images/cards/{tour_id}.png', 'rb') as f:
        await db.card_images.add_image(tour_id, f.read())
    await db.tours.update_duration(tour_id, message.text)
    await state.clear()
    text, markup = await replic_menu_edit_tour(tour_id)
    if os.path.exists(f'images/cards/{tour_id}.png'):
        await message.answer_photo(photo=FSInputFile(f'images/cards/{tour_id}.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)

@router.message(models.tour_editorState.edit_important_text, F.text)
async def edit_tour_descriptionFunc(message: Message, state: FSMContext):
    tour_id = models.editor_tour_id[message.chat.id]
    await db.tours.update_important_text(tour_id, message.text)
    await state.clear()
    text, markup = await replic_menu_edit_tour(tour_id)
    if os.path.exists(f'images/cards/{tour_id}.png'):
        await message.answer_photo(photo=FSInputFile(f'images/cards/{tour_id}.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)

@router.message(models.tour_editorState.edit_duration, F.text)
async def edit_tour_descriptionFunc(message: Message, state: FSMContext):
    tour_id = models.editor_tour_id[message.chat.id]
    await db.tours.update_duration(tour_id, message.text)
    await state.clear()
    text, markup = await replic_menu_edit_tour(tour_id)
    if os.path.exists(f'images/cards/{tour_id}.png'):
        await message.answer_photo(photo=FSInputFile(f'images/cards/{tour_id}.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)

@router.message(models.tour_editorState.edit_description, F.text)
async def edit_tour_descriptionFunc(message: Message, state: FSMContext):
    tour_id = models.editor_tour_id[message.chat.id]
    await db.tours.update_description(tour_id, message.text)
    await state.clear()
    text, markup = await replic_menu_edit_tour(tour_id)
    if os.path.exists(f'images/cards/{tour_id}.png'):
        await message.answer_photo(photo=FSInputFile(f'images/cards/{tour_id}.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)

@router.message(models.tour_editorState.edit_name, F.text)
async def edit_tour_nmaeFunc(message: Message, state: FSMContext):
    tour_id = models.editor_tour_id[message.chat.id]
    await db.tours.update_name(tour_id, message.text)
    await state.clear()
    text, markup = await replic_menu_edit_tour(tour_id)
    if os.path.exists(f'images/cards/{tour_id}.png'):
        await message.answer_photo(photo=FSInputFile(f'images/cards/{tour_id}.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)

@router.message(F.text == '/admin')
async def admin_command(message: Message):
    if await db.tg_admins.check_admin_by_user_id(message.chat.id):
        await message.answer(replic_admin_panel, reply_markup=keyboards.menu)
    else:
        await message.answer(replic_403)

@router.message(F.text.startswith('/start reg_admin_'))
async def start_admin_reg_command(message: Message):
    try:
        key = message.text.split()[1]
        if key == temp.reg_admin_key:
            temp.reg_admin_key = None
            await db.tg_admins.add_admin(message.chat.id, message.from_user.first_name)
            await message.answer(replic_admin_reg_success)
        else:
            await message.answer(replic_403)
    except Exception as e:
        print(e)
        await message.answer(replic_403)

@router.message(F.text == '/reg_admin')
async def reg_admin_command(message: Message):
    if await db.tg_admins.check_admin_by_user_id(message.chat.id):
        await message.answer(replic_reg_new_admin_keygen())
    else:
        await message.answer(replic_403)

@router.callback_query(F.data == 'none')
async def none_button_callback(call):
    try:
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboards.none_button)
        await asyncio.sleep(1)
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=call.message.reply_markup)
    except Exception as e:
        print(e)

@router.callback_query(F.data.startswith('res'))
async def callback(call, state: FSMContext):
    print(call.data)
    user_id = call.message.chat.id
    if await db.tg_admins.check_admin_by_user_id(user_id):
        calls = str(call.data).split(sep='.')
        l1 = calls[0]
        l2 = calls[1]
        l3 = calls[2]
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboards.loading_menu)
        if l2 == 'do':
            if l3 == 'cancel':
                await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboards.reservation_cancelled)
        else:
            if ':' in l2:
                splited_l2 = l2.split(':')
                k1, k2 = splited_l2[0], splited_l2[1]
                if k1 == 'accept':
                    await db.info_table.add_occupied_seats(int(k2), int(l3))
                    markup = await keyboards.get_reservations_markup_accepted(int(k2))
                    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                        message_id=call.message.message_id,
                                                        reply_markup=markup)

@router.callback_query(F.data.startswith('admin'))
async def callback(call, state: FSMContext):
    print(call.data)
    user_id = call.message.chat.id
    if await db.tg_admins.check_admin_by_user_id(user_id):
        calls = str(call.data).split(sep='.')
        l1 = calls[0]
        l2 = calls[1]
        l3 = calls[2]
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboards.loading_menu)
        if l2 == 'main':
            if l3 == 'main':
                await bot.edit_message_text(replic_admin_panel, chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboards.menu)
        elif l2 == 'etourname':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            await state.set_state(models.tour_editorState.edit_name)
            models.editor_tour_id[user_id] = int(l3)
            await call.message.answer(replic_edit_tour_name)
        elif l2 == 'etourdesc':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            await state.set_state(models.tour_editorState.edit_description)
            models.editor_tour_id[user_id] = int(l3)
            await call.message.answer(replic_edit_tour_description)
        elif l2 == 'etoirdur':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            await state.set_state(models.tour_editorState.edit_duration)
            models.editor_tour_id[user_id] = int(l3)
            await call.message.answer(replic_edit_tour_duration)
        elif l2 == 'etourimp':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            await state.set_state(models.tour_editorState.edit_important_text)
            models.editor_tour_id[user_id] = int(l3)
            await call.message.answer(replic_edit_tour_important_text)
        elif l2 == 'etourcard':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            await state.set_state(models.tour_editorState.edit_card_image)
            models.editor_tour_id[user_id] = int(l3)
            await call.message.answer(replic_edit_tour_image)
        elif l2 == 'etourback':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            await state.set_state(models.tour_editorState.edit_background_image)
            models.editor_tour_id[user_id] = int(l3)
            await call.message.answer(replic_edit_tour_image)
        elif l2 == 'deltour':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            text, markup = replic_del_tour_confirmation(l3)
            await call.message.answer(text, reply_markup=markup)
        elif l2 == 'deltconfirm':
            await db.tours.del_tour(int(l3))
            text, markup = await replic_menu_tours()
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'tour':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            text, markup = await replic_menu_edit_tour(int(l3))
            if os.path.exists(f'images/cards/{l3}.png'):
                await call.message.answer_photo(photo=FSInputFile(f'images/cards/{l3}.png'), caption=text, reply_markup=markup)
            else:
                await call.message.answer(text, reply_markup=markup)
        elif l2 == 'menu':
            if l3 == 'admins':
                text, markup = await replic_menu_admins()
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            elif l3 == 'tours':
                await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
                text, markup = await replic_menu_tours()
                await call.message.answer(text, reply_markup=markup)
            elif l3 == 'maintours':
                text, markup = await replic_menu_maintours()
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'updatemain':
            await db.tours.update_main_card(int(l3))
            text, markup = await replic_menu_maintours()
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'add':
            if l3 == 'tour':
                tour_id = await db.tours.add_tour()
                text, markup = await replic_menu_edit_tour(tour_id)
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'del':
            admin_id = await db.tg_admins.get_admin_user_id_by_id(int(l3))
            if user_id != admin_id:
                await db.tg_admins.del_admin_by_id(int(l3))
            else:
                await bot.edit_message_text(replic_admin_cannot_delete_self, chat_id=user_id, message_id=call.message.message_id)
                await asyncio.sleep(2)
            text, markup = await replic_menu_admins()
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'etourdays':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            text, markup = await replic_menu_editor_days_info(int(l3))
            await call.message.answer(text, reply_markup=markup)
        elif l2 == 'adayinfo':
            await db.tours.add_day_info(int(l3))
            text, markup = await replic_menu_editor_days_info(int(l3))
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'adddep':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            departure_id = await db.info_table.add_item(int(l3))
            text, markup = await replic_menu_editor_departure(int(l3), departure_id)
            await call.message.answer(text, reply_markup=markup)
        else:
            if ':' in l2:
                splited_l2 = l2.split(':')
                k1, k2 = splited_l2[0], splited_l2[1]
                if k1 == 'etdel':
                    await db.tours.del_day_info(int(k2), int(l3))
                    text, markup = await replic_menu_editor_days_info(int(k2))
                    await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
                elif k1 == 'etd':
                    models.editor_days_info[user_id] = models.editor_days(int(k2), int(l3))
                    await bot.edit_message_text(replic_edit_day_info, chat_id=user_id, message_id=call.message.message_id)
                    await state.set_state(models.tour_editorState.edit_day_info)
                elif k1 == 'deldep':
                    await db.info_table.del_item(int(l3))
                    await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
                    text, markup = await replic_menu_edit_tour(int(k2))
                    if os.path.exists(f'images/cards/{k2}.png'):
                        await call.message.answer_photo(photo=FSInputFile(f'images/cards/{k2}.png'), caption=text, reply_markup=markup)
                    else:
                        await call.message.answer(text, reply_markup=markup)
                elif k1 == 'edepbus':
                    models.editor_departure[user_id] = models.editor_dep(int(k2), int(l3))
                    await state.set_state(models.departure_editorState.edit_bus)
                    await bot.edit_message_text(replic_edit_dep_bus, chat_id=user_id, message_id=call.message.message_id)
                elif k1 == 'edepoc':
                    models.editor_departure[user_id] = models.editor_dep(int(k2), int(l3))
                    await state.set_state(models.departure_editorState.edit_occupied_seats)
                    await bot.edit_message_text(replic_edit_dep_occupied_seats, chat_id=user_id, message_id=call.message.message_id)
                elif k1 == 'edeps':
                    models.editor_departure[user_id] = models.editor_dep(int(k2), int(l3))
                    await state.set_state(models.departure_editorState.edit_seats)
                    await bot.edit_message_text(replic_edit_dep_seats, chat_id=user_id, message_id=call.message.message_id)
                elif k1 == 'edepta':
                    models.editor_departure[user_id] = models.editor_dep(int(k2), int(l3))
                    await state.set_state(models.departure_editorState.edit_arrival_time)
                    await bot.edit_message_text(replic_edit_dep_arrival_time, chat_id=user_id, message_id=call.message.message_id)
                elif k1 == 'edeptd':
                    models.editor_departure[user_id] = models.editor_dep(int(k2), int(l3))
                    await state.set_state(models.departure_editorState.edit_departure_time)
                    await bot.edit_message_text(replic_edit_dep_departure_time, chat_id=user_id, message_id=call.message.message_id)
                elif k1 == 'edepav':
                    await db.info_table.add_price(int(l3))
                    text, markup = await replic_menu_editor_departure(int(k2), int(l3))
                    await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
                elif k1 == 'edepdv':
                    await db.info_table.del_price(int(l3))
                    text, markup = await replic_menu_editor_departure(int(k2), int(l3))
                    await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
                elif k1 == 'dep':
                    await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
                    text, markup = await replic_menu_editor_departure(int(k2), int(l3))
                    await call.message.answer(text, reply_markup=markup)
                else:
                    if ':' in l3:
                        splited_l3 = l3.split(':')
                        j1, j2 = splited_l3[0], splited_l3[1]
                        if k1 == 'edepp':
                            models.editor_departure[user_id] = models.editor_dep(int(k2), int(j1))
                            models.editor_departure[user_id].variation_id = int(j2)
                            await state.set_state(models.departure_editorState.edit_price)
                            await bot.edit_message_text(replic_edit_dep_price, chat_id=user_id, message_id=call.message.message_id)
                        elif k1 == 'edepv':
                            models.editor_departure[user_id] = models.editor_dep(int(k2), int(j1))
                            models.editor_departure[user_id].variation_id = int(j2)
                            await state.set_state(models.departure_editorState.edit_variation)
                            await bot.edit_message_text(replic_edit_dep_variation, chat_id=user_id, message_id=call.message.message_id)



