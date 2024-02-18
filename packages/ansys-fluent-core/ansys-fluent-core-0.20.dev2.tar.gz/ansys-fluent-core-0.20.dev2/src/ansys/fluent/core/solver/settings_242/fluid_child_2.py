#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .type_4 import type as type_cls
from .phase_32 import phase as phase_cls
from .boundaries import boundaries as boundaries_cls
from .location_2 import location as location_cls
class fluid_child(Group):
    """
    'child_object_type' of fluid.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'type', 'phase', 'boundaries', 'location']

    name: name_cls = name_cls
    """
    name child of fluid_child.
    """
    type: type_cls = type_cls
    """
    type child of fluid_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of fluid_child.
    """
    boundaries: boundaries_cls = boundaries_cls
    """
    boundaries child of fluid_child.
    """
    location: location_cls = location_cls
    """
    location child of fluid_child.
    """
