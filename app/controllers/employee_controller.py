import json
from typing import Optional
from fastapi import HTTPException, UploadFile
import cloudinary.uploader
from app.config import cloudinary_config   # <-- config/ move ke baad
from app.repositories import employee_repository as repo


async def upload_profile_picture(picture: UploadFile) -> str:
    file_bytes = await picture.read()
    result = cloudinary.uploader.upload(file_bytes, folder="employee_profiles")
    return result["secure_url"]


def parse_json_field(field_name: str, value: str):
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        raise HTTPException(400, f"{field_name} must be valid JSON")


async def create_employee(
    name, email, department, designation, employment_type, employee_type,
    working_hours_per_day, company_id, time_config, salary, profile_picture,
) -> dict:
    picture_url = await upload_profile_picture(profile_picture) if profile_picture else None
    data = {
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
    return await repo.create_employee(data)


# async def get_employee_by_id(employee_id: str) -> dict | None:
#     employees = await repo.get_employees_by_ids([employee_id])
#     return employees[0] if employees else None


async def get_employees_by_ids(employee_ids: list[str]) -> list[dict]:
    return await repo.get_employees_by_ids(employee_ids)


async def get_all_employees(company_id: str | None = None) -> list[dict]:
    return await repo.get_all_employees(company_id)


async def query_employees(employee_type=None, salary_type=None, department=None,
                           designation=None, employment_type=None, company_id=None) -> list[dict]:
    filters = {}
    if employee_type: filters["employee_type"] = employee_type
    if salary_type: filters["salary.salary_type"] = salary_type
    if department: filters["department"] = department
    if designation: filters["designation"] = designation
    if employment_type: filters["employment_type"] = employment_type
    if company_id: filters["company_id"] = company_id
    return await repo.query_employees(filters)


async def update_employee(
    employee_id, name, email, department, designation, employment_type,
    employee_type, working_hours_per_day, company_id, time_config, salary, profile_picture,
) -> dict | None:
    data = {}
    if name is not None: data["name"] = name
    if email is not None: data["email"] = email
    if department is not None: data["department"] = department
    if designation is not None: data["designation"] = designation
    if employment_type is not None: data["employment_type"] = employment_type
    if employee_type is not None: data["employee_type"] = employee_type
    if working_hours_per_day is not None: data["working_hours_per_day"] = working_hours_per_day
    if company_id is not None: data["company_id"] = company_id
    if time_config is not None: data["time_config"] = parse_json_field("time_config", time_config)
    if salary is not None: data["salary"] = parse_json_field("salary", salary)
    if profile_picture is not None: data["profile_picture"] = await upload_profile_picture(profile_picture)

    return await repo.update_employee(employee_id, data)


async def delete_employee(employee_id: str) -> bool:
    return await repo.delete_employee(employee_id)