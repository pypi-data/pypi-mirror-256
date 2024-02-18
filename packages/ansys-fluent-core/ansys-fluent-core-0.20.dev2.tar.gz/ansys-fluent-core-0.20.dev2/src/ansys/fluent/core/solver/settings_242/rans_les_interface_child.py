#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .phase_24 import phase as phase_cls
from .turbulence_4 import turbulence as turbulence_cls
from .geometry_2 import geometry as geometry_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class rans_les_interface_child(Group):
    """
    'child_object_type' of rans_les_interface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'turbulence', 'geometry']

    name: name_cls = name_cls
    """
    name child of rans_les_interface_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of rans_les_interface_child.
    """
    turbulence: turbulence_cls = turbulence_cls
    """
    turbulence child of rans_les_interface_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of rans_les_interface_child.
    """
    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    adjacent_cell_zone: adjacent_cell_zone_cls = adjacent_cell_zone_cls
    """
    adjacent_cell_zone query of rans_les_interface_child.
    """
    shadow_face_zone: shadow_face_zone_cls = shadow_face_zone_cls
    """
    shadow_face_zone query of rans_les_interface_child.
    """
