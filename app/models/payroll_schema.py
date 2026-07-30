from pydantic import BaseModel
from typing import List, Literal
from datetime import date

class PayPeriod(BaseModel):
    start_date: date
    end_date: date

class GeneratePayrollRequest(BaseModel):
    payroll_type: Literal["Monthly", "Weekly"]
    employee_type: Literal["Monthly", "Weekly", "Hourly"]
    pay_period: PayPeriod
    employee_ids: List[str] = [] 

class SalaryComponent(BaseModel):
    component: str
    type: Literal["Earnings", "Deduction"]
    amount: float

class AttendanceSummary(BaseModel):
    working_days: int
    present_days: int
    leaves_taken: int
    overtime_hours: float
    late_arrival_hours: float

class EmployeePayroll(BaseModel):
    employee_id: str
    name: str
    email: str
    profile_picture: str
    department: str
    designation: str
    employment_type: str
    attendance: AttendanceSummary
    salary_calculation: List[SalaryComponent]
    currency: str
    net_salary: float

class GeneratePayrollResponse(BaseModel):
    payroll_id: str
    payroll_type: str
    employee_type: str
    pay_period: PayPeriod
    employees: List[EmployeePayroll]