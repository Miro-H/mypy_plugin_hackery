from examples.VectorType import Vector
from typing import List

# XXX: Note that x = Vector[...](...) is neither allowed 
# nor equivalent to the statement below.
x : Vector[int, 6] = Vector(list(range(1,7)))
y : Vector[int, 6] = Vector([1] * 6)

print(__annotations__)

# Allowed
print("Resulting vector: ", x + y)

# Error (invalid vector)
w : Vector[str, 6] = Vector(list(range(1,7)))

# Error (vectors of different dimensions!)
z : Vector[int, 7] = Vector([1] * 6)
print("Resulting vector: ", x + z)
