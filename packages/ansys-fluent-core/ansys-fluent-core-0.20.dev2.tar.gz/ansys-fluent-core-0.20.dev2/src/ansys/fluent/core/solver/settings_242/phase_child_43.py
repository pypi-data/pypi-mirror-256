#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .momentum_5 import momentum as momentum_cls
from .potential_1 import potential as potential_cls
from .structure_1 import structure as structure_cls
from .uds_1 import uds as uds_cls
from .radiation_4 import radiation as radiation_cls
from .dpm_2 import dpm as dpm_cls
from .geometry_2 import geometry as geometry_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['momentum', 'potential', 'structure', 'uds', 'radiation', 'dpm',
         'geometry']

    momentum: momentum_cls = momentum_cls
    """
    momentum child of phase_child.
    """
    potential: potential_cls = potential_cls
    """
    potential child of phase_child.
    """
    structure: structure_cls = structure_cls
    """
    structure child of phase_child.
    """
    uds: uds_cls = uds_cls
    """
    uds child of phase_child.
    """
    radiation: radiation_cls = radiation_cls
    """
    radiation child of phase_child.
    """
    dpm: dpm_cls = dpm_cls
    """
    dpm child of phase_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of phase_child.
    """
