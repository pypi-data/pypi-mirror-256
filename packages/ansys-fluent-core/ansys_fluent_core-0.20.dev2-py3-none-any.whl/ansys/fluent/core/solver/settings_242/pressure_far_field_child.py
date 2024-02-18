#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .phase_20 import phase as phase_cls
from .momentum_7 import momentum as momentum_cls
from .turbulence_2 import turbulence as turbulence_cls
from .thermal_4 import thermal as thermal_cls
from .radiation_1 import radiation as radiation_cls
from .species_9 import species as species_cls
from .dpm_2 import dpm as dpm_cls
from .potential_1 import potential as potential_cls
from .structure_1 import structure as structure_cls
from .uds_1 import uds as uds_cls
from .icing_1 import icing as icing_cls
from .geometry_2 import geometry as geometry_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class pressure_far_field_child(Group):
    """
    'child_object_type' of pressure_far_field.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'momentum', 'turbulence', 'thermal', 'radiation',
         'species', 'dpm', 'potential', 'structure', 'uds', 'icing',
         'geometry']

    name: name_cls = name_cls
    """
    name child of pressure_far_field_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of pressure_far_field_child.
    """
    momentum: momentum_cls = momentum_cls
    """
    momentum child of pressure_far_field_child.
    """
    turbulence: turbulence_cls = turbulence_cls
    """
    turbulence child of pressure_far_field_child.
    """
    thermal: thermal_cls = thermal_cls
    """
    thermal child of pressure_far_field_child.
    """
    radiation: radiation_cls = radiation_cls
    """
    radiation child of pressure_far_field_child.
    """
    species: species_cls = species_cls
    """
    species child of pressure_far_field_child.
    """
    dpm: dpm_cls = dpm_cls
    """
    dpm child of pressure_far_field_child.
    """
    potential: potential_cls = potential_cls
    """
    potential child of pressure_far_field_child.
    """
    structure: structure_cls = structure_cls
    """
    structure child of pressure_far_field_child.
    """
    uds: uds_cls = uds_cls
    """
    uds child of pressure_far_field_child.
    """
    icing: icing_cls = icing_cls
    """
    icing child of pressure_far_field_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of pressure_far_field_child.
    """
    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    adjacent_cell_zone: adjacent_cell_zone_cls = adjacent_cell_zone_cls
    """
    adjacent_cell_zone query of pressure_far_field_child.
    """
    shadow_face_zone: shadow_face_zone_cls = shadow_face_zone_cls
    """
    shadow_face_zone query of pressure_far_field_child.
    """
