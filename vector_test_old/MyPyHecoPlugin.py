
import logging

from typing import Final, Literal, List
from mypy.plugin import Plugin, AnalyzeTypeContext
from mypy.types import (
    AnyType, LiteralType, RawExpressionType, Type, TypeOfAny, 
    UnboundType
)

# TODO: write vector verifier in VectorType, use Annotated to add fetch these
# constraints and apply them here!

VECTOR_TYPE_NAME : Final = "examples.VectorType.Vector"

class HecoPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str):
        if fullname == VECTOR_TYPE_NAME:
            return heco_vector_analyze_callback

def _vector_type_check(ts):
    exp = [ ([UnboundType], ["str", "int", "T"]) ] + \
          [ ([RawExpressionType, UnboundType], ["int", "U"]) ]
    l_exp = len(exp)

    print(ts)

    # TODO: quick fix to allow untyped arguments in class definition, is there a better solution than to 
    # allow this for all Vector instances?
    if len(ts) == 0:
        return True

    if len(ts) != l_exp: 
        print("len")
        return False

    for i in range(len(ts)):
        print(type(ts[i]), ts[i].name if hasattr(ts[i], 'name') else ts[i].simple_name())
        cs_exp, ns_exp = exp[i]
        if not any([ isinstance(ts[i], c_exp) for c_exp in cs_exp]):
            print("isinstance")
            return False
        if hasattr(ts[i], 'name') and all([ts[i].name != n_exp for n_exp in ns_exp]):
            print("name")
            return False
        if hasattr(ts[i], 'simple_name') and all([ts[i].simple_name() != n_exp for n_exp in ns_exp]):
            print("simple_name")
            return False

    return True

def heco_vector_analyze_callback(ctx: AnalyzeTypeContext) -> Type:
    if not _vector_type_check(ctx.type.args):
        ctx.api.fail('Invalid "Vector" type (expected "Vector[int, nr]")', ctx.context)
        return AnyType(TypeOfAny.from_error)

    ts : List[Type] = []
    for arg in ctx.type.args:
        # The latter is implied but here to satisfy MyPy type checking
        if isinstance(arg, RawExpressionType) and isinstance(arg.literal_value, int):
            # All raw expressions are dimensions (i.e., integers)
            ts.append(LiteralType(value=arg.literal_value, 
                fallback=ctx.api.named_type(arg.base_type_name, [])))
        elif isinstance(arg, UnboundType):
            # The UnboundType describes the vector content and only supports int
            print("UNBOUND:", arg)
            if hasattr(arg, 'name'):
                if arg.name == 'int':
                    ts.append(ctx.api.named_type("builtins.int", []))
                elif arg.name == 'str':
                    ts.append(ctx.api.named_type("builtins.str", []))
                else:
                    ts.append(arg)
            else:
                ts.append(arg)

    r = ctx.api.named_type(VECTOR_TYPE_NAME, ts)
    print("Return r =", r)
    return r

def plugin(version: str):
    if version != "0.950":
        logging.warning(f"The custom HecoPlugin for MyPy was not tested with your MyPy version {version}.")
    return HecoPlugin
