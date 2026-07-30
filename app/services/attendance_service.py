def _time_to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m

#this function calculate complete attendance of employee by taking in out time working days present days absent days overtime mins etc
def calculate_attendance_summary(attendance_log: list[dict], time_config: dict) -> dict:
    
    standard_in_min = _time_to_minutes(time_config["standard_clock_in"])
    standard_out_min = _time_to_minutes(time_config["standard_clock_out"])

    working_days = len(attendance_log)
    present_days = 0
    leaves_taken = 0          
    late_minutes_total = 0
    overtime_minutes_total = 0
#agr employee kisi din absent hai to leave mai add ho jay ga or bs usky liay next kuch calculate ni ho ga loop end ho jay gi
#agr present hai tp present day mai add ho ga or next clock in or out b calculate hon gyn
    for day in attendance_log:
        if day["status"] == "absent":
            leaves_taken += 1
            continue

        present_days += 1
        actual_in_min = _time_to_minutes(day["clock_in"])
        actual_out_min = _time_to_minutes(day["clock_out"])

        if actual_in_min > standard_in_min:
            late_minutes_total += (actual_in_min - standard_in_min)
        if actual_out_min > standard_out_min:
            overtime_minutes_total += (actual_out_min - standard_out_min)

    return {
        "working_days": working_days,
        "present_days": present_days,
        "leaves_taken": leaves_taken,
        "overtime_hours": round(overtime_minutes_total / 60, 2),
        "late_arrival_hours": round(late_minutes_total / 60, 2),
    }