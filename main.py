from fastapi import FastAPI, Request, Response
from routers.tours.cards import router as cards_router
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import db
from typing import Any
from luckyticket_bot.bot_init import bot, dp
from luckyticket_bot.admin.admin_messages import router as bot_admin_router
from aiogram.types import Update
import os
import config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(cards_router, prefix="/tours/cards", tags=["cards"])


@app.get('/')
async def index_page():
    '''Ахахахахахахаххахахахахахахахахх'''
    try:
        await db.initialize()
        dp.include_router(bot_admin_router)
        await bot.set_webhook(config.webhook_url, drop_pending_updates=True)
        return {"Status": True, "init": 'Success'}
    except Exception as e:
        return {"Status": False, "init": f"err: {e}"}

@app.post('/webhook')
async def webhook(update: dict[str, Any]):
    '''АХАХАХХАХАХАХАХАХАХАХ'''
    await dp.feed_webhook_update(bot=bot, update=Update(**update))
    return {'status': 'ok'}

@app.on_event('startup')
async def on_startup():
    await db.initialize()
    if not os.path.exists('images'):
        os.mkdir('images')
    if not os.path.exists('images/backgrounds'):
        os.mkdir('images/backgrounds')
    for image in await db.background_images.get_images():
        if not os.path.exists(f'images/backgrounds/{image["tour_id"]}.png'):
            with open(f'images/backgrounds/{image["tour_id"]}.png', 'wb') as f:
                f.write(image["data"])
    if not os.path.exists('images/cards'):
        os.mkdir('images/cards')
    for image in await db.card_images.get_images():
        if not os.path.exists(f'images/cards/{image["tour_id"]}.png'):
            with open(f'images/cards/{image["tour_id"]}.png', 'wb') as f:
                f.write(image["data"])
    dp.include_router(bot_admin_router)
    await bot.set_webhook(config.webhook_url, drop_pending_updates=True)

@app.get('/images/card/{image}')
async def get_cards_imagesPage(image: str):
    file_path = f'images/cards/{image}'
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse('icons/notfound.jpg')

@app.get('/images/backgrounds/{image}')
async def get_backgrounds_imagesPage(image: str):
    file_path = f'images/backgrounds/{image}'
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse('icons/notfound.jpg')

@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, proxy-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Surrogate-Control"] = "no-store"
    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=5500)

