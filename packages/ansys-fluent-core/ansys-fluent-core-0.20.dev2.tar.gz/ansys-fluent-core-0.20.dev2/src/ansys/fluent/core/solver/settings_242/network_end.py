#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .thermal_bc import thermal_bc as thermal_bc_cls
from .temperature_1 import temperature as temperature_cls
from .q import q as q_cls
class network_end(Group):
    """
    Help not available.
    """

    fluent_name = "network-end"

    child_names = \
        ['thermal_bc', 'temperature', 'q']

    thermal_bc: thermal_bc_cls = thermal_bc_cls
    """
    thermal_bc child of network_end.
    """
    temperature: temperature_cls = temperature_cls
    """
    temperature child of network_end.
    """
    q: q_cls = q_cls
    """
    q child of network_end.
    """
