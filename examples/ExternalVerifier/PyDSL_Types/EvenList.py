
from typing import Annotated, TypeVar, Generic, List

from PyDSL.CustomTypes import ConvertRawLiterals
from PyDSL.Constraints import class_constraint, ConstraintContext

U = TypeVar("U", bound=Annotated[int, ConvertRawLiterals])
V = TypeVar("V", bound=Annotated[int, ConvertRawLiterals])
W = TypeVar("W", bound=Annotated[int, ConvertRawLiterals])

# TODO: overwrite add that only some sizes are allowed to be added if one of the types is even

class EvenList(Generic[U]):
    def __init__(self, l: List) -> None:
        self.l = l
    
    def __add__(self: 'EvenList[U]', other: 'EvenList[V]') -> 'EvenList[W]':
        return EvenList(self.l + other.l)

@class_constraint(EvenList)
def is_const_list(ctx: ConstraintContext):
    return True