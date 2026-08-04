from typing import Optional
from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from pydantic import EmailStr
from app.models.company_schema import BusinessType, BusinessSize, Currency
from app.controllers import company_controller as controller

router = APIRouter(prefix="/api/company", tags=["Company"])


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
    logo: Optional[UploadFile] = File(None),
):
    return await controller.create_company(
        business_name, business_type, business_size, default_currency,
        description, business_email, phone_number, business_url, social_links, logo,
    )


@router.get("")
async def list_companies():
    return await controller.list_companies()


@router.get("/{company_id}")
async def get_company(company_id: str):
    company = await controller.get_company(company_id)
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
    updated = await controller.update_company(
        company_id, business_name, business_type, business_size, default_currency,
        description, business_email, phone_number, business_url, social_links, logo,
    )
    if not updated:
        raise HTTPException(404, "Company not found")
    return updated


@router.delete("/{company_id}")
async def delete_company(company_id: str):
    deleted = await controller.delete_company(company_id)
    if not deleted:
        raise HTTPException(404, "Company not found")
    return {"message": "Company deleted successfully"}