#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .child_object_type_child_1 import child_object_type_child

class moving_mesh_axis_direction(ListObject[child_object_type_child]):
    """
    'moving_mesh_axis_direction' child.
    """

    fluent_name = "moving-mesh-axis-direction"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of moving_mesh_axis_direction.
    """
