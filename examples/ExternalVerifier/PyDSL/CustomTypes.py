import logging

from PyDSL.RawLiteralTranslator import RawLiteralTranslator

from .Const import *
from typing import Annotated, Final, Generic, Literal, NewType, Type, TypeVar
from mypy.types import UnboundType, RawExpressionType


def make_literal(e):
    return Literal[e]  # type: ignore


RUNTIME_CONVERSION = make_literal
ANNOTATED_TYPE: Final = type(Annotated[int, ""])


class ConvertRawLiterals:
    pass


def is_raw_type(t: Type) -> bool:
    if not isinstance(t, ANNOTATED_TYPE) or not hasattr(t, "__metadata__"):
        return False

    if ConvertRawLiterals in t.__metadata__:  # type: ignore
        return True

    return False

def rewrite_literals(class_obj, conversion, args):
    """
    Allow custom parsing for custom types.
    """

    type_vars = class_obj.__parameters__
    orig_params_type = type(args)
    args = list(args)
    if isinstance(type_vars, tuple):
        for i, t in enumerate(type_vars):
            arg = args[i]
            if issubclass(type(t), TypeVar) and not isinstance(arg, UnboundType):
                b = t.__bound__
                if b and is_raw_type(b):
                    visitor = RawLiteralTranslator(conversion)
                    args[i] = arg.accept(visitor)

    return orig_params_type(args)


def rewrite_literal(class_obj, conversion, arg):
    if not isinstance(arg, tuple):
        arg = (arg,)
    r = rewrite_literals(class_obj, conversion, arg)
    return r[0]


def has_custom_bound(param, aggregate=False):
    if hasattr(param, "__iter__"):
        response_rec = map(lambda x: has_custom_bound(x, True), param)

        if aggregate:
            return any(response_rec)

        return list(response_rec)

    return param.__bound__ != None and issubclass(param.__bound__, CustomTypes)


def custom_types(decorated_class):
    """
    Decorator to catch the runtime errors that are produced when literals
    are used directly in the type system.
    """
    decorated_class_getitem = decorated_class.__class_getitem__

    def __class_getitem__(params):  # cls is implicit
        params = rewrite_literals(decorated_class, RUNTIME_CONVERSION, params)
        return decorated_class_getitem(params=params)

    decorated_class.__class_getitem__ = __class_getitem__
    return decorated_class


class CustomTypes:
    pass


class IntKind(CustomTypes):
    l: int


L = TypeVar("L", bound=int)


@custom_types
class Int8(IntKind, Generic[L]):
    l = 8


@custom_types
class Int16(IntKind, Generic[L]):
    l = 16


@custom_types
class Int32(IntKind, Generic[L]):
    l = 32


@custom_types
class Int64(IntKind, Generic[L]):
    l = 64
