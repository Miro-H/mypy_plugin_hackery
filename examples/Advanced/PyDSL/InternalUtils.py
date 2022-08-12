"""
This file contains internal helper functions that are not intended for the use outside of PyDSL.
"""

from typing import Optional, Literal, List, Any
from mypy.plugin import AnalyzeTypeContext
from mypy.types import (
    AnyType, CallableType, DeletedType, EllipsisType, ErasedType, Instance,
    LiteralType, NoneType, Overloaded, Parameters, ParamSpecType, PartialType,
    PlaceholderType, RawExpressionType, TupleType, Type, TypedDictType,
    TypeList, TypeVarType, UnboundType, UninhabitedType, UnionType, UnpackType, Type
)

MYPY_WHITELIST = (
    AnyType, CallableType, DeletedType, EllipsisType, ErasedType, Instance,
    LiteralType, NoneType, Overloaded, Parameters, ParamSpecType, PartialType,
    PlaceholderType, RawExpressionType, TupleType, Type, TypedDictType,
    TypeList, TypeVarType, UnboundType, UninhabitedType, UnionType, UnpackType
)


def get_fqcn(cn: object):
    """
    Get fully qualified class name
    """
    fqcn = cn.__module__
    if hasattr(cn, '__qualname__'):
        fqcn += f".{cn.__qualname__}"  # type: ignore
    elif hasattr(cn, '_name'):
        fqcn += f".{cn._name}"  # type: ignore

    return fqcn


def is_typing_list(t: Any) -> bool:
    return get_fqcn(t) == get_fqcn(List)

def is_mypy_type(t: Any) -> bool:
    """
    Check recursively, because some types can be instantiated. E.g., the type
    <TypeList 10, 20> includes the constants and is not whitelisted.
    But it has type TypeList which is in the white list.
    """
    if t in MYPY_WHITELIST:
        return True
    elif not isinstance(t, type):
        return is_mypy_type(type(t))
    return False


def make_literal(e: RawExpressionType, ctx: Optional[AnalyzeTypeContext] = None):
    if ctx:
        val = e.literal_value
        if val:
            return LiteralType(
                value=val,
                fallback=ctx.api.named_type(
                    get_fqcn(type(e.literal_value)), [])
            )
        else:
            return NoneType()
    return Literal[e]


def make_builtin(t: type, args: List[Any], ctx: Optional[AnalyzeTypeContext] = None):
    if ctx:
        return ctx.api.named_type(get_fqcn(t), args)
    return t(args)
