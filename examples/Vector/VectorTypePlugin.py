
import logging

from typing import Final, List, Tuple, cast
from mypy.plugin import Plugin, AnalyzeTypeContext
from mypy.types import (
    AnyType, Instance, LiteralType, RawExpressionType, Type, TypeOfAny, 
    TypeVarType
)

# TODO: write vector verifier in VectorType, use Annotated to add fetch these
# constraints and apply them here!

VECTOR_TYPE_NAME : Final = "VectorType.Vector"

class HecoPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str):
        if fullname == VECTOR_TYPE_NAME:
            return heco_vector_analyze_callback

def _is_builtins_int(t : Type) -> bool:
    return isinstance(t, Instance) and t.type.fullname == "builtins.int"

def _is_literal_int(t: Type) -> bool:
    return isinstance(t, RawExpressionType) and isinstance(t.literal_value, int)

def heco_vector_analyze_callback(ctx: AnalyzeTypeContext) -> Type:
    args = ctx.type.args
    t0 = ctx.api.analyze_type(args[0])
    t_ts : List[Type] = [t0]

    if len(args) == 2:
        success = True
        if _is_builtins_int(t0) and _is_literal_int(args[1]):
            # Accept definitions of the form Vector[int, nr], where nr is a literal int
            t_ts = [ 
                t0,
                LiteralType(value=args[1].literal_value, # type: ignore
                    fallback=ctx.api.named_type(args[1].base_type_name, [])) # type: ignore
            ]
        elif isinstance(t0, TypeVarType):
            # Accept definitions in class with unspecified type variables (e.g., Vector[T, U]) 
            t1 = ctx.api.analyze_type(args[1])
            if isinstance(t0, TypeVarType):
                t_ts = [t0, t1]
        else: 
            success = False
        
        if success:
            r = ctx.api.named_type(VECTOR_TYPE_NAME, t_ts)
            # print("Return r =", r)
            return r

    ctx.api.fail('Invalid "Vector" type (expected "Vector[int, nr]")', ctx.context)
    return AnyType(TypeOfAny.from_error)


def plugin(version: str):
    if version != "0.950":
        logging.warning(f"The custom HecoPlugin for MyPy was not tested with your MyPy version {version}.")
    return HecoPlugin
