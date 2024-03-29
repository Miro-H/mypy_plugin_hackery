from typing import Literal, Dict, Tuple, List
from mypy.types import Union

from PyDSL.CustomTypes import *

from PyDSL_Types import *


#######################################################
##################### Vector Test #####################
#######################################################

# x: Vector[Int32, 20] = Vector(list(range(1, 21)))
# y: Vector[Int32, 20] = Vector([1] * 20)

# # Allowed
# print("Resulting vector: ", x + y)

# Error (invalid vectors)
# u : Vector[float, 10]
# w : Vector[10, Int32]

# Error (vectors of different dimensions!)
# z1: Vector[Int32, 10] = Vector([1] * 6)
# print("Resulting vector: ", x + z1)
# z2: Vector[Int16, 20] = Vector([1] * 6)
# print("Resulting vector: ", x + z2)

#######################################################
##################### Tensor Test #####################
#######################################################

# t1: Tensor[Int16, List[Literal[10, 30]]]
# t2: Tensor[Int16, [10, 30]]

# Invalid type arguments. Expected 'typing.List[int]', got '['10', '30']'.
# t3: Tensor[Int16, ["10", "30"]]

# Invalid type arguments. Expected 'typing.List[int]', got '[10, '30']'.
# t4: Tensor[Int16, [10, "30"]]

######################################################
##################### Money Test #####################
######################################################

# CHFCoins = Literal[5, 10, 20, 50, 100, 500]
# bal1: Dict[CHFCoins, int] = {5: 0, 10: 3, 20: 2, 50: 4, 100: 7, 500: 1}

# # `Literal[5, 10, ...]` is the abbreviated syntax for
# # `Union[Literal[5], Literal[10], ...]`
# a: Money[CHFCoins] = Money(bal1)
# a.store(5, 1)
# a.take(10, 2)

# b: Money[CHFCoins] = Money(bal1)
# c = a + b

# # Invalid Literal[1] -> there is no coin 1 in this currency
# # a.store(1, 1)

# EURCoins = Literal[1, 2, 5, 10, 20, 50, 100, 200]
# bal2: Dict[EURCoins, int] = {1: 10, 2: 5,
#                              5: 10, 10: 1, 20: 2, 50: 2, 100: 3, 200: 0}

# d: Money[EURCoins] = Money(bal2)

# # Cannot add different currencies
# # e = a + d

# # Cannot instantiate money with balance in wrong currency
# # f : Money[EURCoins] = Money(bal1)

# # #####################################################
# # #################### Person Test ####################
# # #####################################################

# p: Person = Person("Alice", 31, "-", 70000)
# print(p.age)

# # Throws error because secret attribute is accessed
# # print(p.health_record)


######################################################
################### ConstList Test ###################
######################################################

# c_l1: ConstList[3] = ConstList(["l1"] * 3)
# c_l2: ConstList[2] = ConstList(["l2"] * 2)

# c_l3 = c_l1 + c_l2

# c_l4: ConstList[5] = ConstList(["l1"] * 3 + ["l2"] * 2)
# print(c_l3.typed_eq(c_l4))

# Error: Argument 1 to "safe_eq" of "ConstList" has incompatible type "ConstList[Literal[6]]"; expected "ConstList[Literal[5]]"
# c_l5: ConstList[6] = ConstList(["l5"] * 6)
# print(c_l3.typed_eq(c_l5))


######################################################
################### EvenList Test ####################
######################################################

# l1: EvenList[4] = EvenList(["l1"] * 4)
# l2: EvenList[2] = EvenList(["l2"] * 2)

# print(l1 + l2)

# Error: only even lists can be added, got: EvenList[4] + EvenList[3]
# l3: EvenList[3] = EvenList(["l3"] * 3)
# print(l1 + l3)