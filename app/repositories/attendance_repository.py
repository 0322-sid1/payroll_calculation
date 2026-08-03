from app.database import attendance_collection


def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc["_id"])
    doc.pop("_id")
    return doc


async def create_attendance_record(data: dict) -> dict:
    result = await attendance_collection.insert_one(data)
    doc = await attendance_collection.find_one({"_id": result.inserted_id})
    return _serialize(doc)


async def get_attendance_records(employee_id: str, start_date: str, end_date: str) -> list[dict]:
    query = {
        "employee_id": employee_id,
        "date": {"$gte": start_date, "$lte": end_date},
    }
    docs = await attendance_collection.find(query).sort("date", 1).to_list(length=None)
    records = []
    for doc in docs:
        records.append(_serialize(doc))
    return records
