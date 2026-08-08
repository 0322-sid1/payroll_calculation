from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://sidra_1234:Sidra123456@cluster0.sfywbvo.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URI)
db = client["payroll_db"]
company_collection = db["companies"]
employee_collection = db["employees"]
attendance_collection = db["attendance_records"]
payroll_collection = db["payrolls"]
users_collection = db["users"]
otps_collection = db["otps"]
blacklisted_tokens_collection = db["blacklisted_tokens"]