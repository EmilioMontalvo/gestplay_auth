import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URL")
db_name = os.getenv('MONGODB_NAME')
db_client: AsyncIOMotorClient = None

async def get_db() -> AsyncIOMotorClient:
    global db_client
    if db_client is None:        
        db_client = AsyncIOMotorClient(mongo_uri)
    return db_client[db_name]

async def connect_and_init_db():
    global db_client
    try:
        db_client = AsyncIOMotorClient(
            mongo_uri    
        )
        return True
    except Exception:
        return False


async def close_db_connect():
    global db_client
    if db_client is None:
        return
    db_client.close()
    db_client = None
    print(f'Connection Closed')