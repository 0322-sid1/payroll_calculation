from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class TimeConfig(BaseModel):
    working_days_per_week: int
    standard_clock_in: str
    standard_clock_out: str
    paid_leaves_allowed_per_month: int
    
class CalculationType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"


class DeductionType(str, Enum):
    UIF = "UIF"
    INCOME_TAX = "Income Tax"


class BenefitType(str, Enum):
    PICK_AND_DROP = "Pick and Drop Service"
    EXPENSES = "Expenses"


class BenefitItem(BaseModel):
    name: BenefitType
    calculation_type: CalculationType   
    value: float                         


class DeductionItem(BaseModel):
    type: DeductionType                  
    calculation_type: CalculationType    
    value: float    

class SalaryConfig(BaseModel):
    salary_type: str
    base_salary: Optional[float]
    hourly_rate: Optional[float]
    currency: str
    pay_period_start_date: str
    payment_method: str
    overtime_hourly_rate: float
    late_deduction_rate: float
    benefits: List[BenefitItem]
    deductions: List[DeductionItem]

class EmployeeProfile(BaseModel):
    employee_id: str
    name: str
    email: str
    profile_picture: str
    department: str
    designation: str
    employment_type: str
    employee_type: str
    working_hours_per_day: int
    time_config: TimeConfig
    salary: SalaryConfig

class EmployeeListResponse(BaseModel):
    total: int
    employees: List[EmployeeProfile]
    
    



    