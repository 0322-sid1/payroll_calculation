from typing import Optional
from app.data.dummy_employees import DUMMY_EMPLOYEES

#this function call all employees of dummy data
def get_all_employees() -> list[dict]:
    return DUMMY_EMPLOYEES

#this function call employees on basis of querry
def query_employees(
    employee_type: Optional[str] = None,
    salary_type: Optional[str] = None,     
    department: Optional[str] = None,
    designation: Optional[str] = None,
    employment_type: Optional[str] = None,
) -> list[dict]:
    result = DUMMY_EMPLOYEES
#sirf wahi employees rakhta hai jinka employee type match krta hai like monthly,weekly ya hourly...upper/lower case ko ignore krta hai
    if employee_type:
        result = [e for e in result if e["employee_type"].lower() == employee_type.lower()]
#same sirf wahi employees jinka salary type match krta hai
    if salary_type:                         
        result = [e for e in result if e["salary"]["salary_type"].lower() == salary_type.lower()]

    if department:
        result = [e for e in result if e["department"].lower() == department.lower()]

    if designation:
        result = [e for e in result if e["designation"].lower() == designation.lower()]

    if employment_type:
        result = [e for e in result if e["employment_type"].lower() == employment_type.lower()]

    return result