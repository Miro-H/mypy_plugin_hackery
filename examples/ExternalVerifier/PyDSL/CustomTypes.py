from typing import Literal, Union

from .Const import *

def _recursive_rewrite_literals(params, type_to_rewrite):
    if hasattr(params, '__iter__'):
        orig_type = type(params)
        params = list(params)
        for i, param in enumerate(params):
            params[i] = _recursive_rewrite_literals(param, type_to_rewrite)
        params = orig_type(params)
    elif isinstance(params, type_to_rewrite):
        params = Literal[params]  # type: ignore

    return params


class IntTypeArgs:
    def __class_getitem__(self, params):
        params = _recursive_rewrite_literals(params, int)
        return super().__class_getitem__(params)


class BoolTypeArgs:
    def __class_getitem__(self, params):
        params = _recursive_rewrite_literals(params, bool)
        return super().__class_getitem__(params)
