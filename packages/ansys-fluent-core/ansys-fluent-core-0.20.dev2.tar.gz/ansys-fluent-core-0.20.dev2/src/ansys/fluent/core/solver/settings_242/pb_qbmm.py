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
from .fixes_child import fixes_child

class pb_qbmm(NamedObject[fixes_child], _NonCreatableNamedObjectMixin[fixes_child]):
    """
    'pb_qbmm' child.
    """

    fluent_name = "pb-qbmm"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    delete: delete_cls = delete_cls
    """
    delete command of pb_qbmm.
    """
    rename: rename_cls = rename_cls
    """
    rename command of pb_qbmm.
    """
    list: list_cls = list_cls
    """
    list command of pb_qbmm.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of pb_qbmm.
    """
    make_a_copy: make_a_copy_cls = make_a_copy_cls
    """
    make_a_copy command of pb_qbmm.
    """
    child_object_type: fixes_child = fixes_child
    """
    child_object_type of pb_qbmm.
    """
