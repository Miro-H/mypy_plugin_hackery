import logging

from typing import Generic, TypeVar

from PyDSL.CustomTypes import IntKind, custom_types
from PyDSL.Constraints import ConstraintContext, class_constraint

from mypy.types import LiteralType

T = TypeVar("T", bound=IntKind)
U = TypeVar("U", bound=int)

@custom_types
class Vector(Generic[T, U]):
    def __init__(self, l):
        self.dim = len(l)
        self.l = l

    # TODO: overwrite add that only some sizes are allowed to be added if one of the types is even
    # TODO: define type that produces new types as result dep on input (vector concatenation)

    def __add__(self: 'Vector[T, U]', other: 'Vector[T, U]') -> 'Vector[T, U]':
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


@class_constraint(Vector)
def is_valid_vector(ctx: ConstraintContext):

    def custom_validator(elem_type, dim):
        if dim % 10 == 0:
            return True
        else:
            return False, f"Wrong dimension, must be zero modulo 10 but is {dim} = {dim % 10} (mod 10)"

    return ctx.validate_types_with_fn(custom_validator)

# @class_constraint(Vector)
# def is_valid_vector(ctx: ConstraintContext):
#     return ctx.validate_types([int, 10])