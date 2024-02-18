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
from .discretization_child import discretization_child

class discretization(NamedObject[discretization_child], _NonCreatableNamedObjectMixin[discretization_child]):
    """
    Enter the adjoint solution methods menu.
    """

    fluent_name = "discretization"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    delete: delete_cls = delete_cls
    """
    delete command of discretization.
    """
    rename: rename_cls = rename_cls
    """
    rename command of discretization.
    """
    list: list_cls = list_cls
    """
    list command of discretization.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of discretization.
    """
    make_a_copy: make_a_copy_cls = make_a_copy_cls
    """
    make_a_copy command of discretization.
    """
    child_object_type: discretization_child = discretization_child
    """
    child_object_type of discretization.
    """
