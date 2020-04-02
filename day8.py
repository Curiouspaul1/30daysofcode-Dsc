import sys
dict_ = {
    "1":"I",
    "5":"V",
    "10":"X",
    "50":"L",
    "100":"C",
    "500":"D",
    "1000":"M"
}


str_ = ''
mdic = []

def arabtorom(num):
    """
        Arabtotrom takes any arabic number representation (0-9, e.g 254), and converts
        it to it's equivalent in roman numerals , with the aid of a dictionary labelled
        'dict_' above.
        arabtorom uses recursion to calculate each of its roman digits.
    """
    global str_
    dic = []
    for i in dict_:
        diff = num - int(i)
        if diff >= 0:
            dic.append(diff)
        else:
            pass
        dic.sort()
    print(dic)
    if len(dic) > 0:
        n = dic[0]
        if 5 - n == 1:
            str_+=dict_[f"{1}"]+dict_[f"{5}"]
            print(str_)
            return None
        elif 10 - n == 1:
            str_+=dict_[f"{1}"]+dict_[f"{10}"]
            print(str_)
            return None
        elif 50-n == 10:
            str_+=dict_[f"{10}"]+dict_[f"{50}"]
            print(str_)
            return None
        elif 100-n == 10:
            str_+=dict_[f"{10}"]+ dict_[f"{100}"]
            print(str_)
            return None
        elif 500-n == 100:
            str_+=dict_[f"{100}"]+dict_[f"{500}"]
            print(str_)
            return None
        elif 1000-n == 100:
            str_ += dict_[f"{100}"]+dict_[f"{1000}"]
            print(str_)
            return None
        else:
            str_ += dict_[f"{num - n}"]
        while n >0:
            return arabtorom(n)
    print(str_)
    pass


print(arabtorom(254))