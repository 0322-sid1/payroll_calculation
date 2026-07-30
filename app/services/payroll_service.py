from uuid import uuid4
from app.data.dummy_employees import DUMMY_EMPLOYEES
from app.models.payroll_schema import EmployeePayroll, AttendanceSummary, SalaryComponent
from app.services.attendance_service import calculate_attendance_summary
from app.data.attendance_generator import generate_working_dates, generate_attendance_log

#return employees on the basis of id if no id then return all employees
def get_employees_by_ids(employee_ids: list[str]) -> list[dict]:
    if not employee_ids:
        return DUMMY_EMPLOYEES
    return [e for e in DUMMY_EMPLOYEES if e["employee_id"] in employee_ids]

#Benefit ya deduction ki actual amount calculate krta hai 
def calculate_component_amount(item: dict, base_salary: float) -> float:
    #if calculation type is percentage then multiply base salary with percent and then divide by 100 at the end round off complete value by 2 decimal places
    #otherwise return value
    if item["calculation_type"] == "percentage":
        return round((base_salary or 0) * (item["value"] / 100), 2)
    return item["value"]

#compute employee payroll by taaking time_config from dummy data and attendance profile
def compute_employee_payroll(emp: dict, pay_period) -> EmployeePayroll:  
    time_config = emp["time_config"]
    profile = emp["attendance_profile"]
#here we call generate wotking dates, attendance log function and attendance summary which we define in attendance generator file
    dates = generate_working_dates(
        str(pay_period.start_date), str(pay_period.end_date), time_config["working_days_per_week"]
    )
    log = generate_attendance_log(
        seed=profile["seed"], dates=dates,
        standard_clock_in=time_config["standard_clock_in"],
        standard_clock_out=time_config["standard_clock_out"],
        absent_days=profile["absent_days"], late_days=profile["late_days"], overtime_days=profile["overtime_days"],
    )
    attendance = calculate_attendance_summary(log, time_config)
    salary = emp["salary"]
    time_config = emp["time_config"]

    overtime_pay = round(attendance["overtime_hours"] * salary["overtime_hourly_rate"], 2)
    late_deduction = round(attendance["late_arrival_hours"] * salary["late_deduction_rate"], 2)
#here we make an empty list in which every salary component like base salary,overtime,deductions benefits etc should be added
    components: list[SalaryComponent] = []
#if employee is hourly then his salary calculate accordingly if monthly then run else block
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
  #here we calculate total earnings total deductions and then net salary 

    total_earnings = sum(c.amount for c in components if c.type == "Earnings")
    total_deductions = sum(c.amount for c in components if c.type == "Deduction")
    net_salary = round(total_earnings - total_deductions, 2)

    return EmployeePayroll(
        employee_id=emp["employee_id"],
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

#generate 6 digit uppercase unique random payroll_id for each employee take first 7 characters of pay period start date that include year and month
def generate_payroll_id(pay_period_start: str) -> str:
    return f"PR-{pay_period_start[:7]}-{uuid4().hex[:6].upper()}"