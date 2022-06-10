"""
This file contains internal helper functions that are not intended for the use outside of PyDSL.
"""

from typing import Optional, Literal, List, Any
from mypy.plugin import AnalyzeTypeContext
from mypy.types import RawExpressionType, LiteralType, NoneType


def get_fqcn(cn: object):
    """
    Get fully qualified class name
    """
    fqcn = cn.__module__
    if hasattr(cn, '__qualname__'):
        fqcn += f".{cn.__qualname__}"  # type: ignore

    return fqcn


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
