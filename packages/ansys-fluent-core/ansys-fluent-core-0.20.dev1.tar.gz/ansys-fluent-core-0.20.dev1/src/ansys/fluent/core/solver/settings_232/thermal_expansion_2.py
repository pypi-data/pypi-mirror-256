#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .value_1 import value as value_cls
class thermal_expansion_2(Group):
    """
    'thermal_expansion_2' child.
    """

    fluent_name = "thermal-expansion-2"

    child_names = \
        ['option', 'value']

    option: option_cls = option_cls
    """
    option child of thermal_expansion_2.
    """
    value: value_cls = value_cls
    """
    value child of thermal_expansion_2.
    """
