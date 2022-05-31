from .Const import *
from typing import Iterator, Literal, Union, TypeVar, List


def _recursive_rewrite_literals(params, type_to_rewrite):
    # TODO: Do nothing to other type except literals, but only the corresponding type variable is of the kind that allows raw integers.
    if hasattr(params, "__iter__"):
        orig_type = type(params)
        params = list(params)
        for i, param in enumerate(params):
            params[i] = _recursive_rewrite_literals(param, type_to_rewrite)
        params = orig_type(params)
    elif isinstance(params, type_to_rewrite):
        params = Literal[params]  # type: ignore

    return params

# TODO: continue
def has_custom_bound(param: Union[TypeVar, List[TypeVar]],
                     aggregate: bool = False) -> Union[bool, List[bool]]:

    if hasattr(param, "__iter__"):
        response_rec = map(lambda x: has_custom_bound(
            x, aggregate=True), param)
        if aggregate:
            return any(response_rec)
        return list(response_rec)
    
    return param.__bound__ != None and issubclass(param.__bound__, CustomTypes) # type: ignore


def custom_types(decorated_class):
    """
    Decorator to catch the runtime errors that are produced when literals
    are used directly in the type system.
    """
    decorated_class_getitem = decorated_class.__class_getitem__

    def __class_getitem__(params):  # cls is implicit
        # TODO
        print(decorated_class.__parameters__)
        params = _recursive_rewrite_literals(params, int)
        return decorated_class_getitem(params=params)

    decorated_class.__class_getitem__ = __class_getitem__
    return decorated_class


class CustomTypes:
    pass


class IntKind(CustomTypes):
    l: int

    def __init__(self, d: int) -> None:
        self.d = d


class Int8(IntKind):
    l = 8


class Int16(IntKind):
    l = 16


class Int32(IntKind):
    l = 32


class Int64(IntKind):
    l = 64
