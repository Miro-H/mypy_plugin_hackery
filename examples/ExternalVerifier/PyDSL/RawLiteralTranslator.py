from typing import List, Union
from mypy.types import (
    AnyType, CallableType, DeletedType, EllipsisType, ErasedType, Instance,
    LiteralType, NoneType, Overloaded, Parameters, ParamSpecType, PartialType,
    PlaceholderType, RawExpressionType, TupleType, Type, TypedDictType,
    TypeList, TypeVarType, UnboundType, UninhabitedType, UnionType, UnpackType
)
from mypy.type_visitor import TypeQuery

# typing does not allow us to inherit directly from SyntheticTypeVisitor
# and using TypeTranslator is not accepted by mypy types like RawExpressionType.
# Thus, we need to use TypeQuery and overwrite some of the changes it made to
# SyntheticTypeVisitor.

RetType = Union[Type, List[Type]]


class RawLiteralTranslator(TypeQuery[RetType]):
    """
    Translate all raw literals in a type (can be complex and nested)
    """

    # We know that the strategy always returns a list, but MyPy doesn't
    # understand this, so we need to add a lot of type: ignore statements
    def __init__(self, conversion) -> None:
        self.conversion = conversion

        def nop_strategy(l) -> List[Type]:
            return l

        super().__init__(nop_strategy)

    def visit_unbound_type(self, t: UnboundType) -> Type:
        t.args = self.query_types(t.args)  # type: ignore
        return t

    def visit_type_list(self, t: TypeList) -> Type:
        r = super().visit_type_list(t)
        t.items = r  # type: ignore
        return t

    def visit_type_var(self, t: TypeVarType) -> Type:
        t.upper_bound = self.query_types([t.upper_bound])[0]  # type: ignore
        t.values = self.query_types(t.values)  # type: ignore
        return t

    def visit_unpack_type(self, t: UnpackType) -> Type:
        t.type = self.query_types([t.type])[0]  # type: ignore
        return t

    def visit_parameters(self, t: Parameters) -> Type:
        t.arg_types = self.query_types(t.arg_types)  # type: ignore
        return t

    def visit_instance(self, t: Instance) -> Type:
        t.args = self.query_types(t.args)  # type: ignore
        return t

    def visit_callable_type(self, t: CallableType) -> Type:
        t.arg_types = self.query_types(t.arg_types)  # type: ignore
        t.ret_type = self.query_types([t.ret_type])[0]  # type: ignore
        return t

    def visit_tuple_type(self, t: TupleType) -> Type:
        t.items = self.query_types(t.items)  # type: ignore
        return t

    def visit_typeddict_type(self, t: TypedDictType) -> Type:
        r = self.query_types(t.items.values())
        for i, k in enumerate(t.items.keys()):
            t.items[k] = r[i]  # type: ignore
        return t

    def visit_raw_expression_type(self, t: RawExpressionType) -> Type:
        return self.conversion(t)

    def visit_union_type(self, t: UnionType) -> Type:
        t.items = self.query_types(t.items)  # type: ignore
        return t

    def visit_overloaded(self, t: Overloaded) -> Type:
        t.items = self.query_types(t.items)  # type: ignore
        return t

    def visit_placeholder_type(self, t: PlaceholderType) -> Type:
        t.args = self.query_types(t.args)  # type: ignore
        return t

    #
    # NOPs
    #
    def visit_any(self, t: AnyType) -> Type:
        return t

    def visit_uninhabited_type(self, t: UninhabitedType) -> Type:
        return t

    def visit_none_type(self, t: NoneType) -> Type:
        return t

    def visit_erased_type(self, t: ErasedType) -> Type:
        return t

    def visit_deleted_type(self, t: DeletedType) -> Type:
        return t

    def visit_param_spec(self, t: ParamSpecType) -> Type:
        return t

    def visit_partial_type(self, t: PartialType) -> Type:
        return t

    def visit_literal_type(self, t: LiteralType) -> Type:
        return t

    def visit_ellipsis_type(self, t: EllipsisType) -> Type:
        return t
