
from typing import Literal, Dict

from PyDSL_Types import *

#######################################################
##################### Vector Test #####################
#######################################################

x: Vector[int, 20] = Vector(list(range(1, 21)))
y: Vector[int, 20] = Vector([1] * 20)

# Allowed
print("Resulting vector: ", x + y)

# Error (invalid vector)
# w : Vector[str, 6] = Vector(list(range(1,7)))

# Error (vectors of different dimensions!)
# z : Vector[int, 10] = Vector([1] * 6)
# print("Resulting vector: ", x + z)


######################################################
##################### Money Test #####################
######################################################

CHFCoins = Literal[5, 10, 20, 50, 100, 500]
bal1 : Dict[CHFCoins, int]= { 5: 0, 10: 3, 20: 2, 50: 4, 100: 7, 500: 1 }

# `Literal[5, 10, ...]` is the abbreviated syntax for 
# `Union[Literal[5], Literal[10], ...]`
a : Money[CHFCoins] = Money(bal1)
a.store(5, 1)
a.take(10, 2)

b : Money[CHFCoins] = Money(bal1)
c = a + b

# Invalid Literal[1] -> there is no coin 1 in this currency
# a.store(1, 1)

EURCoins = Literal[1, 2, 5, 10, 20, 50, 100, 200]
bal2 : Dict[EURCoins, int]= { 1: 10, 2: 5, 5: 10, 10: 1, 20: 2, 50: 2, 100: 3, 200: 0 }

d : Money[EURCoins] = Money(bal2)

# Cannot add different currencies
# e = a + d

# Cannot instantiate money with balance in wrong currency
# f : Money[EURCoins] = Money(bal1)
