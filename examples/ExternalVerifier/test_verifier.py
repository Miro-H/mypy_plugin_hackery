from PyDSL_Types import *

x: Vector[int, 6] = Vector(list(range(1, 7)))
y: Vector[int, 6] = Vector([1] * 6)

# Allowed
print("Resulting vector: ", x + y)

# Error (invalid vector)
# w : Vector[str, 6] = Vector(list(range(1,7)))

# Error (vectors of different dimensions!)
# z : Vector[int, 7] = Vector([1] * 6)
# print("Resulting vector: ", x + z)
