import json
import re
from typing import Optional, List
from fastapi import HTTPException, UploadFile
import cloudinary.uploader
from app.config import cloudinary_config  
from app.repositories import company_repository as repo
from app.repositories import auth_repository as auth_repo


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
    current_user: dict,
    business_name, business_type, business_size, default_currency,
    description, business_email, phone_number, business_url, social_links, logo,
) -> dict:
    if current_user.get("company_id") is not None:
        raise HTTPException(400, "You already have a company. One user can create only one company.")

    phone_number = validate_phone(phone_number)

    logo_url = None
    if logo is not None:
        logo_url = await save_logo(logo)

    data = {
        "logo": logo_url,
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
    created_company = await repo.create_company(data)

    await auth_repo.set_user_company_id(current_user["_id"], created_company["_id"])

    return created_company


# async def list_companies() -> list[dict]:
#     return await repo.get_all_companies()


async def get_company(current_user: dict, company_id: str) -> dict | None:
    company = await repo.get_company_by_id(company_id)
    if company is None:
        return None
    if company["_id"] != current_user.get("company_id"):
        raise HTTPException(403, "You are not allowed to access this company")
    return company


async def update_company(
    current_user, company_id, business_name, business_type, business_size, default_currency,
    description, business_email, phone_number, business_url, social_links, logo,
) -> dict | None:
    existing_company = await repo.get_company_by_id(company_id)
    if existing_company is None:
        return None
    if existing_company["_id"] != current_user.get("company_id"):
        raise HTTPException(403, "You are not allowed to update this company")

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


async def delete_company(current_user: dict, company_id: str) -> bool:
    existing_company = await repo.get_company_by_id(company_id)
    if existing_company is None:
        return False
    if existing_company["_id"] != current_user.get("company_id"):
        raise HTTPException(403, "You are not allowed to delete this company")

    return await repo.delete_company(company_id)


