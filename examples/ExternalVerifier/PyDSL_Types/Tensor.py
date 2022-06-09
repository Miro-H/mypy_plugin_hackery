
from typing import List, Generic, TypeVar, Any, Literal

from PyDSL.CustomTypes import *
from PyDSL.Constraints import ConstraintContext, class_constraint

T = TypeVar("T", bound=IntKind)
V = TypeVar("V", bound=Annotated[List[int], ConvertRawLiterals])


@custom_types
class Tensor(Generic[T, V]):
    def __init__(self, d: List[List[T]]) -> None:
        self.d = d
        if len(d) > 0:
            l = len(d[0])
            assert all([len(row) == l for row in d[1:]])
            self.dims = (len(d), l)
        else:
            self.dims = (0, 0)


@class_constraint(Tensor)
def is_valid_tensor(ctx: ConstraintContext):
    return True
