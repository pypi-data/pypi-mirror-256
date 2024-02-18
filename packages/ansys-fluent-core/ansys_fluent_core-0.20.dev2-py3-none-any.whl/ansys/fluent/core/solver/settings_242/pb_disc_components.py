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
from .fixes_child import fixes_child

class pb_disc_components(ListObject[fixes_child]):
    """
    'pb_disc_components' child.
    """

    fluent_name = "pb-disc-components"

    command_names = \
        ['list_properties', 'resize']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of pb_disc_components.
    """
    resize: resize_cls = resize_cls
    """
    resize command of pb_disc_components.
    """
    child_object_type: fixes_child = fixes_child
    """
    child_object_type of pb_disc_components.
    """
