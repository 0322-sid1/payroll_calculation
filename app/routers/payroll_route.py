from fastapi import APIRouter, HTTPException, Depends
from app.models.payroll_schema import GeneratePayrollRequest, GeneratePayrollResponse
from app.controllers import payroll_controller as controller
from app.config.dependencies import get_current_user

router = APIRouter(prefix="/api/payroll", tags=["Payroll"])


@router.post("/generate", response_model=GeneratePayrollResponse)
async def generate_payroll(request: GeneratePayrollRequest, current_user: dict = Depends(get_current_user)):
    return await controller.generate_payroll(request, current_user)


@router.delete("/{payroll_id}")
async def delete_payroll(payroll_id: str, current_user: dict = Depends(get_current_user)):
    deleted = await controller.delete_payroll(payroll_id, current_user)
    if not deleted:
        raise HTTPException(404, "Payroll not found")
    return {"message": "Payroll deleted successfully"}


