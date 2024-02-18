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
from .groups_child import groups_child

class groups(NamedObject[groups_child], _CreatableNamedObjectMixin[groups_child]):
    """
    'groups' child.
    """

    fluent_name = "groups"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of groups.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of groups.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of groups.
    """
    child_object_type: groups_child = groups_child
    """
    child_object_type of groups.
    """
