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
from .templated_child import templated_child

class templated(NamedObject[templated_child], _CreatableNamedObjectMixin[templated_child]):
    """
    Adjoint-observables-named named-object-class.
    """

    fluent_name = "templated"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    delete: delete_cls = delete_cls
    """
    delete command of templated.
    """
    rename: rename_cls = rename_cls
    """
    rename command of templated.
    """
    list: list_cls = list_cls
    """
    list command of templated.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of templated.
    """
    make_a_copy: make_a_copy_cls = make_a_copy_cls
    """
    make_a_copy command of templated.
    """
    child_object_type: templated_child = templated_child
    """
    child_object_type of templated.
    """
