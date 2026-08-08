from fastapi import APIRouter, Depends
from app.models.auth_schema import SignupRequest, VerifyEmailRequest, LoginRequest, ForgotPasswordRequest, ResetPasswordRequest, ChangePasswordRequest, TokenResponse
from app.controllers import auth_controller as controller
from fastapi.security import HTTPAuthorizationCredentials
from app.config.dependencies import get_current_user, bearer_scheme


router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/signup")
async def signup(payload: SignupRequest):
    return await controller.signup(payload.name, payload.email, payload.password)


@router.post("/verify-email")
async def verify_email(payload: VerifyEmailRequest):
    return await controller.verify_email(payload.email, payload.otp)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    return await controller.login(payload.email, payload.password)


@router.post("/forgot-password")
async def forgot_password(payload: ForgotPasswordRequest):
    return await controller.forgot_password(payload.email)


@router.post("/reset-password")
async def reset_password(payload: ResetPasswordRequest):
    return await controller.reset_password(payload.email, payload.otp, payload.new_password)


@router.post("/change-password")
async def change_password(payload: ChangePasswordRequest, current_user: dict = Depends(get_current_user)):
    return await controller.change_password(current_user["_id"], payload.old_password, payload.new_password)


@router.post("/logout")
async def logout(
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = credentials.credentials
    return await controller.logout(token)


