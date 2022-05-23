from MyList import MyList

a : MyList[int] = MyList([2, 3])
b : MyList[str] = MyList(['a', 'b'])
c : MyList[int] = MyList([2, 3])

print(a + c)

# The following line has to throw an error
# print(a + b)