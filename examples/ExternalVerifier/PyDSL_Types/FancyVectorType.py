import logging

from math import prod
from typing import Annotated, Generic, MutableSequence, TypeVar, Literal, Tuple

from PyDSL.CustomTypes import IntTypeArgs
from PyDSL.Constraints import ConstraintContext, constraint

T = TypeVar("T")
U = TypeVar("U")

class Vector(IntTypeArgs, Generic[T, U]):
    def __init__(self, l):
        self.dim = len(l)
        self.l = l

    def __add__(self : 'Vector[T, U]', other : 'Vector[T, U]') -> 'Vector[T, U]':
       if self.get_dim() != other.get_dim():
           logging.error("Added vectors must have the same dimensions.\n"
                         f"{self.get_dim()} != {other.get_dim()}")

       r = []
       for i in range(self.dim):
           r.append(self.l[i] + other.l[i])

       return Vector(r)

    def __str__(self):
       return f"Vector[{self.dim}] = [{', '.join(map(str, self.l))}]"

    def get_dim(self) -> int:
       return self.dim

@constraint(Vector)
def is_valid_vector(ctx : ConstraintContext):
    print(ctx.types)
    return True