from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorDatabase
import os

client = AsyncIOMotorClient(os.environ["MONGO_URL"])
mongo_db = client.get_database("gestplay")

async def create_document(collection_name: str, document: BaseModel):
    try:
        #mongo_db = await get_mongo_db()
        collection= mongo_db.get_collection(collection_name)
        dictionary = document.model_dump(by_alias=True, exclude=["id"])
        result = await collection.insert_one(dictionary)
        return result
    except Exception as e:
        print("Error al escribir en la base de datos:", e)
        return None

#delete_document
async def delete_document(collection_name: str, id: str):
    try:
        #mongo_db = await get_mongo_db()
        collection = mongo_db.get_collection(collection_name)
        result = await collection.delete_one({"_id": ObjectId(id)})        
        if result.deleted_count == 1:
            return True 
        else:
            return False 

    except Exception as e:
        print("Error al eliminar carta por ID:", e)
        return None
    
async def find_game_data(collection_name: str, profile_id: str, game: str):
    try:
        #mongo_db = await get_mongo_db()
        collection = mongo_db.get_collection(collection_name)
        result = await collection.find_one({"profile_id_db": profile_id, "game": game})
        return result
    except Exception as e:
        print("Error al buscar carta por ID:", e)
        return None

#find_document by id
async def find_document(collection_name: str, id: str):
    try:
        #mongo_db = await get_mongo_db()
        collection = mongo_db[collection_name]
        result = await collection.find_one({"_id": ObjectId(id)})
        return result
    except Exception as e:
        print("Error al buscar documento por ID:", e)
        return None

#update_document
async def update_document(collection_name: str,id: str, document: BaseModel):
    try:
        #db = await get_mongo_db()
        print("id",id)
        collection = mongo_db[collection_name]
        dictionary = document.model_dump(by_alias=True, exclude=["id"])
        result = await collection.update_one({"_id": ObjectId(id)}, {"$set":dictionary})
        
        
        return result
        
    except Exception as e:
        print("Error al actualizar carta por ID:", e)
        return None
    
async def update_game_data(collection_name: str, profile_id: str, game: str, document: BaseModel):
    try:
        #mongo_db = await get_mongo_db()
        collection = mongo_db.get_collection(collection_name)
        result = await collection.update_one({"profile_id_db": profile_id, "game": game}, {"$set": document})
        
        if result.modified_count == 1:
            return result
        else:
            return None
    except Exception as e:
        print("Error al actualizar carta por ID:", e)
        return None