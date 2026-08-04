from app.config.database import employee_collection
from bson import ObjectId

#this function converts the objectid to string bcz fastapi cannot directly return objectid
def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc

#this function creates employee in database and returns the created employee document
async def create_employee(data: dict) -> dict:
    result = await employee_collection.insert_one(data)
    doc = await employee_collection.find_one({"_id": result.inserted_id})
    return _serialize(doc)

#
async def get_employees_by_ids(employee_ids: list[str]) -> list[dict]:
    if not employee_ids:
        docs = await employee_collection.find().to_list(length=None)
    else:
        object_ids = []
        for eid in employee_ids:
            object_ids.append(ObjectId(eid))
        docs = await employee_collection.find({"_id": {"$in": object_ids}}).to_list(length=None)

    employees = []
    for doc in docs:
        employees.append(_serialize(doc))
    return employees


async def update_employee(employee_id: str, data: dict) -> dict | None:
    await employee_collection.update_one({"_id": ObjectId(employee_id)}, {"$set": data})
    doc = await employee_collection.find_one({"_id": ObjectId(employee_id)})
    return _serialize(doc) if doc else None


async def delete_employee(employee_id: str) -> bool:
    result = await employee_collection.delete_one({"_id": ObjectId(employee_id)})
    return result.deleted_count > 0


# async def get_all_employees(company_id: str | None = None) -> list[dict]:
#     query = {"company_id": company_id} if company_id else {}
#     docs = await employee_collection.find(query).to_list(length=None)
#     return [_serialize(d) for d in docs]



async def query_employees(filters: dict) -> list[dict]:
    docs = await employee_collection.find(filters).to_list(length=None)
    return [_serialize(d) for d in docs]