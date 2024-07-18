import asyncio

from luckyticket_bot import bot

asyncio.run(bot.main())

# import db
# import asyncio
#
# async def main():
#     await db.initialize()
#     await db.info_table.drop_table()
#     await db.tours.drop_table()
#
# asyncio.run(main())