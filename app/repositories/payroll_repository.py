from bson import ObjectId
from app.config.database import payroll_collection


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


async def save_payroll(data: dict) -> dict:
    result = await payroll_collection.insert_one(data)
    doc = await payroll_collection.find_one({"_id": result.inserted_id})
    return _serialize(doc)


async def get_payroll_by_id(payroll_id: str) -> dict | None:
    doc = await payroll_collection.find_one({"_id": ObjectId(payroll_id)})
    if doc is None:
        return None
    return _serialize(doc)


async def get_all_payrolls() -> list[dict]:
    docs = await payroll_collection.find().to_list(length=None)
    return [_serialize(d) for d in docs]


async def get_payroll_by_company_and_month(company_id: str, month: str) -> dict | None:
    doc = await payroll_collection.find_one({"company_id": company_id, "month": month})
    if doc is None:
        return None
    return _serialize(doc)


async def delete_payroll(payroll_id: str) -> bool:
    result = await payroll_collection.delete_one({"_id": ObjectId(payroll_id)})
    if result.deleted_count > 0:
        return True
    return False