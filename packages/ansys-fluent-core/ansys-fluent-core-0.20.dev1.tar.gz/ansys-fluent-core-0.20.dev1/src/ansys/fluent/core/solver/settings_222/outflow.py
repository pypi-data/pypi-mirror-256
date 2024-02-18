#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .change_type import change_type as change_type_cls
from .outflow_child import outflow_child

class outflow(NamedObject[outflow_child], _CreatableNamedObjectMixin[outflow_child]):
    """
    'outflow' child.
    """

    fluent_name = "outflow"

    command_names = \
        ['change_type']

    change_type: change_type_cls = change_type_cls
    """
    change_type command of outflow.
    """
    child_object_type: outflow_child = outflow_child
    """
    child_object_type of outflow.
    """
