#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .child_object_type_child import child_object_type_child

class momentum_source_components(ListObject[child_object_type_child]):
    """
    'momentum_source_components' child.
    """

    fluent_name = "momentum-source-components"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of momentum_source_components.
    """
