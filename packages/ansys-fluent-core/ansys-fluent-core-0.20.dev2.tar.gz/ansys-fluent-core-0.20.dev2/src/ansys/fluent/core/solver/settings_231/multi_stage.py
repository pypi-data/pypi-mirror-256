#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .multi_stage_child import multi_stage_child

class multi_stage(ListObject[multi_stage_child]):
    """
    'multi_stage' child.
    """

    fluent_name = "multi-stage"

    child_object_type: multi_stage_child = multi_stage_child
    """
    child_object_type of multi_stage.
    """
