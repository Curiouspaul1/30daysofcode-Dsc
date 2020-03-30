def finder(list1,list2):
    new_list = []
    for i in list1:
        if i in list2:
            new_list.append(i)
    return new_list

print(finder([1,2,3,4,5,6],[2,4,6]))