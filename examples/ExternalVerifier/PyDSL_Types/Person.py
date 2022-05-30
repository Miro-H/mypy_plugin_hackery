from PyDSL.HecoTypes import Secret
from PyDSL.Constraints import AttributeConstraintContext, attribute_constraint
from PyDSL.InternalUtils import get_fqcn
from PyDSL.TypeFinderVisitor import TypeFinderVisitor

class Person:
    name: str
    age: int

    health_record: Secret[str]
    salary: Secret[int]

    def __init__(self, name, age, health_record, salary) -> None:
        self.name = name
        self.age = age
        # False positives, didn't found a way to allow class internal access to secret values
        self.health_record = health_record # type: ignore
        self.salary = salary # type: ignore

    def get_name(self) -> str:
        return self.name

    # Marked as error because it accesses a secret variable
    # def leak(self) -> Secret[int]:
    #     return self.salary

@attribute_constraint(Person)
def is_valid_person_attribute(ctx: AttributeConstraintContext):
    v = TypeFinderVisitor(Secret)
    has_secret = ctx.type.accept(v)
    return not has_secret