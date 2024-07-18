import asyncio
from aiogram import Bot, Dispatcher
import config
from luckyticket_bot.bot_init import bot, dp
from luckyticket_bot.admin.admin_messages import router as admin_router
import db

async def bot_starter():
    print('bot running')
    dp.include_router(admin_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def main():
    await db.initialize()
    await bot_starter()

if __name__ == '__main__':
    print('virazh bot running')
    asyncio.run(main())
