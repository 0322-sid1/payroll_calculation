import json
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from app.models.company_schema import BusinessType, BusinessSize
from app.repositories import company_repository as repo
import cloudinary.uploader
from app.utils import cloudinary_config
from app.models.company_schema import BusinessType, BusinessSize, Currency
from pydantic import EmailStr
import re            

router = APIRouter(prefix="/api/company", tags=["Company"])


async def save_logo(logo: UploadFile) -> str:
    file_bytes = await logo.read()
    result = cloudinary.uploader.upload(file_bytes, folder="company_logos")
    return result["secure_url"]

def parse_social_links(social_links: Optional[str]) -> List[dict]:
    if not social_links:
        return []
    try:
        return json.loads(social_links)
    except json.JSONDecodeError:
        raise HTTPException(400, 'social_links must be JSON, e.g. [{"title":"twitter","url":"..."}]')

def validate_phone(phone: str) -> str:
    if not re.fullmatch(r"^\+?\d{7,15}$", phone):
        raise HTTPException(422, "Invalid phone number format")
    return phone

@router.post("")
async def create_company(
    business_name: str = Form(...),
    business_type: BusinessType = Form(...),
    business_size: BusinessSize = Form(...),
    default_currency: Currency = Form(...),
    description: str = Form(...),
    business_email: EmailStr = Form(...),
    phone_number: str = Form(...),
    business_url: Optional[str] = Form(None),
    social_links: Optional[str] = Form(None),
    logo: UploadFile = File(...),
):
    phone_number = validate_phone(phone_number)
    data = {
        "logo": await save_logo(logo),
        "business_name": business_name,
        "business_type": business_type,
        "business_size": business_size,
        "default_currency": default_currency,
        "description": description,
        "business_email": business_email,
        "phone_number": phone_number,
        "business_url": business_url,
        "social_links": parse_social_links(social_links),
    }
    return await repo.create_company(data)


@router.get("")
async def list_companies():
    return await repo.get_all_companies()


@router.get("/{company_id}")
async def get_company(company_id: str):
    company = await repo.get_company_by_id(company_id)
    if not company:
        raise HTTPException(404, "Company not found")
    return company


@router.put("/{company_id}")
async def update_company(
    company_id: str,
    business_name: Optional[str] = Form(None),
    business_type: Optional[BusinessType] = Form(None),
    business_size: Optional[BusinessSize] = Form(None),
    default_currency: Optional[Currency] = Form(None),
    description: Optional[str] = Form(None),
    business_email: Optional[EmailStr] = Form(None),
    phone_number: Optional[str] = Form(None),
    business_url: Optional[str] = Form(None),
    social_links: Optional[str] = Form(None),
    logo: Optional[UploadFile] = File(None),
):
    data = {}

    if business_name is not None:
        data["business_name"] = business_name
    if business_type is not None:
        data["business_type"] = business_type
    if business_size is not None:
        data["business_size"] = business_size
    if default_currency is not None:
        data["default_currency"] = default_currency
    if description is not None:
        data["description"] = description
    if business_email is not None:
        data["business_email"] = business_email
    if phone_number is not None:
        phone_number = validate_phone(phone_number)
        data["phone_number"] = phone_number
    if business_url is not None:
        data["business_url"] = business_url


    if social_links is not None:
        data["social_links"] = parse_social_links(social_links)
    if logo is not None:
        data["logo"] = await save_logo(logo)

    updated = await repo.update_company(company_id, data)
    if not updated:
        raise HTTPException(404, "Company not found")
    return updated


@router.delete("/{company_id}")
async def delete_company(company_id: str):
    deleted = await repo.delete_company(company_id)
    if not deleted:
        raise HTTPException(404, "Company not found")
    return {"message": "Company deleted successfully"}