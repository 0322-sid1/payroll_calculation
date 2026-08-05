from app.config.database import payroll_collection 
from bson import ObjectId

def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


async def save_payroll(data: dict) -> dict:
    result = await payroll_collection.insert_one(data)
    doc = await payroll_collection.find_one({"_id": result.inserted_id})
    return _serialize(doc)

async def get_payroll_by_id(payroll_id: str) -> dict | None:
    doc = await payroll_collection.find_one({"_id": ObjectId(payroll_id)})  
    return _serialize(doc) if doc else None


