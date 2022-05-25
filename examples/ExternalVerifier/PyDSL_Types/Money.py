
from typing import Generic, TypeVar, Dict

from PyDSL.CustomTypes import IntTypeArgs
from PyDSL.Constraints import ConstraintContext, class_constraint

V = TypeVar("V")

class Money(IntTypeArgs, Generic[V]):
    def __init__(self, balance : Dict[V, int]) -> None:
        self.balance = balance

    def store(self, coin : V, nr : int) -> None:
        self.balance[coin] += nr
    
    def take(self, coin : V, nr : int) -> bool:
        if self.balance[coin] < nr:
            return False
        self.balance[coin] -= nr
        return True
    
    def __add__(self, other : 'Money[V]'):
        new_balance = self.balance.copy()
        for coin, nr in other.balance.items():
            new_balance[coin] += nr

        r : Money[V] = Money(new_balance)
        return r

@class_constraint(Money)
def is_valid_money(ctx: ConstraintContext):
    def limit_valid_currencies(coins):
        for coin in coins:
            if coin > 10 and coin % 5 != 0:
                return False, "Coin denominations above 10 must be multiples of 5."
        return True

    return ctx.validate_types_with_fn(limit_valid_currencies)
