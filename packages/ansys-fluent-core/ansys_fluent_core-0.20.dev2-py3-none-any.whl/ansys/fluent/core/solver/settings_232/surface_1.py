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
from .surface_child import surface_child

class surface(NamedObject[surface_child], _CreatableNamedObjectMixin[surface_child]):
    """
    'surface' child.
    """

    fluent_name = "surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of surface.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of surface.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of surface.
    """
    child_object_type: surface_child = surface_child
    """
    child_object_type of surface.
    """
