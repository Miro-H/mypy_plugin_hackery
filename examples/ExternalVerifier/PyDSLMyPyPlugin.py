
import logging

from mypy.plugin import Plugin
from typing import Union

from PyDSL.Constraints import Constraints
from PyDSL.Const import *

# Although not used, the following line has to be here to ensure the
# types are loaded and added to Constraints() such that they can be verified.
from PyDSL_Types import *

class PyDSLPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str):
        for n, cb in Constraints().items():
            if fullname == n:
                return cb

def plugin(version: str):
    if version not in TESTED_VERSIONS:
        logging.warning(PLUGIN_VERSION_WARNING.format(version))

    return PyDSLPlugin
