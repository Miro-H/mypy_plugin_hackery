from .Const import *
from typing import Generic, Literal, NewType, TypeVar
from mypy.types import UnboundType

def make_literal(e):
    return Literal[e] # type: ignore

RUNTIME_CONVERSION = make_literal

# def make_literal_type(e: RawExpressionType):
#     val = e.literal_value
#     if val:
#         return LiteralType(
#             value=val, 
#             fallback=make_instance(val)
#         )
#     else:
#         return NoneType()

# RawInt = NewType("RawInt", int)

# RUNTIME_TYPE_CONVERSION: Final = {
#     RawInt.__name__: make_literal
# }

# STATIC_TYPE_CONVERSION: Final = {
#     RawInt.__name__: make_literal_type
# }

def do_raw_conversion(name, conversion, raw_val):
    return conversion[name](raw_val)

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
                # TODO: done for all literals now, how can we achieve only doing this for custom values?
                # n=NewType(...) + VarType(..., bound=n) failed because the translated type is not a subtype of
                # n anymore... And creating types of n during analysis doesn't work :(
                
                # OLD code:
                # if b and isinstance(b, FunctionType):
                #   args[i] = do_raw_conversion(b.__name__, conversion, arg)
                args[i] = conversion(arg)

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
        print("class_getitem before rewrite", params)
        params = rewrite_literals(decorated_class, RUNTIME_CONVERSION, params)
        print("class_getitem after rewrite", params)
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
