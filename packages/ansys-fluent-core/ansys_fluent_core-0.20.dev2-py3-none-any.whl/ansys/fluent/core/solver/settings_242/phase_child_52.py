#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .recirculation_inlet import recirculation_inlet as recirculation_inlet_cls
from .geometry_2 import geometry as geometry_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['recirculation_inlet', 'geometry']

    recirculation_inlet: recirculation_inlet_cls = recirculation_inlet_cls
    """
    recirculation_inlet child of phase_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of phase_child.
    """
