#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .backward_compatibility import backward_compatibility as backward_compatibility_cls
from .flux_scaling import flux_scaling as flux_scaling_cls
from .print_settings import print_settings as print_settings_cls
class expert(Group):
    """
    Configure expert parameters for turbo interfaces.
    """

    fluent_name = "expert"

    child_names = \
        ['backward_compatibility']

    backward_compatibility: backward_compatibility_cls = backward_compatibility_cls
    """
    backward_compatibility child of expert.
    """
    command_names = \
        ['flux_scaling', 'print_settings']

    flux_scaling: flux_scaling_cls = flux_scaling_cls
    """
    flux_scaling command of expert.
    """
    print_settings: print_settings_cls = print_settings_cls
    """
    print_settings command of expert.
    """
