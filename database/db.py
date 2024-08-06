import json

import asyncpg
import config
import db


class tg_admins:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS tg_admins (
                                     id SERIAL PRIMARY KEY,
                                     user_id BIGINT,
                                     name TEXT)''')

    async def check_admin_by_id(self, admin_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT 1 FROM tg_admins WHERE id = $1''', admin_id)
            return row is not None

    async def check_admin_by_user_id(self, user_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT 1 FROM tg_admins WHERE user_id = $1', user_id)
            return row is not None

    async def add_admin(self, user_id, name):
        if not await self.check_admin_by_user_id(user_id):
            async with self.db.acquire() as connection:
                await connection.execute('''INSERT INTO tg_admins (user_id, name) VALUES ($1, $2)''', user_id, name)

    async def get_admins_list(self):
        async with self.db.acquire() as connection:
            cursor = await connection.fetch('''SELECT * FROM tg_admins''')
            return [dict(data) for data in cursor]

    async def get_admins_user_ids(self):
        async with self.db.acquire() as connection:
            cursor = await connection.fetch('''SELECT user_id FROM tg_admins''')
            return [data[0] for data in cursor]

    async def del_admin_by_id(self, admin_id):
        async with self.db.acquire() as connection:
            if await self.check_admin_by_id(admin_id):
                await connection.execute('''DELETE FROM tg_admins WHERE id = $1''', admin_id)

    async def get_admin_user_id_by_id(self, admin_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT user_id FROM tg_admins WHERE id = $1''', admin_id)
            return row["user_id"]


class info_table:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS info_table (
                                    id SERIAL PRIMARY KEY,
                                    tour_id INT,
                                    departure_time TEXT,
                                    arrival_time TEXT,
                                    seats INT,
                                    occupied_seats INT,
                                    prices JSON,
                                    bus TEXT)''')

    async def drop_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''DROP TABLE info_table''')

    async def add_item(self, tour_id):
        async with self.db.acquire() as connection:
            new_id = await connection.fetchval('''INSERT INTO info_table (tour_id, prices) VALUES ($1, $2) RETURNING id''', tour_id, json.dumps([]))
            return new_id

    async def get_items(self, tour_id):
        async with self.db.acquire() as connection:
            result = []
            cursor = await connection.fetch('''SELECT * FROM info_table WHERE tour_id = $1''', tour_id)
            if cursor is None:
                return []
            for i in cursor:
                data = dict(i)
                data["prices"] = json.loads(data["prices"])
                result.append(data)
            return result

    async def get_item_info(self, item_id):
        async with self.db.acquire() as connection:
            cursor = await connection.fetchrow('''SELECT * FROM info_table WHERE id = $1''', item_id)
            data = dict(cursor)
            data["prices"] = json.loads(data["prices"])
            return data

    async def get_prices(self, item_id):
        async with self.db.acquire() as connection:
            cursor = await connection.fetchrow('''SELECT prices FROM info_table WHERE id = $1''', item_id)
            if cursor is not None:
                return json.loads(dict(cursor)["prices"])
            return [{"variation": "default", "price": 0}]

    async def update_prices(self, item_id, prices):
        async with self.db.acquire() as connection:
            await connection.execute('''UPDATE info_table SET prices = $1 WHERE id = $2''', json.dumps(prices), item_id)

    async def add_price(self, item_id):
        prices = await self.get_prices(item_id)
        print(prices)
        prices.append({"variation": "Вариация", "price": 0})
        print(prices)
        await self.update_prices(item_id, prices)

    async def del_price(self, item_id):
        prices = await self.get_prices(item_id)
        prices.pop(-1)
        await self.update_prices(item_id, prices)

    async def update_bus(self, item_id, bus):
        async with self.db.acquire() as connection:
            await connection.execute('''
                            UPDATE info_table SET bus = $1 WHERE id = $2
                        ''', bus, item_id)

    async def update_occupied_seats(self, item_id, occupied_seats):
        async with self.db.acquire() as connection:
            await connection.execute('''UPDATE info_table SET occupied_seats = $1 WHERE id = $2''', occupied_seats, item_id)

    async def add_occupied_seats(self, item_id, count):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT occupied_seats FROM info_table WHERE id = $1''', item_id)
            occupied_seats = row[0]
            if occupied_seats is None:
                occupied_seats = 0
            new_occupied_seats = occupied_seats + count
            await self.update_occupied_seats(item_id, new_occupied_seats)

    async def update_seats(self, item_id, seats):
        async with self.db.acquire() as connection:
            await connection.execute('''UPDATE info_table SET seats = $1 WHERE id = $2''', seats, item_id)

    async def update_arrival_time(self, item_id, arrival_time):
        async with self.db.acquire() as connection:
            await connection.execute('''UPDATE info_table SET arrival_time = $1 WHERE id = $2''', arrival_time, item_id)

    async def update_departure_time(self, item_id, departure_time):
        async with self.db.acquire() as connection:
            await connection.execute('''UPDATE info_table SET departure_time = $1 WHERE id = $2''', departure_time, item_id)

    async def update_variation(self, item_id, variation_id, variation):
        prices = await self.get_prices(item_id)
        prices[variation_id]["variation"] = variation
        await self.update_prices(item_id, prices)

    async def update_price(self, item_id, variation_id, price):
        prices = await self.get_prices(item_id)
        prices[variation_id]["price"] = price
        await self.update_prices(item_id, prices)

    async def del_item(self, item_id):
        async with self.db.acquire() as connection:
            await connection.execute('''DELETE FROM info_table WHERE id = $1''', item_id)

