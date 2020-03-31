# Type check (Day 2)
def typecheck(*args):
    """Checks type() of a given argument, returns str(Error) if None """
    if len(args) != 0:
        typeof = type(args[0])
        if typeof:
            return typeof
        else:
            return "Error"
    else:
        return "Error"

try:
    print(typecheck())
except SyntaxError or TypeError or NameError or ValueError:
    raise "Error"