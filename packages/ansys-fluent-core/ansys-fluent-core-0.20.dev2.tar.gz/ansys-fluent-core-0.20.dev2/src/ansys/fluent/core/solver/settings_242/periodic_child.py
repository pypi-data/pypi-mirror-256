#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .phase_18 import phase as phase_cls
from .ai import ai as ai_cls
from .aj import aj as aj_cls
from .ak import ak as ak_cls
from .x_origin import x_origin as x_origin_cls
from .y_origin import y_origin as y_origin_cls
from .z_origin import z_origin as z_origin_cls
from .shift_x import shift_x as shift_x_cls
from .shift_y import shift_y as shift_y_cls
from .shift_z import shift_z as shift_z_cls
from .periodic import periodic as periodic_cls
from .geometry_2 import geometry as geometry_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class periodic_child(Group):
    """
    'child_object_type' of periodic.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'ai', 'aj', 'ak', 'x_origin', 'y_origin',
         'z_origin', 'shift_x', 'shift_y', 'shift_z', 'periodic', 'geometry']

    name: name_cls = name_cls
    """
    name child of periodic_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of periodic_child.
    """
    ai: ai_cls = ai_cls
    """
    ai child of periodic_child.
    """
    aj: aj_cls = aj_cls
    """
    aj child of periodic_child.
    """
    ak: ak_cls = ak_cls
    """
    ak child of periodic_child.
    """
    x_origin: x_origin_cls = x_origin_cls
    """
    x_origin child of periodic_child.
    """
    y_origin: y_origin_cls = y_origin_cls
    """
    y_origin child of periodic_child.
    """
    z_origin: z_origin_cls = z_origin_cls
    """
    z_origin child of periodic_child.
    """
    shift_x: shift_x_cls = shift_x_cls
    """
    shift_x child of periodic_child.
    """
    shift_y: shift_y_cls = shift_y_cls
    """
    shift_y child of periodic_child.
    """
    shift_z: shift_z_cls = shift_z_cls
    """
    shift_z child of periodic_child.
    """
    periodic: periodic_cls = periodic_cls
    """
    periodic child of periodic_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of periodic_child.
    """
    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    adjacent_cell_zone: adjacent_cell_zone_cls = adjacent_cell_zone_cls
    """
    adjacent_cell_zone query of periodic_child.
    """
    shadow_face_zone: shadow_face_zone_cls = shadow_face_zone_cls
    """
    shadow_face_zone query of periodic_child.
    """
