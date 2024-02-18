#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
from .uds_diffusivities import uds_diffusivities as uds_diffusivities_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class uds_diffusivity(Group):
    """
    'uds_diffusivity' child.
    """

    fluent_name = "uds-diffusivity"

    child_names = \
        ['option', 'uds_diffusivities', 'user_defined_function']

    option: option_cls = option_cls
    """
    option child of uds_diffusivity.
    """
    uds_diffusivities: uds_diffusivities_cls = uds_diffusivities_cls
    """
    uds_diffusivities child of uds_diffusivity.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of uds_diffusivity.
    """
