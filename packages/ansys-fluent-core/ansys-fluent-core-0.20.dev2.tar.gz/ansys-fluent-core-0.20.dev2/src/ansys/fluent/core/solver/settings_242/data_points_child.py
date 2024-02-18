#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .item import item as item_cls
from .value_4 import value as value_cls
class data_points_child(Group):
    """
    'child_object_type' of data_points.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['item', 'value']

    item: item_cls = item_cls
    """
    item child of data_points_child.
    """
    value: value_cls = value_cls
    """
    value child of data_points_child.
    """
