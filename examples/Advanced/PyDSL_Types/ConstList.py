from typing import Annotated, TypeVar, Generic, List

from PyDSL.CustomTypes import ConvertRawLiterals, custom_types
from PyDSL.Constraints import class_constraint, ConstraintContext

U = TypeVar("U", bound=Annotated[int, ConvertRawLiterals])
V = TypeVar("V", bound=Annotated[int, ConvertRawLiterals])
W = TypeVar("W", bound=Annotated[int, ConvertRawLiterals])

@custom_types
class ConstList(Generic[U]):
    def __init__(self, l: List) -> None:
        self.l = l
    
    def __add__(self: 'ConstList[U]', other: 'ConstList[V]') -> 'ConstList[W]':
        return ConstList(self.l + other.l)
    
    def typed_eq(self: 'ConstList[U]', other: 'ConstList[U]') -> bool:
        return self.l == other.l

@class_constraint(ConstList)
def is_const_list(ctx: ConstraintContext):
    return True