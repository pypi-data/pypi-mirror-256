#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .type_5 import type as type_cls
from .location_2 import location as location_cls
from .phase_39 import phase as phase_cls
class interior_child(Group):
    """
    'child_object_type' of interior.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'type', 'location', 'phase']

    name: name_cls = name_cls
    """
    name child of interior_child.
    """
    type: type_cls = type_cls
    """
    type child of interior_child.
    """
    location: location_cls = location_cls
    """
    location child of interior_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of interior_child.
    """
