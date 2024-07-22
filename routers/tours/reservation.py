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
    messanger - ссылка на любой мессенджер (вк, тг)
    email - емаил
    comment - комментарий
    [{"variation": int, "name": str}, {variation, name}] - вариация и имя человека
    То есть на фронте должна быть возможность добавить +1 к вариации и вписать имя человека на эту вариацию
    Также нужно учитывать, чтобы забронировать можно было мест столько, чтобы они не превышали количество свободных'''
    await send_reservation_to_chat(item.tour_id, item.departure_id, item.name, item.phone_number, item.email, item.telegram, item.comment, item.variations)
    return {"status": True, "info": "success"}
