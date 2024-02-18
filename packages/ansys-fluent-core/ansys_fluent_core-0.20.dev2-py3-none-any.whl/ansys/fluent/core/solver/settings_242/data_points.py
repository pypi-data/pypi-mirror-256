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
from .data_points_child import data_points_child

class data_points(ListObject[data_points_child]):
    """
    Specify ranges and values for piecewise-linear property.
    """

    fluent_name = "data-points"

    command_names = \
        ['list_properties', 'resize']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of data_points.
    """
    resize: resize_cls = resize_cls
    """
    resize command of data_points.
    """
    child_object_type: data_points_child = data_points_child
    """
    child_object_type of data_points.
    """
