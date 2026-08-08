import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24


def hash_password(password: str) -> str:
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(user_id: str) -> str:
    expire_time = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {"user_id": user_id, "exp": expire_time}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None