import logging

from math import prod
from typing import Generic, MutableSequence, TypeVar, Literal, Tuple

T = TypeVar("T")
U = TypeVar("U")

def _recursive_rewrite_literals(params):
    if hasattr(params, '__iter__'):
        orig_type = type(params)
        params = list(params)
        for i, param in enumerate(params):
            params[i] = _recursive_rewrite_literals(param)
        params = orig_type(params)
    elif isinstance(params, int):
        params = Literal[params] # type: ignore

    return params

class Vector(Generic[T, U]):
    def __init__(self, l):
        self.dim = len(l)
        self.l = l

    def __class_getitem__(self, params):
        params = _recursive_rewrite_literals(params)
        return super().__class_getitem__(params)

    def __add__(self : 'Vector[T, U]', other : 'Vector[T, U]') -> 'Vector[T, U]':
       if self.get_dim() != other.get_dim():
           logging.error("Added vectors must have the same dimensions.\n"
                         f"{self.get_dim()} != {other.get_dim()}")

       r = []
       for i in range(self.dim):
           r.append(self.l[i] + other.l[i])

       return Vector(r)

    def __str__(self):
       return f"Vector[{self.dim}] = [{', '.join(map(str, self.l))}]"

    def get_dim(self) -> int:
       return self.dim

