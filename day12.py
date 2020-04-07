# Filename: day12.py

def strinverter(str):
    """
        strinverter() takes a string input (a digit) and converts
        it to it's corresponding int type, given that the input is 
        a digit or concatenation of digits that can be expressed as 
        base10 -literals with int()
    
        ===========
        args: <class 'str'>
        returns: <class 'str'> or <class 'int'>
    """
    try:
        num = int(str)
        return num
    except ValueError:
        return "Error"

print(strinverter("49"))