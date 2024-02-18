#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .range_child import range_child

class range(ListObject[range_child]):
    """
    Specify piecewise-polynomial settings.
    """

    fluent_name = "range"

    command_names = \
        ['list_properties', 'resize']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of range.
    """
    resize: resize_cls = resize_cls
    """
    resize command of range.
    """
    child_object_type: range_child = range_child
    """
    child_object_type of range.
    """
