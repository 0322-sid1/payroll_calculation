from fastapi import APIRouter
from app.models.payroll_schema import GeneratePayrollRequest, GeneratePayrollResponse
from app.services.payroll_service import get_employees_by_ids, compute_employee_payroll, generate_payroll_id

router = APIRouter(prefix="/api/payroll", tags=["Payroll"])

#this api generate payroll of employees
@router.post("/generate", response_model=GeneratePayrollResponse)
def generate_payroll(request: GeneratePayrollRequest):
    employees = get_employees_by_ids(request.employee_ids)
    payroll_employees = [compute_employee_payroll(emp, request.pay_period) for emp in employees]

    return GeneratePayrollResponse(
        payroll_id=generate_payroll_id(str(request.pay_period.start_date)),
        payroll_type=request.payroll_type,
        employee_type=request.employee_type,
        pay_period=request.pay_period,
        employees=payroll_employees,
    )
    