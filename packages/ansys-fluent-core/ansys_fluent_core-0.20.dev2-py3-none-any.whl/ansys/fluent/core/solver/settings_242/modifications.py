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
from .modifications_child import modifications_child

class modifications(ListObject[modifications_child]):
    """
    'modifications' child.
    """

    fluent_name = "modifications"

    command_names = \
        ['list_properties', 'resize']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of modifications.
    """
    resize: resize_cls = resize_cls
    """
    resize command of modifications.
    """
    child_object_type: modifications_child = modifications_child
    """
    child_object_type of modifications.
    """