class tours:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def drop_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''DROP TABLE tours''')

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS tours (
                                     id SERIAL PRIMARY KEY,
                                     name TEXT,
                                     duration TEXT,
                                     card_image TEXT,
                                     background_image TEXT,
                                     days_info JSON,
                                     important_text TEXT,
                                     description TEXT,
                                     main_card INT,
                                     price INT)''')

    async def get_main_cards(self):
        async with self.db.acquire() as connection:
            cursor = await connection.fetch('''SELECT id, name, description, duration, background_image, price FROM tours WHERE main_card = $1 ORDER BY id''', 1)
            return [dict(data) for data in cursor]

    async def get_cards(self):
        async with self.db.acquire() as connection:
            cursor = await connection.fetch('''SELECT id, name, description, duration, card_image, price FROM tours ORDER BY id''')
            result = []
            for data in cursor:
                print(data)
                result_data = dict(data)
                info_table = await db.info_table.get_items(data["id"])
                if info_table != []:
                    prices = await db.info_table.get_prices(info_table[0]["id"])
                    result_data["prices"] = prices
                else:
                    result_data["prices"] = []
                result.append(result_data)
            return result

    async def add_tour(self):
        async with self.db.acquire() as connection:
            new_id = await connection.fetchval('''INSERT INTO tours (name, background_image, main_card) 
            VALUES ($1, $2, $3) RETURNING id''', "Название тура", json.dumps([]), 0)
            await connection.execute('''UPDATE tours SET card_image = $1, background_image = $2 WHERE id = $3''',
                                     f"{config.fastapi_url}/images/card/{new_id}.png",
                                     f'{config.fastapi_url}/images/backgrounds/{new_id}.png',
                                     new_id)
            return new_id

    async def del_tour(self, tour_id):
        async with self.db.acquire() as connection:
            await connection.execute('''DELETE FROM tours WHERE id = $1''', tour_id)
            await connection.execute('''DELETE FROM info_table WHERE tour_id = $1''', tour_id)
            await connection.execute('''DELETE FROM card_images WHERE tour_id = $1''', tour_id)
            await connection.execute('''DELETE FROM background_images WHERE tour_id = $1''', tour_id)

    async def get_tours_list(self):
        async with self.db.acquire() as connection:
            cursor = await connection.fetch('''SELECT id, name, main_card FROM tours ORDER BY id''')
            return [dict(data) for data in cursor]

    async def get_tour_info(self, tour_id):
        async with self.db.acquire() as connection:
            cursor = dict(await connection.fetchrow('''SELECT * FROM tours WHERE id = $1''', tour_id))
            cursor["info_table"] = await db.info_table.get_items(tour_id)
            if cursor["days_info"] is None:
                cursor["days_info"] = []
            else:
                cursor["days_info"] = json.loads(cursor["days_info"])
            print(cursor)
            cursor["variations"] = []
            for i in cursor["info_table"]:
                for j in i["prices"]:
                    if j["variation"] not in cursor["variations"]:
                        cursor["variations"].append(j["variation"])
            return cursor

    async def get_tour_departure_info(self, tour_id, departure_id):
        async with self.db.acquire() as connection:
            cursor = dict(await connection.fetchrow('''SELECT id, name, duration, description FROM tours WHERE id = $1''', tour_id))
            items_cursor = await connection.fetchrow('''SELECT * FROM info_table WHERE id = $1''', departure_id)
            cursor["info_table"] = dict(items_cursor)
            cursor["info_table"]["prices"] = json.loads(cursor["info_table"]["prices"])
            return cursor

    async def update_name(self, tour_id, name):
        async with self.db.acquire() as connection:
            await connection.execute('''
                            UPDATE tours SET name = $1 WHERE id = $2
                        ''', name, tour_id)

    async def update_price(self, tour_id, price):
        async with self.db.acquire() as connection:
            await connection.execute('''UPDATE tours SET price = $1 WHERE id = $2''', price, tour_id)

    async def update_main_card(self, tour_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT main_card FROM tours WHERE id = $1''', tour_id)
            new_status = 0
            if row[0] is None or row[0] == 0:
                new_status = 1
            await connection.execute('''
                            UPDATE tours SET main_card  = $1 WHERE id = $2
                        ''', new_status, tour_id)

    async def update_description(self, tour_id, description):
        async with self.db.acquire() as connection:
            await connection.execute('''UPDATE tours SET description = $1 WHERE id = $2''', description, tour_id)

    async def update_duration(self, tour_id, duration):
        async with self.db.acquire() as connection:
            await connection.execute('''UPDATE tours SET duration = $1 WHERE id = $2''', duration, tour_id)

    async def update_important_text(self, tour_id, important_text):
        async with self.db.acquire() as connection:
            await connection.execute('''UPDATE tours SET important_text = $1 WHERE id = $2''', important_text, tour_id)

    async def update_days_info(self, tour_id, days_info):
        async with self.db.acquire() as connection:
            await connection.execute('''UPDATE tours SET days_info = $1 WHERE id = $2''', json.dumps(days_info), tour_id)

    async def update_day_info(self, tour_id, day_id, info):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT days_info FROM tours WHERE id = $1''', tour_id)
            days_info = json.loads(row[0])
            days_info[day_id] = info
            await self.update_days_info(tour_id, days_info)

    async def get_days_info(self, tour_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT days_info FROM tours WHERE id = $1''', tour_id)
            if row is not None:
                if row[0] is not None:
                    return json.loads(row[0])
                return []
            return []

    async def add_day_info(self, tour_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT days_info FROM tours WHERE id = $1''', tour_id)
            if row is not None:
                if row[0] is not None:
                    days_info = json.loads(row[0])
                else:
                    days_info = []
            else:
                days_info = []
            days_info.append("Текст")
            await connection.execute('''UPDATE tours SET days_info = $1 WHERE id = $2''', json.dumps(days_info), tour_id)

    async def del_day_info(self, tour_id, day_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT days_info FROM tours WHERE id = $1''', tour_id)
            days_info = json.loads(row[0])
            days_info.pop(day_id)
            await self.update_days_info(tour_id, days_info)

    async def get_tour_name_by_id(self, tour_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT name FROM tours WHERE id = $1''', tour_id)
            return row[0]

    async def truncate(self):
        async with self.db.acquire() as connection:
            await connection.execute('''TRUNCATE TABLE tours''')

