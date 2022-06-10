
import logging

from mypy.plugin import Plugin, MethodSigContext
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
    
    def get_method_signature_hook(self, fullname: str):
        if fullname == "PyDSL_Types.ConstList.ConstList.__add__":
            return test_cb

def test_cb(ctx: MethodSigContext):
    print(ctx.type, type(ctx.type))
    print(ctx.context)
    # TODO: continue here!

def plugin(version: str):
    if version not in TESTED_VERSIONS:
        logging.warning(PLUGIN_VERSION_WARNING.format(version))

    return PyDSLPlugin
