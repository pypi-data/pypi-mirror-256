#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .phase_5 import phase as phase_cls
from .fan import fan as fan_cls
from .geometry_2 import geometry as geometry_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class fan_child(Group):
    """
    'child_object_type' of fan.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'fan', 'geometry']

    name: name_cls = name_cls
    """
    name child of fan_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of fan_child.
    """
    fan: fan_cls = fan_cls
    """
    fan child of fan_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of fan_child.
    """
    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    adjacent_cell_zone: adjacent_cell_zone_cls = adjacent_cell_zone_cls
    """
    adjacent_cell_zone query of fan_child.
    """
    shadow_face_zone: shadow_face_zone_cls = shadow_face_zone_cls
    """
    shadow_face_zone query of fan_child.
    """
