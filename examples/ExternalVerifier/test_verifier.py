from typing import Literal, Dict, Tuple
from mypy.types import Union

from PyDSL.CustomTypes import *

from PyDSL_Types import *


#######################################################
##################### Vector Test #####################
#######################################################

# x: Vector[Int32, 20] = Vector(list(range(1, 21)))
x: Vector[Int32, Union[Literal[10], Literal[20]]] = Vector(list(range(1, 21)))
y: Vector[Int32, [10, 20]] = Vector(list(range(1, 21)))
# y: Vector[Int32, [10, 20]] = Vector([1] * 20)

# Allowed
# print("Resulting vector: ", x + y)

# Error (invalid vectors)
# u : Vector[float, 10]
# w : Vector[10, Int32]

# Error (vectors of different dimensions!)
# z1: Vector[Int32, 10] = Vector([1] * 6)
# print("Resulting vector: ", x + z1)
# z2: Vector[Int16, 20] = Vector([1] * 6)
# print("Resulting vector: ", x + z2)


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
