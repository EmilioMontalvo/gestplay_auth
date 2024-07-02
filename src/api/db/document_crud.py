from bson import ObjectId
from pydantic import BaseModel
from api.db.mongo_db import get_db
from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorDatabase

async def create_document(collection_name: str, document: BaseModel):
    try:
        db = await get_db()
        collection= db[collection_name]
        result = await collection.insert_one(document.model_dump())
        return result
    except Exception as e:
        print("Error al escribir en la base de datos:", e)
        return None

#delete_document
async def delete_document(collection_name: str, id: str):
    try:
        db = await get_db()
        collection = db[collection_name]
        result = await collection.delete_one({"_id": ObjectId(id)})        
        if result.deleted_count == 1:
            return True 
        else:
            return False 

    except Exception as e:
        print("Error al eliminar carta por ID:", e)
        return None

#find_document by id
async def find_document(collection_name: str, id: str):
    try:
        db = await get_db()
        collection = db[collection_name]
        result = await collection.find_one({"_id": ObjectId(id)})
        return result
    except Exception as e:
        print("Error al buscar documento por ID:", e)
        return None

#update_document
async def update_document(collection_name: str,id: str, document: BaseModel):
    try:
        db = await get_db()
        collection = db[collection_name]
        result = await collection.update_one({"_id": ObjectId(id)}, {"$set": document})
        
        if result.modified_count == 1:
            return result
        else:
            return None
    except Exception as e:
        print("Error al actualizar carta por ID:", e)
        return None