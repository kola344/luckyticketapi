from database import db
from asyncpg import create_pool

tg_admins = db.tg_admins()
tours = db.tours()
info_table = db.info_table()
card_images = db.card_images()
background_images = db.background_images()
async def initialize(folder = 'database/'):
    db = await create_pool(user='gen_user', password='b%|#bSc0!YhAOu', database='default_db', host="147.45.138.15")
    await tg_admins.connect(db)
    await tg_admins.create_table()
    await tours.connect(db)
    await tours.create_table()
    await info_table.connect(db)
    await info_table.create_table()
    await card_images.connect(db)
    await card_images.create_table()
    await background_images.connect(db)
    await background_images.create_table()
