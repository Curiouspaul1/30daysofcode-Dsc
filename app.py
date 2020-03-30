# 30 DAYS OF CODE
import datetime as d

# Date viewer (DAY 0)
def dateview():
    diff = d.timedelta(0,0,0,0,0,1,0)
    date = diff + d.datetime.utcnow()
    date_ = str(date)
    time = date_.split(' ')
    #complements = ['beautiful','wonderful','gracious','magnificent']
    print(f"It's a gracious {date.strftime('%A')}")
    print(f"Current time is {time[1]} {date.strftime('%p')}")

    pass


# Number Checker (DAY 1)
def checker(*args):
    if len(args) == 1:
        if args[0] < 0:
            return f"{args[0]} is Negative"
        elif args[0] > 0:
            return f"{args[0]} is Positive"
    
    if len(args) > 1:
        if args[0] > 0 and args[1] > 0:
            return f"{args[0]} is Positive, {args[1]} is Positive"
        elif args[0] > 0 and args[1] < 0:
            return f"{args[0]} is Positive, {args[1]} is Negative"
        elif args[0] < 0 and args[1] < 0:
            return f"{args[0]} is Negative, {args[1]} is Negative"
        elif args[0] < 0 and args[1] > 0:
            return f"{args[0]} is Negative, {args[1]} is Positive"






# run functions
print(checker(-2,4))
dateview()
