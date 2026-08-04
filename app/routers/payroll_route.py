from fastapi import APIRouter
from app.models.payroll_schema import GeneratePayrollRequest, GeneratePayrollResponse
from app.controllers import payroll_controller as controller

router = APIRouter(prefix="/api/payroll", tags=["Payroll"])


@router.post("/generate", response_model=GeneratePayrollResponse)
async def generate_payroll(request: GeneratePayrollRequest):
    return await controller.generate_payroll(request)