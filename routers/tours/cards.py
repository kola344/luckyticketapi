from fastapi import APIRouter
import db
from models.tours.cards import get_tour_infoModel

router = APIRouter()

@router.post('/get_main_cards')
async def get_main_cardsPage():
    '''Возвращает список карточек, которые сразу под хеадером.'''
    data = await db.tours.get_main_cards()
    return {"status": True, "info": "success", "data": data}

@router.post('/get_cards')
async def get_cardsPage():
    '''Возвращает список всех карточек.'''
    data = await db.tours.get_cards()
    return {"status": True, "info": "success", "data": data}

@router.post('/get_tour_info')
async def get_tour_infoPage(item: get_tour_infoModel):
    '''[days_info] = описание каждого дня. Может быть до 4096 символов, а также есть табуляция переноса строк\n
    important_text = важный текст. Может быть до 4096 символов и также с переносом строк'''
    data = await db.tours.get_tour_info(item.tour_id)
    return {"status": True, "info": "success", "data": data}