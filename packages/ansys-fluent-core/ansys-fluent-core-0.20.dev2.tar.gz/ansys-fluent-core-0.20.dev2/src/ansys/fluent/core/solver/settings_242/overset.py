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
from .overset_child import overset_child

class overset(NamedObject[overset_child], _NonCreatableNamedObjectMixin[overset_child]):
    """
    Settings for boundary-condition object.
    """

    fluent_name = "overset"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    delete: delete_cls = delete_cls
    """
    delete command of overset.
    """
    rename: rename_cls = rename_cls
    """
    rename command of overset.
    """
    list: list_cls = list_cls
    """
    list command of overset.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of overset.
    """
    make_a_copy: make_a_copy_cls = make_a_copy_cls
    """
    make_a_copy command of overset.
    """
    child_object_type: overset_child = overset_child
    """
    child_object_type of overset.
    """
