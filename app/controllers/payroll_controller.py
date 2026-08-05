from app.models.payroll_schema import EmployeePayroll, AttendanceSummary, SalaryComponent, GeneratePayrollResponse
from app.controllers import attendance_controller
from app.repositories import employee_repository as emp_repo
from app.repositories import payroll_repository


async def get_employees_by_ids(employee_ids: list[str]) -> list[dict]:
    return await emp_repo.get_employees_by_ids(employee_ids)


def calculate_component_amount(item: dict, base_salary: float) -> float:
    if item["calculation_type"] == "percentage":
        return round((base_salary or 0) * (item["value"] / 100), 2)
    return item["value"]


async def compute_employee_payroll(emp: dict, pay_period) -> EmployeePayroll:
    time_config = emp["time_config"]
    salary = emp["salary"]

    attendance = await attendance_controller.get_attendance_summary(
        emp["_id"], str(pay_period.start_date), str(pay_period.end_date), time_config
    )

    overtime_pay = round(attendance["overtime_hours"] * salary["overtime_hourly_rate"], 2)
    late_deduction = round(attendance["late_arrival_hours"] * salary["late_deduction_rate"], 2)

    components: list[SalaryComponent] = []

    if emp["employee_type"] == "Hourly":
        basic_amount = round(attendance["present_days"] * emp["working_hours_per_day"] * salary["hourly_rate"], 2)
        components.append(SalaryComponent(component="Basic Salary (Hourly)", type="Earnings", amount=basic_amount))
        base_for_deductions = basic_amount
    else:
        base_salary = salary["base_salary"]
        unpaid_absent_days = max(0, attendance["leaves_taken"] - time_config["paid_leaves_allowed_per_month"])
        per_day_salary = round(base_salary / attendance["working_days"], 2) if attendance["working_days"] else 0
        leave_deduction = round(unpaid_absent_days * per_day_salary, 2)

        components.append(SalaryComponent(component="Basic Salary", type="Earnings", amount=base_salary))
        if leave_deduction > 0:
            components.append(SalaryComponent(component="Leave Deduction", type="Deduction", amount=leave_deduction))
        base_for_deductions = base_salary

    if overtime_pay > 0:
        components.append(SalaryComponent(component="Overtime Pay", type="Earnings", amount=overtime_pay))
    if late_deduction > 0:
        components.append(SalaryComponent(component="Late Arrivals", type="Deduction", amount=late_deduction))

    for benefit in salary["benefits"]:
        amount = calculate_component_amount(benefit, base_for_deductions)
        if amount > 0:
            components.append(SalaryComponent(component=benefit["name"], type="Earnings", amount=amount))

    for deduction in salary["deductions"]:
        amount = calculate_component_amount(deduction, base_for_deductions)
        if amount > 0:
            components.append(SalaryComponent(component=deduction["type"], type="Deduction", amount=amount))

    total_earnings = sum(c.amount for c in components if c.type == "Earnings")
    total_deductions = sum(c.amount for c in components if c.type == "Deduction")
    net_salary = round(total_earnings - total_deductions, 2)

    return EmployeePayroll(
        employee_id=emp["_id"],
        name=emp["name"],
        email=emp["email"],
        profile_picture=emp["profile_picture"],
        department=emp["department"],
        designation=emp["designation"],
        employment_type=emp["employment_type"],
        attendance=AttendanceSummary(**attendance),
        salary_calculation=components,
        currency=salary["currency"],
        net_salary=net_salary,
    )


async def generate_payroll(request) -> GeneratePayrollResponse:
    employees = await get_employees_by_ids(request.employee_ids)

    payroll_employees = []
    for emp in employees:
        employee_payroll = await compute_employee_payroll(emp, request.pay_period)
        payroll_employees.append(employee_payroll)

    payroll_data = {
        "payroll_type": request.payroll_type,
        "employee_type": request.employee_type,
        "pay_period": request.pay_period.model_dump(mode="json"),
        "employees": [emp.model_dump(mode="json") for emp in payroll_employees],
    }

    saved = await payroll_repository.save_payroll(payroll_data)

    return GeneratePayrollResponse(
        payroll_id=saved["_id"],   
        payroll_type=saved["payroll_type"],
        employee_type=saved["employee_type"],
        pay_period=request.pay_period,
        employees=payroll_employees,
    )
