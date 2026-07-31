from bson import ObjectId
from app.database import company_collection


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


async def create_company(data: dict) -> dict:
    result = await company_collection.insert_one(data)
    doc = await company_collection.find_one({"_id": result.inserted_id})
    return _serialize(doc)


async def get_all_companies() -> list[dict]:
    docs = await company_collection.find().to_list(length=None)
    return [_serialize(d) for d in docs]


async def get_company_by_id(company_id: str) -> dict | None:
    doc = await company_collection.find_one({"_id": ObjectId(company_id)})
    return _serialize(doc) if doc else None


async def update_company(company_id: str, data: dict) -> dict | None:
    await company_collection.update_one({"_id": ObjectId(company_id)}, {"$set": data})
    return await get_company_by_id(company_id)


async def delete_company(company_id: str) -> bool:
    result = await company_collection.delete_one({"_id": ObjectId(company_id)})
    return result.deleted_count > 0