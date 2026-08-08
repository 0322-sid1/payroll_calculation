from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class VerifyEmailRequest(BaseModel):
    email: EmailStr
    otp: str
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
    
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    
class TokenResponse(BaseModel):
    access_token: str
    name: str
    email: str    

