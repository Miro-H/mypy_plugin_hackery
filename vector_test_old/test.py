from examples.VectorType import Vector
from typing import List

# XXX: Note that x = Vector[...](...) is neither allowed 
# nor equivalent to the statement below.
w : Vector[str, 6] = Vector(list(range(1,7)))
x : Vector[int, 6] = Vector(list(range(1,7)))
y : Vector[int, 6] = Vector([1] * 6)
z : Vector[int, 7] = Vector([1] * 6)

print(__annotations__)

# Allowed
print("Resulting vector: ", x + y)

# Error
print("Resulting vector: ", x + z)
print("Resulting vector: ", x + w)

# a : List[int] = [2, 3]
# b : List[str] = ['a', 'b']
# print(a + b)