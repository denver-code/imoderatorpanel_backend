import motor.motor_asyncio
import requests
import api.config_api as cp


r = requests.get("http://ip.42.pl/raw")

ip = r.text

if ip != cp.get_value(name="server_ip"):
    DATABASE_LOCAL = cp.get_value(name="database_local")
    client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_LOCAL)
else:
    DATABASE = cp.get_value(name="database")
    client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE)

db = client["iNews"]

users = db["users"]
waitpublish = db["waitpublish"]
posts = db["posts"]

async def insert_db(db, data):
    return await globals()[db].insert_one(data)

async def find_one_query(db, querry):
    return await globals()[db].find_one(querry)

async def find_query(db, querry):
    cursor =  globals()[db].find(querry)
    return await cursor.to_list(length=1000)

async def update_db(db, scdata, ndata):
    return await globals()[db].update_one(scdata, {"$set": ndata}, upsert=True)

async def delete_db(db, obj):
    await globals()[db].delete_one(obj)