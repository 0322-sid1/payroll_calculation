from app.repositories import employee_repository as repo


async def create_employee(data: dict) -> dict:
    return await repo.create_employee(data)

async def get_employees_by_ids(employee_ids: list[str]) -> list[dict]:
    return await repo.get_employees_by_ids(employee_ids)

async def update_employee(employee_id: str, data: dict) -> dict | None:
    return await repo.update_employee(employee_id, data)


async def delete_employee(employee_id: str) -> bool:
    return await repo.delete_employee(employee_id)



async def get_all_employees(company_id: str | None = None):
    return await repo.get_all_employees(company_id)


async def query_employees(employee_type=None, salary_type=None, department=None, designation=None, employment_type=None, company_id=None):
    filters = {}
    if employee_type: filters["employee_type"] = employee_type
    if salary_type: filters["salary.salary_type"] = salary_type
    if department: filters["department"] = department
    if designation: filters["designation"] = designation
    if employment_type: filters["employment_type"] = employment_type
    if company_id: filters["company_id"] = company_id
    return await repo.query_employees(filters)