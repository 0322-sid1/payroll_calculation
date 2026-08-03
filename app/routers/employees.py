from fastapi import APIRouter, Query
from typing import Optional
from app.models.employee_schema import EmployeeListResponse
from app.services.employee_service import get_all_employees, query_employees
from fastapi import HTTPException
from app.models.employee_schema import EmployeeOut
from app.services import employee_service
import json
import cloudinary.uploader
from fastapi import Form, File, UploadFile
from app.utils import cloudinary_config 
from app.models.employee_schema import TimeConfig, SalaryConfig, EmploymentType, EmployeeType

#define router of employees each api of this router starts from /api/employees
router = APIRouter(prefix="/api/employees", tags=["Employees"])


async def upload_profile_picture(picture: UploadFile) -> str:
    file_bytes = await picture.read()
    result = cloudinary.uploader.upload(file_bytes, folder="employee_profiles")
    return result["secure_url"]


def parse_json_field(field_name: str, value: str):
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        raise HTTPException(400, f"{field_name} must be valid JSON")


#this api fetch all employees 
@router.get("")
async def fetch_all_employees(company_id: str | None = None):
    employees = await get_all_employees(company_id)
    return EmployeeListResponse(total=len(employees), employees=employees)

#this is query serach api...search emplyee by employee type salary type department etc
@router.get("/search")
async def search_employees(
    employee_type: Optional[str] = Query(None, description="Monthly | Weekly | Hourly"),
    salary_type: Optional[str] = Query(None, description="Monthly | Hourly"),  
    department: Optional[str] = Query(None),
    designation: Optional[str] = Query(None),
    employment_type: Optional[str] = Query(None, description="Full-time | Part-time | Contract"),
):
    employees = await query_employees(
        employee_type=employee_type,
        salary_type=salary_type,            
        department=department,
        designation=designation,
        employment_type=employment_type,
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
    profile_picture: UploadFile = File(...),
):
    picture_url = await upload_profile_picture(profile_picture)

    employee_data = {
        "name": name,
        "email": email,
        "profile_picture": picture_url,
        "department": department,
        "designation": designation,
        "employment_type": employment_type,
        "employee_type": employee_type,
        "working_hours_per_day": working_hours_per_day,
        "company_id": company_id,
        "time_config": parse_json_field("time_config", time_config),
        "salary": parse_json_field("salary", salary),
    }

    created_employee = await employee_service.create_employee(employee_data)
    return created_employee


@router.get("/{employee_id}", response_model=EmployeeOut)
async def get_employee(employee_id: str):
    employees = await employee_service.get_employees_by_ids([employee_id])

    if not employees:
        raise HTTPException(404, "Employee not found")

    return employees[0]


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
    update_data = {}

    if name is not None:
        update_data["name"] = name
    if email is not None:
        update_data["email"] = email
    if department is not None:
        update_data["department"] = department
    if designation is not None:
        update_data["designation"] = designation
    if employment_type is not None:
        update_data["employment_type"] = employment_type
    if employee_type is not None:
        update_data["employee_type"] = employee_type
    if working_hours_per_day is not None:
        update_data["working_hours_per_day"] = working_hours_per_day
    if company_id is not None:
        update_data["company_id"] = company_id
    if time_config is not None:
        update_data["time_config"] = parse_json_field("time_config", time_config)
    if salary is not None:
        update_data["salary"] = parse_json_field("salary", salary)
    if profile_picture is not None:
        update_data["profile_picture"] = await upload_profile_picture(profile_picture)

    updated_employee = await employee_service.update_employee(employee_id, update_data)

    if updated_employee is None:
        raise HTTPException(404, "Employee not found")

    return updated_employee


@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):
    deleted = await employee_service.delete_employee(employee_id)

    if not deleted:
        raise HTTPException(404, "Employee not found")

    return {"message": "Employee deleted successfully"}
