from fastapi import APIRouter, Query
from typing import Optional
from app.models.employee_schema import EmployeeListResponse
from app.services.employee_service import get_all_employees, query_employees

# from datetime import date
# from fastapi import HTTPException
# from app.data.dummy_employees import DUMMY_EMPLOYEES
# from app.data.attendance_generator import generate_working_dates, generate_attendance_log


#define router of employees each api of this router starts from /api/employees
router = APIRouter(prefix="/api/employees", tags=["Employees"])

#this api fetch all employees 
@router.get("", response_model=EmployeeListResponse)
def fetch_all_employees():
    employees = get_all_employees()
    return EmployeeListResponse(total=len(employees), employees=employees)

#this is query serach api...search emplyee by employee type salary type department etc
@router.get("/search", response_model=EmployeeListResponse)
def search_employees(
    employee_type: Optional[str] = Query(None, description="Monthly | Weekly | Hourly"),
    salary_type: Optional[str] = Query(None, description="Monthly | Hourly"),  
    department: Optional[str] = Query(None),
    designation: Optional[str] = Query(None),
    employment_type: Optional[str] = Query(None, description="Full-time | Part-time | Contract"),
):
    employees = query_employees(
        employee_type=employee_type,
        salary_type=salary_type,            
        department=department,
        designation=designation,
        employment_type=employment_type,
    )
    return EmployeeListResponse(total=len(employees), employees=employees)




# @router.get("/{employee_id}/attendance-log")
# def get_attendance_log(employee_id: str, start_date: date, end_date: date):
#     emp = next((e for e in DUMMY_EMPLOYEES if e["employee_id"] == employee_id), None)
#     if not emp:
#         raise HTTPException(status_code=404, detail="Employee not found")

#     time_config = emp["time_config"]
#     profile = emp["attendance_profile"]

#     dates = generate_working_dates(str(start_date), str(end_date), time_config["working_days_per_week"])
#     log = generate_attendance_log(
#         seed=profile["seed"], dates=dates,
#         standard_clock_in=time_config["standard_clock_in"],
#         standard_clock_out=time_config["standard_clock_out"],
#         absent_days=profile["absent_days"], late_days=profile["late_days"], overtime_days=profile["overtime_days"],
#     )
#     return {"employee_id": employee_id, "total_days": len(dates), "attendance_log": log}