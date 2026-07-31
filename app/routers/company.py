import json
import os
import uuid
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from app.models.company_schema import BusinessType, BusinessSize
from app.repositories import company_repository as repo
import cloudinary.uploader
from app.utils import cloudinary_config

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


@router.post("")
async def create_company(
    business_name: str = Form(...),
    business_type: BusinessType = Form(...),
    business_size: BusinessSize = Form(...),
    default_currency: str = Form(...),
    description: str = Form(...),
    business_email: str = Form(...),
    phone_number: str = Form(...),
    business_url: Optional[str] = Form(None),
    social_links: Optional[str] = Form(None),
    logo: UploadFile = File(...),
):
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
    default_currency: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    business_email: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    business_url: Optional[str] = Form(None),
    social_links: Optional[str] = Form(None),
    logo: Optional[UploadFile] = File(None),
):
    data = {k: v for k, v in {
        "business_name": business_name, "business_type": business_type,
        "business_size": business_size, "default_currency": default_currency,
        "description": description, "business_email": business_email,
        "phone_number": phone_number, "business_url": business_url,
    }.items() if v is not None}

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