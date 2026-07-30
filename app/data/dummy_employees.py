DUMMY_EMPLOYEES = [
    {
        "employee_id": "EMP001", "name": "Dianne Russell", "email": "diannerussell@gmail.com",
        "profile_picture": "https://i.pravatar.cc/150?img=1",
        "department": "Designing", "designation": "UI/UX Designer", "employment_type": "Full-time",
        "employee_type": "Monthly", "working_hours_per_day": 8,
        "time_config": {"working_days_per_week": 5, "standard_clock_in": "09:00", "standard_clock_out": "17:00", "paid_leaves_allowed_per_month": 2},
        "attendance_profile": {"seed": 1, "absent_days": 2, "late_days": 1, "overtime_days": 1},
    
        "salary": {
            "salary_type": "Monthly", "base_salary": 25000, "hourly_rate": None, "currency": "PKR",
            "pay_period_start_date": "2026-06-01", "payment_method": "Bank Transfer",
            "overtime_hourly_rate": 200, "late_deduction_rate": 100,
            "benefits": [{"name": "Pick and Drop Service", "amount": 1000}, {"name": "Expenses", "amount": 500}],
            "deductions": [{"type": "UIF", "calculation_type": "percentage", "value": 5}, {"type": "Income Tax", "calculation_type": "fixed", "value": 1500}]
        }
    },
    {
        "employee_id": "EMP002", "name": "Ahmed Khan", "email": "ahmedkhan@gmail.com",
        "profile_picture": "https://i.pravatar.cc/150?img=2",
        "department": "Engineering", "designation": "Backend Developer", "employment_type": "Full-time",
        "employee_type": "Monthly", "working_hours_per_day": 8,
        "time_config": {"working_days_per_week": 5, "standard_clock_in": "10:00", "standard_clock_out": "18:00", "paid_leaves_allowed_per_month": 2},
        "attendance_profile": {"seed": 2, "absent_days": 1, "late_days": 0, "overtime_days": 1}, 
        "salary": {
            "salary_type": "Monthly", "base_salary": 45000, "hourly_rate": None, "currency": "PKR",
            "pay_period_start_date": "2026-06-01", "payment_method": "Bank Transfer",
            "overtime_hourly_rate": 300, "late_deduction_rate": 150,
            "benefits": [{"name": "Pick and Drop Service", "amount": 0}, {"name": "Expenses", "amount": 800}],
            "deductions": [{"type": "UIF", "calculation_type": "percentage", "value": 5}, {"type": "Income Tax", "calculation_type": "percentage", "value": 8}]
        }
    },
    {
        "employee_id": "EMP003", "name": "Sara Ali", "email": "saraali@gmail.com",
        "profile_picture": "https://i.pravatar.cc/150?img=3",
        "department": "Marketing", "designation": "Marketing Executive", "employment_type": "Full-time",
        "employee_type": "Weekly", "working_hours_per_day": 8,
        "time_config": {"working_days_per_week": 5, "standard_clock_in": "09:30", "standard_clock_out": "17:30", "paid_leaves_allowed_per_month": 1},
        "attendance_profile": {"seed": 3, "absent_days": 0, "late_days": 0, "overtime_days": 1},
 
        "salary": {
            "salary_type": "Monthly", "base_salary": 12000, "hourly_rate": None, "currency": "PKR",
            "pay_period_start_date": "2026-06-01", "payment_method": "Bank Transfer",
            "overtime_hourly_rate": 150, "late_deduction_rate": 80,
            "benefits": [{"name": "Pick and Drop Service", "amount": 0}, {"name": "Expenses", "amount": 0}],
            "deductions": [{"type": "UIF", "calculation_type": "percentage", "value": 5}, {"type": "Income Tax", "calculation_type": "fixed", "value": 400}]
        }
    },
    {
        "employee_id": "EMP004", "name": "Bilal Ahmed", "email": "bilalahmed@gmail.com",
        "profile_picture": "https://i.pravatar.cc/150?img=4",
        "department": "Sales", "designation": "Sales Executive", "employment_type": "Full-time",
        "employee_type": "Weekly", "working_hours_per_day": 8,
        "time_config": {"working_days_per_week": 6, "standard_clock_in": "09:00", "standard_clock_out": "17:00", "paid_leaves_allowed_per_month": 1},
        "attendance_profile": {"seed": 4, "absent_days": 2, "late_days": 1, "overtime_days": 0},
 
        "salary": {
            "salary_type": "Monthly", "base_salary": 10000, "hourly_rate": None, "currency": "PKR",
            "pay_period_start_date": "2026-06-01", "payment_method": "Cash",
            "overtime_hourly_rate": 120, "late_deduction_rate": 70,
            "benefits": [{"name": "Pick and Drop Service", "amount": 500}, {"name": "Expenses", "amount": 0}],
            "deductions": [{"type": "UIF", "calculation_type": "percentage", "value": 5}, {"type": "Income Tax", "calculation_type": "fixed", "value": 300}]
        }
    },
    {
        "employee_id": "EMP005", "name": "Fatima Noor", "email": "fatimanoor@gmail.com",
        "profile_picture": "https://i.pravatar.cc/150?img=5",
        "department": "HR", "designation": "HR Officer", "employment_type": "Full-time",
        "employee_type": "Monthly", "working_hours_per_day": 8,
        "time_config": {"working_days_per_week": 5, "standard_clock_in": "09:00", "standard_clock_out": "17:00", "paid_leaves_allowed_per_month": 2},
        "attendance_profile": {"seed": 5, "absent_days": 0, "late_days": 0, "overtime_days": 0},

        "salary": {
            "salary_type": "Monthly", "base_salary": 40000, "hourly_rate": None, "currency": "PKR",
            "pay_period_start_date": "2026-06-01", "payment_method": "Bank Transfer",
            "overtime_hourly_rate": 250, "late_deduction_rate": 120,
            "benefits": [{"name": "Pick and Drop Service", "amount": 1000}, {"name": "Expenses", "amount": 300}],
            "deductions": [{"type": "UIF", "calculation_type": "percentage", "value": 5}, {"type": "Income Tax", "calculation_type": "percentage", "value": 7}]
        }
    },
    {
        "employee_id": "EMP006", "name": "Usman Tariq", "email": "usmantariq@gmail.com",
        "profile_picture": "https://i.pravatar.cc/150?img=6",
        "department": "QA", "designation": "QA Engineer", "employment_type": "Contract",
        "employee_type": "Hourly", "working_hours_per_day": 8,
        "time_config": {"working_days_per_week": 5, "standard_clock_in": "10:00", "standard_clock_out": "18:00", "paid_leaves_allowed_per_month": 0},
        "attendance_profile": {"seed": 6, "absent_days": 3, "late_days": 0, "overtime_days": 1},
        "salary": {
            "salary_type": "Hourly", "base_salary": None, "hourly_rate": 250, "currency": "PKR",
            "pay_period_start_date": "2026-06-01", "payment_method": "Bank Transfer",
            "overtime_hourly_rate": 350, "late_deduction_rate": 0,
            "benefits": [{"name": "Pick and Drop Service", "amount": 0}, {"name": "Expenses", "amount": 0}],
            "deductions": [{"type": "UIF", "calculation_type": "fixed", "value": 500}, {"type": "Income Tax", "calculation_type": "fixed", "value": 0}]
        }
    },
    {
        "employee_id": "EMP007", "name": "Ayesha Malik", "email": "ayeshamalik@gmail.com",
        "profile_picture": "https://i.pravatar.cc/150?img=7",
        "department": "Finance", "designation": "Accountant", "employment_type": "Full-time",
        "employee_type": "Monthly", "working_hours_per_day": 8,
        "time_config": {"working_days_per_week": 5, "standard_clock_in": "09:00", "standard_clock_out": "17:00", "paid_leaves_allowed_per_month": 2},
        "attendance_profile": {"seed": 7, "absent_days": 1, "late_days": 1, "overtime_days": 0},

        "salary": {
            "salary_type": "Monthly", "base_salary": 38000, "hourly_rate": None, "currency": "PKR",
            "pay_period_start_date": "2026-06-01", "payment_method": "Bank Transfer",
            "overtime_hourly_rate": 220, "late_deduction_rate": 100,
            "benefits": [{"name": "Pick and Drop Service", "amount": 0}, {"name": "Expenses", "amount": 400}],
            "deductions": [{"type": "UIF", "calculation_type": "percentage", "value": 5}, {"type": "Income Tax", "calculation_type": "percentage", "value": 6}]
        }
    },
    {
        "employee_id": "EMP008", "name": "Hamza Sheikh", "email": "hamzasheikh@gmail.com",
        "profile_picture": "https://i.pravatar.cc/150?img=8",
        "department": "Customer Support", "designation": "Support Agent", "employment_type": "Part-time",
        "employee_type": "Hourly", "working_hours_per_day": 6,
        "time_config": {"working_days_per_week": 5, "standard_clock_in": "12:00", "standard_clock_out": "18:00", "paid_leaves_allowed_per_month": 0},
        "attendance_profile": {"seed": 8, "absent_days": 0, "late_days": 1, "overtime_days": 0},

        "salary": {
            "salary_type": "Hourly", "base_salary": None, "hourly_rate": 180, "currency": "PKR",
            "pay_period_start_date": "2026-06-01", "payment_method": "Bank Transfer",
            "overtime_hourly_rate": 250, "late_deduction_rate": 60,
            "benefits": [{"name": "Pick and Drop Service", "amount": 0}, {"name": "Expenses", "amount": 0}],
            "deductions": [{"type": "UIF", "calculation_type": "fixed", "value": 300}, {"type": "Income Tax", "calculation_type": "fixed", "value": 0}]
        }
    },
    {
        "employee_id": "EMP009", "name": "Zainab Yousuf", "email": "zainabyousuf@gmail.com",
        "profile_picture": "https://i.pravatar.cc/150?img=9",
        "department": "Design", "designation": "Graphic Designer", "employment_type": "Full-time",
        "employee_type": "Monthly", "working_hours_per_day": 8,
        "time_config": {"working_days_per_week": 5, "standard_clock_in": "09:00", "standard_clock_out": "17:00", "paid_leaves_allowed_per_month": 2},
        "attendance_profile": {"seed": 9, "absent_days": 5, "late_days": 1, "overtime_days": 0},

        "salary": {
            "salary_type": "Monthly", "base_salary": 30000, "hourly_rate": None, "currency": "PKR",
            "pay_period_start_date": "2026-06-01", "payment_method": "Bank Transfer",
            "overtime_hourly_rate": 200, "late_deduction_rate": 90,
            "benefits": [{"name": "Pick and Drop Service", "amount": 500}, {"name": "Expenses", "amount": 0}],
            "deductions": [{"type": "UIF", "calculation_type": "percentage", "value": 5}, {"type": "Income Tax", "calculation_type": "fixed", "value": 1200}]
        }
    },
    {
        "employee_id": "EMP010", "name": "Talha Farooq", "email": "talhafarooq@gmail.com",
        "profile_picture": "https://i.pravatar.cc/150?img=10",
        "department": "Operations", "designation": "Operations Manager", "employment_type": "Full-time",
        "employee_type": "Weekly", "working_hours_per_day": 8,
        "time_config": {"working_days_per_week": 5, "standard_clock_in": "09:00", "standard_clock_out": "17:00", "paid_leaves_allowed_per_month": 1},
        "attendance_profile": {"seed": 10, "absent_days": 0, "late_days": 0, "overtime_days": 1},

        "salary": {
            "salary_type": "Monthly", "base_salary": 18000, "hourly_rate": None, "currency": "PKR",
            "pay_period_start_date": "2026-06-01", "payment_method": "Bank Transfer",
            "overtime_hourly_rate": 280, "late_deduction_rate": 130,
            "benefits": [{"name": "Pick and Drop Service", "amount": 0}, {"name": "Expenses", "amount": 600}],
            "deductions": [{"type": "UIF", "calculation_type": "percentage", "value": 5}, {"type": "Income Tax", "calculation_type": "percentage", "value": 9}]
        }
    },
]