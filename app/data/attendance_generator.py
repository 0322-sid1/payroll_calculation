# import random
# from datetime import datetime, timedelta

# #this function converts time to minutes bcz we have to calculate the standard in and out time of employees in minutes.
# def _time_to_minutes(t: str) -> int:
#     #this line split time like 9:30 so split it into 9  30 assign first vale to h and second value to m
#     h, m = map(int, t.split(":"))
#     #multiply h by 60 and then add m
#     return h * 60 + m

# #this function is opposite of above bcz at the end we should return exact time like 9:30 
# def _minutes_to_time(mins: int) -> str:
#     #multiply 24 by 6 then divide by 60 % ensure that the time should be in 24 hours same first nmbr assign to h and second to m  
#     h, m = divmod(mins % (24 * 60), 60)
#     #return time like 9:30...02d means if digit is 1 then add 0 in front of it like 09:05
#     return f"{h:02d}:{m:02d}"

# #this function generates total working dates from start date to end date without weekends
# def generate_working_dates(start_date: str, end_date: str, working_days_per_week: int) -> list[str]:
#     #convert string date into actual date 
#     start = datetime.strptime(start_date, "%Y-%m-%d").date()
#     end = datetime.strptime(end_date, "%Y-%m-%d").date()
#     #set range of working days if 6 then mon to sat else mon to fri
#     allowed_weekdays = set(range(6)) if working_days_per_week >= 6 else set(range(5))  # Mon-Sat vs Mon-Fri
# #empty list to store dates
#     dates = []
#     #set current date as start date
#     current = start
#     #jb tk current date end date k less or equal rahy gi loop chlti rahy gi
#     while current <= end:
#         #if current date is working date then add date in list
#         if current.weekday() in allowed_weekdays:
#             dates.append(current.isoformat())
#             #add one day into current date and then check next date and so on
#         current += timedelta(days=1)
#     return dates

# #This function calculate attendance of employees randomly select absent,late,overtime and set in and out timing of employees for total working days
# def generate_attendance_log(seed: int, dates: list[str], standard_clock_in: str, standard_clock_out: str, absent_days: int = 0,late_days: int = 0,overtime_days: int = 0) -> list[dict]:
#     #make random genertor by using seed
#     rng = random.Random(seed)
#     #total working dates count krta hai
#     total_days = len(dates)
#     #convert clock in time to minutes
#     standard_in_min = _time_to_minutes(standard_clock_in)
#     # convert clock out time to minutes
#     standard_out_min = _time_to_minutes(standard_clock_out)
# #assign indexes to total working days start from 0
#     day_indexes = list(range(total_days))
#     #randomly kisi b din ko absent day bna k uska aik set bna raha hai
#     absent_set = set(rng.sample(day_indexes, min(absent_days, total_days)))
#     #absent days k ilawa baki days ko remaining mai store kr ra
#     remaining = [d for d in day_indexes if d not in absent_set]
#     #remaining days mai sy randomly kisi b day ko late day consider kr k late set bna ra
#     late_set = set(rng.sample(remaining, min(late_days, len(remaining))))
#     #remaining days mai sy late days ko nikal raha
#     remaining_for_ot = [d for d in remaining if d not in late_set]
#     overtime_set = set(rng.sample(remaining_for_ot, min(overtime_days, len(remaining_for_ot))))
# #save attendance for each day 
#     log = []
#     #
#     for idx, date_str in enumerate(dates):
#         if idx in absent_set:
#             log.append({"date": date_str, "status": "absent", "clock_in": None, "clock_out": None})
#             continue

#         clock_in_min = standard_in_min
#         clock_out_min = standard_out_min
#         if idx in late_set:
#             clock_in_min += rng.randint(15, 45)
#         if idx in overtime_set:
#             clock_out_min += rng.randint(30, 90)

#         log.append({
#             "date": date_str,
#             "status": "present",
#             "clock_in": _minutes_to_time(clock_in_min),
#             "clock_out": _minutes_to_time(clock_out_min),
#         })
#     return log