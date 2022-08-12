from typing import Callable
from mypy.type_visitor import TypeQuery
from mypy.types import *

from PyDSL.InternalUtils import get_fqcn


class TypeFinderVisitor(TypeQuery[bool]):
    """
    Visitor class to detect if any type or subtype is a type instance of the given
    search target.
    """

    def __init__(self,
                 search_target: object,
                 strategy: Callable[[Iterable[bool]], bool] = any) -> None:

        self.search_target_fqcn = get_fqcn(search_target)
        super().__init__(strategy)

    def visit_instance(self, t: Instance) -> bool:
        if t.type.fullname == self.search_target_fqcn:
            return True
        return False
