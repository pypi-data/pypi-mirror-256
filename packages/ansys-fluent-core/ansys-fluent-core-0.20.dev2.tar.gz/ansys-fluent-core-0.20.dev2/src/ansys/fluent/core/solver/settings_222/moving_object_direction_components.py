#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .child_object_type_child import child_object_type_child

class moving_object_direction_components(ListObject[child_object_type_child]):
    """
    'moving_object_direction_components' child.
    """

    fluent_name = "moving-object-direction-components"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of moving_object_direction_components.
    """
