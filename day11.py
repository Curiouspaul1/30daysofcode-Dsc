# Filename: day11.py

import datetime as d
import calendar as c

def dateofbirth(str_):
    """
        dateofbirth takes your date of birth as input
        calculates the number of days from, the current
        day till your next birthday.

        ========
        args: <string: class>
        returns: <string: class>,<timedelta: class>

        date-input format: YYYY-MM-DD 
    """
    try:
        birth_date = d.date(int(str_.split("-")[0]),int(str_.split("-")[1]),int(str_.split("-")[2]))
    except ValueError:
        raise ValueError("please enter date using the format described")
    today = d.date.today()
    if today != birth_date:
        dob = birth_date.replace(year=today.year)
        diff = dob - today
        tgap = str(dob-today).split(",")[0].split(" ")[0]
        if int(tgap) > 0:
            return tgap
        elif int(tgap) < 0 and c.isleap(today.year+1):
            diff += d.timedelta(days=366)
            return diff
        else:
            diff += d.timedelta(days=365)
            return diff

   
print(dateofbirth("1999-9-2"))