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
from .entries_child import entries_child

class entries(ListObject[entries_child]):
    """
    List of observables and coefficients for linear combination of powers.
    """

    fluent_name = "entries"

    command_names = \
        ['list_properties', 'resize']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of entries.
    """
    resize: resize_cls = resize_cls
    """
    resize command of entries.
    """
    child_object_type: entries_child = entries_child
    """
    child_object_type of entries.
    """
