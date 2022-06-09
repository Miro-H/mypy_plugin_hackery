import logging

from typing import Annotated, Any, Generic, TypeVar, List

from PyDSL.CustomTypes import IntKind, ConvertRawLiterals, custom_types
from PyDSL.Constraints import ConstraintContext, class_constraint

T = TypeVar("T", bound=IntKind)
# U = TypeVar("U", bound=int)
# U = TypeVar("U")
U = TypeVar("U", bound=Annotated[int, ConvertRawLiterals])
# V = TypeVar("V", bound=Annotated[List[int], ConvertRawLiterals])


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


# class Tensor(Generic[T, V]):
#     def __init__(self, d: List[List[T]]) -> None:
#         self.d = d
#         if len(d) > 0:
#             l = len(d[0])
#             assert all([len(row) == l for row in d[1:]])
#             self.dims = (len(d), l)
#         else:
#             self.dims = (0, 0)


@class_constraint(Vector)
def is_valid_vector(ctx: ConstraintContext):

    def custom_validator(elem_type, dims):
        if isinstance(dims, int):
            dims = [dims]

        if all([dim % 10 == 0 for dim in dims]):
            return True
        else:
            return False, f"Wrong dimensions, must all be zero modulo 10 but have {dims}"

    return ctx.validate_types_with_fn(custom_validator)

# @class_constraint(Vector)
# def is_valid_vector(ctx: ConstraintContext):
#     return ctx.validate_types([int, 10])
