from MyListType import MyList

a : MyList[int] = MyList([2, 3])
b : MyList[str] = MyList(['a', 'b'])
c : MyList[int] = MyList([2, 3])

print(a + c)

# Error: lists of different types (`str` and `int` cannot be concatinated)
# print(a + b)
