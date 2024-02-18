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
from .test_data_sets_child import test_data_sets_child

class test_data_sets(ListObject[test_data_sets_child]):
    """
    'test_data_sets' child.
    """

    fluent_name = "test-data-sets"

    command_names = \
        ['list_properties', 'resize']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of test_data_sets.
    """
    resize: resize_cls = resize_cls
    """
    resize command of test_data_sets.
    """
    child_object_type: test_data_sets_child = test_data_sets_child
    """
    child_object_type of test_data_sets.
    """
