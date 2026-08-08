from fastapi import FastAPI
from app.routers.payroll_route import router as payroll_router
from app.routers.employees_route import router as employee_router
from app.routers.company_route import router as company_router
from app.routers.attendance_route import router as attendance_router
from app.routers import auth_route


app = FastAPI(title="Payroll Generation API")
app.include_router(payroll_router)
app.include_router(employee_router)
app.include_router(company_router)
app.include_router(attendance_router)
app.include_router(auth_route.router)

