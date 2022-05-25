from PyDSL_Types import *

x: Vector[int, 20] = Vector(list(range(1, 11)))
y: Vector[int, 20] = Vector([1] * 20)

# Allowed
print("Resulting vector: ", x + y)

# Error (invalid vector)
# w : Vector[str, 6] = Vector(list(range(1,7)))

# Error (vectors of different dimensions!)
# z : Vector[int, 10] = Vector([1] * 6)
# print("Resulting vector: ", x + z)
