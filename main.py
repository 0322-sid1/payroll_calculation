from fastapi import FastAPI
from app.routers.payroll import router as payroll_router
from app.routers.employees import router as employee_router

app = FastAPI(title="Payroll Generation API")
app.include_router(payroll_router)
app.include_router(employee_router)