#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .axis_direction_component_child import axis_direction_component_child

class axis_origin_component(ListObject[axis_direction_component_child]):
    """
    'axis_origin_component' child.
    """

    fluent_name = "axis-origin-component"

    child_object_type: axis_direction_component_child = axis_direction_component_child
    """
    child_object_type of axis_origin_component.
    """
