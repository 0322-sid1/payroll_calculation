from fastapi import APIRouter
from app.models.attendance_schema import AttendanceRecordCreate
from app.controllers import attendance_controller as controller

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])

#this api create attendance record for an employee
@router.post("")
async def create_attendance_record(payload: AttendanceRecordCreate):
    record_data = payload.model_dump()
    created_record = await controller.create_attendance_record(record_data)
    return created_record

#this api fetch attendance records for an employee within a date range
@router.get("/{employee_id}")
async def get_attendance_records(employee_id: str, start_date: str, end_date: str):
    records = await controller.get_attendance_records(employee_id, start_date, end_date)
    return {"employee_id": employee_id, "total_records": len(records), "records": records}