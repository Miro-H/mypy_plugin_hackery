from PyDSL.HecoTypes import Secret
from PyDSL.Constraints import AttributeConstraintContext, attribute_constraint, class_constraint, ConstraintContext
from PyDSL.InternalUtils import get_fqcn

class Person:
    name: str
    age: int

    health_record: Secret[str]
    salary: Secret[int]

    def __init__(self, name, age, health_record, salary) -> None:
        self.name = name
        self.age = age
        self.health_record = health_record
        self.salary = salary

    def get_name(self) -> str:
        return self.name

    def leak(self) -> Secret[int]:
        return self.salary

@attribute_constraint(Person)
def is_valid_person_attribute(ctx: AttributeConstraintContext):
    # TODO: should write visitor to check for secret values in nested expressions
    return get_fqcn(Secret) != ctx.type.type.fullname # type: ignore