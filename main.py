from fastapi import FastAPI
from app.routers.payroll import router as payroll_router
from app.routers.employees import router as employee_router
from app.routers.company import router as company_router
from app.routers.attendance import router as attendance_router

app = FastAPI(title="Payroll Generation API")
app.include_router(payroll_router)
app.include_router(employee_router)
app.include_router(company_router)
app.include_router(attendance_router)
