#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .axis_direction_component_child import axis_direction_component_child

class fan_origin_components(ListObject[axis_direction_component_child]):
    """
    'fan_origin_components' child.
    """

    fluent_name = "fan-origin-components"

    child_object_type: axis_direction_component_child = axis_direction_component_child
    """
    child_object_type of fan_origin_components.
    """
