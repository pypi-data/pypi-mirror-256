#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .solid_child import solid_child

class solid(NamedObject[solid_child], _CreatableNamedObjectMixin[solid_child]):
    """
    'solid' child.
    """

    fluent_name = "solid"

    child_object_type: solid_child = solid_child
    """
    child_object_type of solid.
    """
