
from typing import Annotated, TypeVar, Generic, List

from PyDSL.CustomTypes import ConvertRawLiterals

U = TypeVar("U", bound=Annotated[int, ConvertRawLiterals])

# TODO: overwrite add that only some sizes are allowed to be added if one of the types is even

class EvenList(Generic[U]):
    def __init__(self, l: List) -> None:
        self.l = l