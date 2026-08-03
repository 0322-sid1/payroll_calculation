from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class BusinessType(str, Enum):
    INFORMATION_TECHNOLOGY = "Information Technology"
    HEALTHCARE = "Healthcare"
    RETAIL = "Retail"
    MANUFACTURING = "Manufacturing"
    FINANCE = "Finance"
    EDUCATION = "Education"


class BusinessSize(str, Enum):
    SIZE_1_50 = "1 - 50 employees"
    SIZE_51_200 = "51 - 200 employees"
    SIZE_201_500 = "201 - 500 employees"
    SIZE_500_PLUS = "500+ employees"
    
class Currency(str, Enum):
    USD = "USD"
    PKR = "PKR"
    EUR = "EUR"
    GBP = "GBP"
    AED = "AED"    


class SocialLink(BaseModel):
    title: str    
    url: str


class CompanyBase(BaseModel):
    logo: Optional[str] = None
    business_name: str
    business_type: BusinessType
    business_size: BusinessSize
    default_currency: str
    description: str
    business_email: str
    phone_number: str
    business_url: Optional[str] = None
    social_links: List[SocialLink] = []


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    logo: Optional[str] = None
    business_name: Optional[str] = None
    business_type: Optional[BusinessType] = None
    business_size: Optional[BusinessSize] = None
    default_currency: Optional[str] = None
    description: Optional[str] = None
    business_email: Optional[str] = None
    phone_number: Optional[str] = None
    business_url: Optional[str] = None
    social_links: Optional[List[SocialLink]] = None

class CompanyOut(CompanyBase):
    id: str = Field(..., alias="_id")
    class Config:
        populate_by_name = True
