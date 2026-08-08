from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.security import decode_access_token
from app.repositories import auth_repository as repo

bearer_scheme = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    token = credentials.credentials

    is_blacklisted = await repo.is_token_blacklisted(token)
    if is_blacklisted:
        raise HTTPException(401, "This token has been logged out. Please login again.")

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(401, "Invalid or expired token")

    user = await repo.get_user_by_id(payload["user_id"])
    if user is None:
        raise HTTPException(401, "User not found")

    return user