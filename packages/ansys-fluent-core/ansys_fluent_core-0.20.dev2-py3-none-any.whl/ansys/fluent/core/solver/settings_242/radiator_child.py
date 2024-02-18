#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .phase_23 import phase as phase_cls
from .radiator import radiator as radiator_cls
from .geometry_2 import geometry as geometry_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class radiator_child(Group):
    """
    'child_object_type' of radiator.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'radiator', 'geometry']

    name: name_cls = name_cls
    """
    name child of radiator_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of radiator_child.
    """
    radiator: radiator_cls = radiator_cls
    """
    radiator child of radiator_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of radiator_child.
    """
    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    adjacent_cell_zone: adjacent_cell_zone_cls = adjacent_cell_zone_cls
    """
    adjacent_cell_zone query of radiator_child.
    """
    shadow_face_zone: shadow_face_zone_cls = shadow_face_zone_cls
    """
    shadow_face_zone query of radiator_child.
    """
