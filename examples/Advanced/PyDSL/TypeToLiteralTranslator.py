# mypy: ignore-errors

import builtins
import logging

from PyDSL import CustomTypes
from PyDSL.Const import TYPE_TO_LITERAL_NO_CAST, TYPE_TO_LITERAL_UNKNOWN_INSTANCE
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

    def visit_any(self, t: AnyType) -> RetType:
        return object

    def visit_none_type(self, t: NoneType) -> RetType:
        return None

    # def visit_type_list(self, t: TypeList) -> RetType:
    #     return list(super().visit_type_list(t))

    def visit_instance(self, t: Instance) -> T:
        args = self.query_types(t.args)

        if t.type.name in dir(builtins):
            inst = eval(t.type.name)
        elif t.type.name in CustomTypes.__dict__:
            inst = CustomTypes.__dict__[t.type.name]
        else:
            logging.warning(TYPE_TO_LITERAL_UNKNOWN_INSTANCE)
            return args

        try:
            return inst(*args)
        except Exception as e:
            logging.debug(TYPE_TO_LITERAL_NO_CAST.format(args, inst, e))
            return inst

    def visit_tuple_type(self, t: TupleType) -> RetType:
        return tuple(super().visit_tuple_type(t))

    def visit_literal_type(self, t: LiteralType) -> RetType:
        return t.value
