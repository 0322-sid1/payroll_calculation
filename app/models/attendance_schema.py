from enum import Enum
from pydantic import BaseModel
from typing import Optional


class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"


class AttendanceRecordCreate(BaseModel):
    employee_id: str
    date: str                       
    status: AttendanceStatus
    clock_in: Optional[str] = None  
    clock_out: Optional[str] = None


class AttendanceRecordOut(AttendanceRecordCreate):
    id: str