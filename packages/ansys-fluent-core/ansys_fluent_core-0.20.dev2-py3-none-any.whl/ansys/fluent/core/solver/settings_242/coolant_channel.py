#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_20 import enabled as enabled_cls
from .coolant_zone_list import coolant_zone_list as coolant_zone_list_cls
from .coolant_density import coolant_density as coolant_density_cls
class coolant_channel(Group):
    """
    Set up coolant channel.
    """

    fluent_name = "coolant-channel"

    child_names = \
        ['enabled', 'coolant_zone_list', 'coolant_density']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of coolant_channel.
    """
    coolant_zone_list: coolant_zone_list_cls = coolant_zone_list_cls
    """
    coolant_zone_list child of coolant_channel.
    """
    coolant_density: coolant_density_cls = coolant_density_cls
    """
    coolant_density child of coolant_channel.
    """
