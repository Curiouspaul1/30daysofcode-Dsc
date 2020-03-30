def square(array):
    result = map(lambda x:pow(x,2),array)
    return list(result)

print(square([1,2,3,4]))