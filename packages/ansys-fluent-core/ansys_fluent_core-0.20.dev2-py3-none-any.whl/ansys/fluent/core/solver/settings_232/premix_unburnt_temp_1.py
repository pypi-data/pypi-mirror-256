#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class premix_unburnt_temp(Group):
    """
    'premix_unburnt_temp' child.
    """

    fluent_name = "premix-unburnt-temp"

    child_names = \
        ['option', 'user_defined_function']

    option: option_cls = option_cls
    """
    option child of premix_unburnt_temp.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of premix_unburnt_temp.
    """
