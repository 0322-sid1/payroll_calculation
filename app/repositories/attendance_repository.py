from app.config.database import attendance_collection


def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc["_id"])
    doc.pop("_id")
    return doc

#this function creates attendance record in database and returns the created attendance document
async def create_attendance_record(data: dict) -> dict:
    result = await attendance_collection.insert_one(data)
    doc = await attendance_collection.find_one({"_id": result.inserted_id})
    return _serialize(doc)

#this function fetches attendance records for an employee within a date range
async def get_attendance_records(employee_id: str, start_date: str, end_date: str) -> list[dict]:
    query = {
        "employee_id": employee_id,
        #this query fetches records where date is greater than or equal to start_date and less than or equal to end_date
        "date": {"$gte": start_date, "$lte": end_date},
    }
    #fetches attendance records from database and sort them by date in ascending order
    docs = await attendance_collection.find(query).sort("date", 1).to_list(length=None)
    records = []
    for doc in docs:
        records.append(_serialize(doc))
    return records















# async def get_attendance_summary(
#     employee_id: str,
#     start_date: str,
#     end_date: str,
#     standard_in_min: int,
#     standard_out_min: int,
# ) -> dict:
#     pipeline = [
#         {"$match": {
#             "employee_id": employee_id,
#             "date": {"$gte": start_date, "$lte": end_date},
#         }},
#         {"$addFields": {
#             "in_min": {
#                 "$cond": [
#                     {"$eq": ["$status", "present"]},
#                     {"$add": [
#                         {"$multiply": [{"$toInt": {"$arrayElemAt": [{"$split": ["$clock_in", ":"]}, 0]}}, 60]},
#                         {"$toInt": {"$arrayElemAt": [{"$split": ["$clock_in", ":"]}, 1]}},
#                     ]},
#                     None,
#                 ]
#             },
#             "out_min": {
#                 "$cond": [
#                     {"$eq": ["$status", "present"]},
#                     {"$add": [
#                         {"$multiply": [{"$toInt": {"$arrayElemAt": [{"$split": ["$clock_out", ":"]}, 0]}}, 60]},
#                         {"$toInt": {"$arrayElemAt": [{"$split": ["$clock_out", ":"]}, 1]}},
#                     ]},
#                     None,
#                 ]
#             },
#         }},
#         {"$group": {
#             "_id": None,
#             "working_days": {"$sum": 1},
#             "present_days": {"$sum": {"$cond": [{"$eq": ["$status", "present"]}, 1, 0]}},
#             "leaves_taken": {"$sum": {"$cond": [{"$eq": ["$status", "absent"]}, 1, 0]}},
#             "late_minutes_total": {
#                 "$sum": {"$cond": [
#                     {"$and": [{"$eq": ["$status", "present"]}, {"$gt": ["$in_min", standard_in_min]}]},
#                     {"$subtract": ["$in_min", standard_in_min]},
#                     0,
#                 ]}
#             },
#             "overtime_minutes_total": {
#                 "$sum": {"$cond": [
#                     {"$and": [{"$eq": ["$status", "present"]}, {"$gt": ["$out_min", standard_out_min]}]},
#                     {"$subtract": ["$out_min", standard_out_min]},
#                     0,
#                 ]}
#             },
#         }},
#     ]

#     result = await attendance_collection.aggregate(pipeline).to_list(length=None)

#     if not result:
#         return {
#             "working_days": 0,
#             "present_days": 0,
#             "leaves_taken": 0,
#             "overtime_hours": 0.0,
#             "late_arrival_hours": 0.0,
#         }

#     doc = result[0]
#     return {
#         "working_days": doc["working_days"],
#         "present_days": doc["present_days"],
#         "leaves_taken": doc["leaves_taken"],
#         "overtime_hours": round(doc["overtime_minutes_total"] / 60, 2),
#         "late_arrival_hours": round(doc["late_minutes_total"] / 60, 2),
#     }



#     # doc.pop("_id")
