#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .axis_direction_child import axis_direction_child

class output_parameters(NamedObject[axis_direction_child], _NonCreatableNamedObjectMixin[axis_direction_child]):
    """
    Output Parameter Values of Design Point.
    """

    fluent_name = "output-parameters"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of output_parameters.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of output_parameters.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of output_parameters.
    """
    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of output_parameters.
    """
