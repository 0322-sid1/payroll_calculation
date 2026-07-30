import random
from datetime import datetime, timedelta

#this function converts time to minutes bcz we have to calculate the standard in and out time of employees in minutes.
def _time_to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m

#this function is opposite of above bcz at the end we should return exact time like 9:30 
def _minutes_to_time(mins: int) -> str:
    h, m = divmod(mins % (24 * 60), 60)
    return f"{h:02d}:{m:02d}"

#this function generates total working dates from start date to end date without weekends
def generate_working_dates(start_date: str, end_date: str, working_days_per_week: int) -> list[str]:
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    allowed_weekdays = set(range(6)) if working_days_per_week >= 6 else set(range(5))  # Mon-Sat vs Mon-Fri

    dates = []
    current = start
    while current <= end:
        if current.weekday() in allowed_weekdays:
            dates.append(current.isoformat())
        current += timedelta(days=1)
    return dates

#This function calculate attendance of employees randomly select absent,late,overtime and set in and out timing of employees for total working days
def generate_attendance_log(
    seed: int,
    dates: list[str],
    standard_clock_in: str,
    standard_clock_out: str,
    absent_days: int = 0,
    late_days: int = 0,
    overtime_days: int = 0,
) -> list[dict]:
    rng = random.Random(seed)
    total_days = len(dates)
    standard_in_min = _time_to_minutes(standard_clock_in)
    standard_out_min = _time_to_minutes(standard_clock_out)
#assign indexes to total working days start from 0
    day_indexes = list(range(total_days))
    absent_set = set(rng.sample(day_indexes, min(absent_days, total_days)))
    remaining = [d for d in day_indexes if d not in absent_set]
    late_set = set(rng.sample(remaining, min(late_days, len(remaining))))
    remaining_for_ot = [d for d in remaining if d not in late_set]
    overtime_set = set(rng.sample(remaining_for_ot, min(overtime_days, len(remaining_for_ot))))
#save attendance for each day
    log = []
    for idx, date_str in enumerate(dates):
        if idx in absent_set:
            log.append({"date": date_str, "status": "absent", "clock_in": None, "clock_out": None})
            continue

        clock_in_min = standard_in_min
        clock_out_min = standard_out_min
        if idx in late_set:
            clock_in_min += rng.randint(15, 45)
        if idx in overtime_set:
            clock_out_min += rng.randint(30, 90)

        log.append({
            "date": date_str,
            "status": "present",
            "clock_in": _minutes_to_time(clock_in_min),
            "clock_out": _minutes_to_time(clock_out_min),
        })
    return log