class card_images:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS card_images (
                                                tour_id INT,
                                                data BYTEA)''')

    async def add_image(self, tour_id, data):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT 1 FROM card_images WHERE tour_id = $1''', tour_id)
            if row is not None:
                await connection.execute('''UPDATE card_images SET data = $1 WHERE tour_id = $2''', data, tour_id)
            else:
                await connection.execute('''INSERT INTO card_images (tour_id, data) VALUES ($1, $2)''', tour_id, data)

    async def get_images(self):
        async with self.db.acquire() as connection:
            cursor = await connection.fetch('''SELECT * FROM card_images''')
            return [dict(data) for data in cursor]

class background_images:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS background_images (
                                                tour_id INT,
                                                data BYTEA)''')

    async def add_image(self, tour_id, data):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT 1 FROM background_images WHERE tour_id = $1''', tour_id)
            if row is not None:
                await connection.execute('''UPDATE background_images SET data = $1 WHERE tour_id = $2''', data, tour_id)
            else:
                await connection.execute('''INSERT INTO background_images (tour_id, data) VALUES ($1, $2)''', tour_id, data)

    async def get_images(self):
        async with self.db.acquire() as connection:
            cursor = await connection.fetch('''SELECT * FROM background_images''')
            return [dict(data) for data in cursor]
