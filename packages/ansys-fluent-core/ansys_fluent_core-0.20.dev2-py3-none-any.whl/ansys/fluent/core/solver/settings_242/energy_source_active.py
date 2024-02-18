#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .energy_source_active_child import energy_source_active_child

class energy_source_active(NamedObject[energy_source_active_child], _NonCreatableNamedObjectMixin[energy_source_active_child]):
    """
    Set energy source for active zone.
    """

    fluent_name = "energy-source-active"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    delete: delete_cls = delete_cls
    """
    delete command of energy_source_active.
    """
    rename: rename_cls = rename_cls
    """
    rename command of energy_source_active.
    """
    list: list_cls = list_cls
    """
    list command of energy_source_active.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of energy_source_active.
    """
    make_a_copy: make_a_copy_cls = make_a_copy_cls
    """
    make_a_copy command of energy_source_active.
    """
    child_object_type: energy_source_active_child = energy_source_active_child
    """
    child_object_type of energy_source_active.
    """
