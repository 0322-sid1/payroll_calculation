from app.repositories import attendance_repository as repo


def time_to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m


async def create_attendance_record(data: dict) -> dict:
    return await repo.create_attendance_record(data)


async def get_attendance_records(employee_id: str, start_date: str, end_date: str) -> list[dict]:
    return await repo.get_attendance_records(employee_id, start_date, end_date)


async def get_attendance_summary(employee_id: str, start_date: str, end_date: str, time_config: dict) -> dict:
    standard_in_min = time_to_minutes(time_config["standard_clock_in"])
    standard_out_min = time_to_minutes(time_config["standard_clock_out"])
    return await repo.get_attendance_summary(employee_id, start_date, end_date, standard_in_min, standard_out_min)