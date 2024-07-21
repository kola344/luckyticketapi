from fastapi import APIRouter
from luckyticket_bot.reservations import send_reservation_to_chat
import db
from models.tours.reservation import reservationModel

router = APIRouter()

@router.post('/send_reservation')
async def send_variationPage(item: reservationModel):
    '''Отправить бронь на сервер
    name - ФИО отправителя
    phone_number - телефон
    email - емаил
    comment - комментарий
    [{"variation": int, "count": int}, {variation, count}] - вариации и их количество'''
    await send_reservation_to_chat(item.tour_id, item.departure_id, item.name, item.phone_number, item.email, item.telegram, item.comment, item.variations)
    return {"status": True, "info": "success"}
