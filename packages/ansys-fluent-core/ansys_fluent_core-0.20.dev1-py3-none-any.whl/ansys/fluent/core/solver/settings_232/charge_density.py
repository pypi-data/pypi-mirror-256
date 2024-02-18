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
from .user_defined_function import user_defined_function as user_defined_function_cls
class charge_density(Group):
    """
    'charge_density' child.
    """

    fluent_name = "charge-density"

    child_names = \
        ['option', 'value', 'user_defined_function']

    option: option_cls = option_cls
    """
    option child of charge_density.
    """
    value: value_cls = value_cls
    """
    value child of charge_density.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of charge_density.
    """
