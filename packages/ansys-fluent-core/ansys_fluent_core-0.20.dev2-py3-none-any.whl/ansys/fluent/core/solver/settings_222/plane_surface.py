#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .plane_surface_child import plane_surface_child

class plane_surface(NamedObject[plane_surface_child], _CreatableNamedObjectMixin[plane_surface_child]):
    """
    'plane_surface' child.
    """

    fluent_name = "plane-surface"

    child_object_type: plane_surface_child = plane_surface_child
    """
    child_object_type of plane_surface.
    """
