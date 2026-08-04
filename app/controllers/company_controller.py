import json
import re
from typing import Optional, List
from fastapi import HTTPException, UploadFile
import cloudinary.uploader
from app.config import cloudinary_config  
from app.repositories import company_repository as repo


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


async def create_company(
    business_name, business_type, business_size, default_currency,
    description, business_email, phone_number, business_url, social_links, logo,
) -> dict:
    phone_number = validate_phone(phone_number)
    data = {
        "logo": await save_logo(logo) if logo else None,
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


async def list_companies() -> list[dict]:
    return await repo.get_all_companies()


async def get_company(company_id: str) -> dict | None:
    return await repo.get_company_by_id(company_id)


async def update_company(
    company_id, business_name, business_type, business_size, default_currency,
    description, business_email, phone_number, business_url, social_links, logo,
) -> dict | None:
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
        data["phone_number"] = validate_phone(phone_number)
    if business_url is not None:
        data["business_url"] = business_url
    if social_links is not None:
        data["social_links"] = parse_social_links(social_links)
    if logo is not None:
        data["logo"] = await save_logo(logo)

    return await repo.update_company(company_id, data)


async def delete_company(company_id: str) -> bool:
    return await repo.delete_company(company_id)