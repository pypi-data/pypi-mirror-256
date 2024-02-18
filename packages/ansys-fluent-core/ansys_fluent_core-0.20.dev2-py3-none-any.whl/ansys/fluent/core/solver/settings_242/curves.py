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
from .curves_child import curves_child

class curves(ListObject[curves_child]):
    """
    Set parameters for curves.
    """

    fluent_name = "curves"

    command_names = \
        ['list_properties', 'resize']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of curves.
    """
    resize: resize_cls = resize_cls
    """
    resize command of curves.
    """
    child_object_type: curves_child = curves_child
    """
    child_object_type of curves.
    """
