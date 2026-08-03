from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class EmploymentType(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"


class EmployeeType(str, Enum):
    MONTHLY = "Monthly"
    WEEKLY = "Weekly"
    HOURLY = "Hourly"


class SalaryType(str, Enum):
    MONTHLY = "Monthly"
    HOURLY = "Hourly"


class CalculationType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"


class DeductionType(str, Enum):
    UIF = "UIF"
    INCOME_TAX = "Income Tax"


class BenefitType(str, Enum):
    PICK_AND_DROP = "Pick and Drop Service"
    EXPENSES = "Expenses"


class TimeConfig(BaseModel):
    working_days_per_week: int
    standard_clock_in: str
    standard_clock_out: str
    paid_leaves_allowed_per_month: int


class BenefitItem(BaseModel):
    name: BenefitType
    calculation_type: CalculationType
    value: float


class DeductionItem(BaseModel):
    type: DeductionType
    calculation_type: CalculationType
    value: float


class SalaryConfig(BaseModel):
    salary_type: SalaryType
    base_salary: Optional[float] = None
    hourly_rate: Optional[float] = None
    currency: str
    pay_period_start_date: str
    payment_method: str
    overtime_hourly_rate: float
    late_deduction_rate: float
    benefits: List[BenefitItem] = []
    deductions: List[DeductionItem] = []


class AttendanceProfile(BaseModel):
    seed: int
    absent_days: int
    late_days: int
    overtime_days: int



class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    profile_picture: Optional[str] = None
    department: str
    designation: str
    employment_type: EmploymentType
    employee_type: EmployeeType
    working_hours_per_day: int
    company_id: str
    time_config: TimeConfig
    salary: SalaryConfig


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_picture: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    employee_type: Optional[EmployeeType] = None
    working_hours_per_day: Optional[int] = None
    company_id: Optional[str] = None
    time_config: Optional[TimeConfig] = None
    salary: Optional[SalaryConfig] = None


class EmployeeOut(EmployeeCreate):
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True


class EmployeeListResponse(BaseModel):
    total: int
    employees: List[EmployeeOut]