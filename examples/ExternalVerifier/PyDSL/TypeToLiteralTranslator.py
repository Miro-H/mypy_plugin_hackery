# mypy: ignore-errors

import builtins
import logging

from PyDSL import CustomTypes
from typing import Tuple, Callable
from mypy.types import *

# TODO: set? -> no SetType? What should we do with dict?
RetType = Union[bool, int, str, bytes, list, tuple]

class TypeToLiteralTranslator(TypeQuery[RetType]):
    """
    Visitor class to convert parsed types into raw literals, i.e.
    we convert
    Tuple[Literal[10], Literal[20]]
    to
    (10, 20)
    """

    def __init__(self) -> None:
        def nop_strategy(results) -> List[RetType]:
            return results

        super().__init__(nop_strategy)
    
    def visit_type_list(self, t: TypeList) -> RetType:
        return list(super().visit_type_list(t))

    def visit_instance(self, t: Instance) -> T:
        if t.type.name in dir(builtins):
            return eval(t.type.name)
        elif t.type.name in CustomTypes.__dict__:
            return CustomTypes.__dict__[t.type.name]
        
        logging.warning("Unknown instance ignored, only returned arguments")
        return self.query_types(t.args)
        
    def visit_tuple_type(self, t: TupleType) -> RetType:
        return tuple(super().visit_tuple_type(t))
    
    def visit_literal_type(self, t: LiteralType) -> RetType:
        return t.value