from bson import ObjectId
from app.config.database import users_collection, otps_collection, blacklisted_tokens_collection


def _serialize_user(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


async def create_user(data: dict) -> dict:
    result = await users_collection.insert_one(data)
    doc = await users_collection.find_one({"_id": result.inserted_id})
    return _serialize_user(doc)


async def get_user_by_email(email: str) -> dict | None:
    doc = await users_collection.find_one({"email": email})
    if doc is None:
        return None
    return _serialize_user(doc)


async def get_user_by_id(user_id: str) -> dict | None:
    doc = await users_collection.find_one({"_id": ObjectId(user_id)})
    if doc is None:
        return None
    return _serialize_user(doc)


async def mark_user_verified(email: str) -> None:
    await users_collection.update_one({"email": email}, {"$set": {"is_verified": True}})


async def update_user_password(email: str, new_hashed_password: str) -> None:
    await users_collection.update_one({"email": email}, {"$set": {"password": new_hashed_password}})


async def set_user_company_id(user_id: str, company_id: str) -> None:
    await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"company_id": company_id}})



async def save_otp(email: str, otp: str, purpose: str, expires_at) -> None:
    await otps_collection.delete_many({"email": email, "purpose": purpose})
    await otps_collection.insert_one({
        "email": email,
        "otp": otp,
        "purpose": purpose,
        "expires_at": expires_at,
        "is_used": False,
    })


async def get_valid_otp(email: str, otp: str, purpose: str) -> dict | None:
    doc = await otps_collection.find_one({
        "email": email,
        "otp": otp,
        "purpose": purpose,
        "is_used": False,
    })
    return doc


async def mark_otp_used(otp_id) -> None:
    await otps_collection.update_one({"_id": otp_id}, {"$set": {"is_used": True}})
    

async def blacklist_token(token: str) -> None:
    await blacklisted_tokens_collection.insert_one({"token": token})


async def is_token_blacklisted(token: str) -> bool:
    doc = await blacklisted_tokens_collection.find_one({"token": token})
    if doc is None:
        return False
    return True    