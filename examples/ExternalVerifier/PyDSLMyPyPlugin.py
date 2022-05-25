
import logging

from mypy.plugin import Plugin, AttributeContext
from typing import Any, Optional, Callable, Type

from PyDSL.Constraints import Constraints
from PyDSL.Const import *

# Although not used, the following line has to be here to ensure the
# types are loaded and added to Constraints() such that they can be verified.
from PyDSL_Types import *


class PyDSLPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str):
        for n, cb in Constraints().get_class_constraints().items():
            if fullname == n:
                return cb

    def get_attribute_hook(self, fullname: str):
        for n, cb in Constraints().get_attributes_constraints().items():
            if fullname == n:
                return cb

        return None

def plugin(version: str):
    if version not in TESTED_VERSIONS:
        logging.warning(PLUGIN_VERSION_WARNING.format(version))

    return PyDSLPlugin
