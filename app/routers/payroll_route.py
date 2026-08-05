from fastapi import APIRouter
from app.models.payroll_schema import GeneratePayrollRequest, GeneratePayrollResponse
from app.controllers import payroll_controller as controller
from app.repositories import payroll_repository
from fastapi import HTTPException


router = APIRouter(prefix="/api/payroll", tags=["Payroll"])


@router.post("/generate", response_model=GeneratePayrollResponse)
async def generate_payroll(request: GeneratePayrollRequest):
    return await controller.generate_payroll(request)

@router.get("/{payroll_id}")
async def get_payroll(payroll_id: str):
    payroll = await payroll_repository.get_payroll_by_id(payroll_id)
    if not payroll:
        raise HTTPException(404, "Payroll not found")
    return payroll

