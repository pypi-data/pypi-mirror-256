#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .phase_15 import phase as phase_cls
from .momentum_5 import momentum as momentum_cls
from .potential_1 import potential as potential_cls
from .structure_1 import structure as structure_cls
from .uds_1 import uds as uds_cls
from .radiation_4 import radiation as radiation_cls
from .dpm_2 import dpm as dpm_cls
from .geometry_2 import geometry as geometry_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class outflow_child(Group):
    """
    'child_object_type' of outflow.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'momentum', 'potential', 'structure', 'uds',
         'radiation', 'dpm', 'geometry']

    name: name_cls = name_cls
    """
    name child of outflow_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of outflow_child.
    """
    momentum: momentum_cls = momentum_cls
    """
    momentum child of outflow_child.
    """
    potential: potential_cls = potential_cls
    """
    potential child of outflow_child.
    """
    structure: structure_cls = structure_cls
    """
    structure child of outflow_child.
    """
    uds: uds_cls = uds_cls
    """
    uds child of outflow_child.
    """
    radiation: radiation_cls = radiation_cls
    """
    radiation child of outflow_child.
    """
    dpm: dpm_cls = dpm_cls
    """
    dpm child of outflow_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of outflow_child.
    """
    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    adjacent_cell_zone: adjacent_cell_zone_cls = adjacent_cell_zone_cls
    """
    adjacent_cell_zone query of outflow_child.
    """
    shadow_face_zone: shadow_face_zone_cls = shadow_face_zone_cls
    """
    shadow_face_zone query of outflow_child.
    """
