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
from .injection_child import injection_child

class injection(NamedObject[injection_child], _CreatableNamedObjectMixin[injection_child]):
    """
    'injection' child.
    """

    fluent_name = "injection"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of injection.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of injection.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of injection.
    """
    child_object_type: injection_child = injection_child
    """
    child_object_type of injection.
    """
