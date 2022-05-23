
from typing import Generic, TypeVar, List

T = TypeVar("T")

class MyList(Generic[T]):
    def __init__(self, l : List[T]):
        self.l = l
    
    def __add__(self : 'MyList[T]', other : 'MyList[T]') -> 'MyList[T]':
        return MyList(self.l + other.l)

    def __str__(self) -> str:
        return self.l.__str__()