
import logging

from mypy.plugin import Plugin, MethodSigContext, MethodContext
from mypy.types import get_proper_type, LiteralType, Instance, UninhabitedType, AnyType, TypeOfAny
from typing import Any, Optional, Callable, Type

from PyDSL.Constraints import Constraints
from PyDSL.Const import *

# Although not used, the following line has to be here to ensure the
# types are loaded and added to Constraints() such that they can be verified.
from PyDSL_Types import *


class PyDSLPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str):
        return Constraints().get_class_constraint(fullname)

    def get_attribute_hook(self, fullname: str):
        return Constraints().get_attributes_constraint(fullname)

    def get_method_hook(self, fullname: str):
        if fullname == "PyDSL_Types.ConstList.ConstList.__add__":
            return list_concat_cb
        if fullname == "PyDSL_Types.EvenList.EvenList.__add__":
            return even_list_concat_cb

# TODO: integrate the following callbacks into constraints singleton


def list_concat_cb(ctx: MethodContext):
    # TODO: Provide simpler abstraction for custom method signature redefinition
    #   Maybe: expect: args_types=[ConstList[Literal[3]], ConstList[Literal[2]]], args_raw=[[2], [3]]
    #   i.e., a special case for type vars.
    # TODO: Can we generate the conditions below automatically?
    if (len(ctx.arg_types) == 1
            and len(ctx.arg_types[0]) == 1
            and isinstance(ctx.arg_types[0][0], Instance)
            and len(ctx.arg_types[0][0].args) == 1
            and isinstance(ctx.arg_types[0][0].args[0], LiteralType)
            and isinstance(ctx.default_return_type, Instance)
            and len(ctx.default_return_type.args) == 1
            and isinstance(ctx.default_return_type.args[0], UninhabitedType)):

        # Grab operand dimensions
        my_dim = ctx.type.args[0].value  # type: ignore
        other_dim = ctx.arg_types[0][0].args[0].value

        # Make return type more concrete (from the
        # unbound PyDSL_Types.ConstList.ConstList[<nothing>]
        # to
        # PyDSL_Types.ConstList.ConstList[Literal[my_dim + other_dim]])
        ret_arg = LiteralType(
            value=my_dim + other_dim,
            fallback=ctx.api.named_generic_type("builtins.int", [])
        )

        r = ctx.default_return_type.copy_modified(args=[ret_arg])
        return r
    return ctx.type


def even_list_concat_cb(ctx: MethodContext):
    # See list_concat_cb for comments, most of the code is the same.
    if (len(ctx.arg_types) == 1
            and len(ctx.arg_types[0]) == 1
            and isinstance(ctx.arg_types[0][0], Instance)
            and len(ctx.arg_types[0][0].args) == 1
            and isinstance(ctx.arg_types[0][0].args[0], LiteralType)
            and isinstance(ctx.default_return_type, Instance)
            and len(ctx.default_return_type.args) == 1
            and isinstance(ctx.default_return_type.args[0], UninhabitedType)):

        my_dim = ctx.type.args[0].value  # type: ignore
        other_dim = ctx.arg_types[0][0].args[0].value

        if my_dim % 2 != 0 or other_dim % 2 != 0:
            ctx.api.fail(f"Only even lists can be added, got: EvenList[{my_dim}] + EvenList[{other_dim}]", ctx.context)
            return ctx.default_return_type

        ret_arg = LiteralType(
            value=my_dim + other_dim,
            fallback=ctx.api.named_generic_type("builtins.int", [])
        )

        r = ctx.default_return_type.copy_modified(args=[ret_arg])
        return r
    return ctx.type


def plugin(version: str):
    if version not in TESTED_VERSIONS:
        logging.warning(PLUGIN_VERSION_WARNING.format(version))

    return PyDSLPlugin
