def reverser(str):
    holder = []
    for i in range(1,len(str)+1):
        holder.append(str[-i])
    word = ''.join(i for i in holder)
    return word

def palindromecheck(str):
    list1 = str.split(' ')
    if len(list1)==1:
        word = reverser(str)
        if word == str:
            return True
        else:
            return False
        pass
    else:
        placehold = []
        placehold1 = []
        for i in range(1,len(list1)+1):
            placehold.append(list1[-i])
        for i in placehold:
            placehold1.append(reverser(i))
        
        word = ''.join(i for i in placehold1)
        if word == ''.join(i for i in list1):
            return True
        else:
            return False

print(palindromecheck("nurses run"))
print(palindromecheck("mum"))