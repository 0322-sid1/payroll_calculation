from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Form, File, UploadFile
from app.models.employee_schema import EmployeeOut, EmployeeListResponse, EmploymentType, EmployeeType
from app.controllers import employee_controller as controller

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.get("")
async def fetch_all_employees(company_id: str | None = None):
    employees = await controller.get_all_employees(company_id)
    return EmployeeListResponse(total=len(employees), employees=employees)


@router.get("/search")
async def search_employees(
    employee_type: Optional[str] = Query(None, description="Monthly | Weekly | Hourly"),
    salary_type: Optional[str] = Query(None, description="Monthly | Hourly"),
    department: Optional[str] = Query(None),
    designation: Optional[str] = Query(None),
    employment_type: Optional[str] = Query(None, description="Full-time | Part-time | Contract"),
    company_id: Optional[str] = Query(None),
):
    employees = await controller.query_employees(
        employee_type=employee_type, salary_type=salary_type, department=department,
        designation=designation, employment_type=employment_type, company_id=company_id,
    )
    return EmployeeListResponse(total=len(employees), employees=employees)


@router.post("", response_model=EmployeeOut)
async def create_employee(
    name: str = Form(...),
    email: str = Form(...),
    department: str = Form(...),
    designation: str = Form(...),
    employment_type: EmploymentType = Form(...),
    employee_type: EmployeeType = Form(...),
    working_hours_per_day: int = Form(...),
    company_id: str = Form(...),
    time_config: str = Form(...),
    salary: str = Form(...),
    profile_picture: Optional[UploadFile] = File(None),
):
    return await controller.create_employee(
        name, email, department, designation, employment_type, employee_type,
        working_hours_per_day, company_id, time_config, salary, profile_picture,
    )


@router.get("/{employee_id}", response_model=EmployeeOut)
async def get_employee(employee_id: str):
    employee = await controller.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(404, "Employee not found")
    return employee


@router.put("/{employee_id}", response_model=EmployeeOut)
async def update_employee(
    employee_id: str,
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    designation: Optional[str] = Form(None),
    employment_type: Optional[EmploymentType] = Form(None),
    employee_type: Optional[EmployeeType] = Form(None),
    working_hours_per_day: Optional[int] = Form(None),
    company_id: Optional[str] = Form(None),
    time_config: Optional[str] = Form(None),
    salary: Optional[str] = Form(None),
    profile_picture: Optional[UploadFile] = File(None),
):
    updated = await controller.update_employee(
        employee_id, name, email, department, designation, employment_type,
        employee_type, working_hours_per_day, company_id, time_config, salary, profile_picture,
    )
    if updated is None:
        raise HTTPException(404, "Employee not found")
    return updated


@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):
    deleted = await controller.delete_employee(employee_id)
    if not deleted:
        raise HTTPException(404, "Employee not found")
    return {"message": "Employee deleted successfully"}