#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .phase_26 import phase as phase_cls
from .recirculation_outlet import recirculation_outlet as recirculation_outlet_cls
from .geometry_2 import geometry as geometry_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class recirculation_outlet_child(Group):
    """
    'child_object_type' of recirculation_outlet.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'recirculation_outlet', 'geometry']

    name: name_cls = name_cls
    """
    name child of recirculation_outlet_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of recirculation_outlet_child.
    """
    recirculation_outlet: recirculation_outlet_cls = recirculation_outlet_cls
    """
    recirculation_outlet child of recirculation_outlet_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of recirculation_outlet_child.
    """
    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    adjacent_cell_zone: adjacent_cell_zone_cls = adjacent_cell_zone_cls
    """
    adjacent_cell_zone query of recirculation_outlet_child.
    """
    shadow_face_zone: shadow_face_zone_cls = shadow_face_zone_cls
    """
    shadow_face_zone query of recirculation_outlet_child.
    """
