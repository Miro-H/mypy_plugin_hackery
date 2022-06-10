import logging
import builtins

from PyDSL.RawLiteralTranslator import RawLiteralTranslator
from PyDSL.InternalUtils import get_fqcn, make_literal
from .Const import *

from typing import (
    Annotated, Final, Generic, Literal, Type, TypeVar,
    Optional, Union, List, Any
)

from mypy.types import UnboundType, RawExpressionType, LiteralType, NoneType
from mypy.plugin import AnalyzeTypeContext

ANNOTATED_TYPE: Final = type(Annotated[int, ""])


class CustomAny:
    def __init__(self, t: type):
        self.t = t


CustomInt = Annotated[Any, CustomAny(int)]


class ConvertRawLiterals:
    pass


def has_annotation(t: Type) -> bool:
    return isinstance(t, ANNOTATED_TYPE) and hasattr(t, "__metadata__")


def is_raw_type(t: Type) -> bool:
    return has_annotation(t) and ConvertRawLiterals in t.__metadata__


def get_custom_any(t):
    if has_annotation(t):
        for md in t.__metadata__:
            if isinstance(md, CustomAny):
                return md.t
    return None


def unwrap_custom_bound(bound):
    real_t = get_custom_any(bound)

    if real_t:
        return real_t
    else:
        if hasattr(bound, "__args__"):
            bound.__args__ = tuple([unwrap_custom_bound(arg)
                                   for arg in bound.__args__])
        return bound


def convert_recursively(conversion, arg, ctx):
    if type(arg) in [int, str, bytes, bool]:
        return conversion(arg, ctx)
    elif type(arg) in [list, tuple, set]:
        # TODO:
        raise NotImplementedError("TODO")
    elif type(arg) in builtins.__dict__.values():
        # TODO: is there a use case for dicts, ...?
        raise NotImplementedError(
            f"Support for type {type(arg)} is not yet implemented at runtime.")

    visitor = RawLiteralTranslator(ctx)
    r = arg.accept(visitor)
    return r


def get_bounds(obj, convert_annotated=False):
    bounds = []
    for param in obj.__parameters__:
        if hasattr(param, "__bound__"):
            bound = param.__bound__
            if isinstance(bound, ANNOTATED_TYPE):
                bound = bound.__args__[0]
            bounds.append(bound)
        else:
            bounds.append(param)

    return bounds


def rewrite_literals(class_obj, args, ctx=None):
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
                    args[i] = convert_recursively(make_literal, arg, ctx)
    return orig_params_type(args)


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
        params = rewrite_literals(decorated_class, params)
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
