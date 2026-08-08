import random
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.repositories import auth_repository as repo
from app.config.security import hash_password, verify_password, create_access_token
from app.config.email_service import send_otp_email


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


async def signup(name: str, email: str, password: str) -> dict:
    existing_user = await repo.get_user_by_email(email)
    if existing_user is not None:
        raise HTTPException(400, "Email already registered")

    hashed_password = hash_password(password)

    user_data = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "is_verified": False,
        "company_id": None,
    }
    await repo.create_user(user_data)

    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    await repo.save_otp(email, otp, "signup_verification", expires_at)

    await send_otp_email(email, otp)

    return {"message": "Signup successful. Please check your email for the OTP to verify your account."}


async def verify_email(email: str, otp: str) -> dict:
    otp_doc = await repo.get_valid_otp(email, otp, "signup_verification")
    if otp_doc is None:
        raise HTTPException(400, "Invalid OTP")

    if otp_doc["expires_at"] < datetime.utcnow():
        raise HTTPException(400, "OTP has expired. Please signup again to get a new OTP.")

    await repo.mark_otp_used(otp_doc["_id"])
    await repo.mark_user_verified(email)

    return {"message": "Email verified successfully. You can now login."}

async def login(email: str, password: str) -> dict:
    user = await repo.get_user_by_email(email)
    if user is None:
        raise HTTPException(400, "Invalid email or password")

    if not verify_password(password, user["password"]):
        raise HTTPException(400, "Invalid email or password")

    if not user["is_verified"]:
        raise HTTPException(400, "Please verify your email before login")

    token = create_access_token(user["_id"])

    return {
        "access_token": token,
        "name": user["name"],
        "email": user["email"],
    }



async def forgot_password(email: str) -> dict:
    user = await repo.get_user_by_email(email)
    if user is None:
        raise HTTPException(404, "No account found with this email")

    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    await repo.save_otp(email, otp, "password_reset", expires_at)

    await send_otp_email(email, otp)

    return {"message": "OTP sent to your email. Use it to reset your password."}


async def reset_password(email: str, otp: str, new_password: str) -> dict:
    otp_doc = await repo.get_valid_otp(email, otp, "password_reset")
    if otp_doc is None:
        raise HTTPException(400, "Invalid OTP")

    if otp_doc["expires_at"] < datetime.utcnow():
        raise HTTPException(400, "OTP has expired. Please try forgot password again.")

    await repo.mark_otp_used(otp_doc["_id"])

    hashed_password = hash_password(new_password)
    await repo.update_user_password(email, hashed_password)

    return {"message": "Password reset successful. You can now login with your new password."}


async def change_password(user_id: str, old_password: str, new_password: str) -> dict:
    user = await repo.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(404, "User not found")

    if not verify_password(old_password, user["password"]):
        raise HTTPException(400, "Old password is incorrect")

    hashed_password = hash_password(new_password)
    await repo.update_user_password(user["email"], hashed_password)

    return {"message": "Password changed successfully"}

async def logout(token: str) -> dict:
    await repo.blacklist_token(token)
    return {"message": "Logged out successfully"}