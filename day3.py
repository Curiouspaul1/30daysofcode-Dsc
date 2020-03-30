vowels = ['a','e','i','o','u','A','E','I','O','U']

def vowelcheck(str):
    dict_ = []
    for i in str:
        if i in vowels or i.upper() in vowels:
            dict_.append(i)
    count = len(dict_)
    return count


