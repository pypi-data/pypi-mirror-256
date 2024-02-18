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

class diffuse_irradiation(NamedObject[fixes_child], _NonCreatableNamedObjectMixin[fixes_child]):
    """
    Diffuse Irradiation.
    """

    fluent_name = "diffuse-irradiation"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    delete: delete_cls = delete_cls
    """
    delete command of diffuse_irradiation.
    """
    rename: rename_cls = rename_cls
    """
    rename command of diffuse_irradiation.
    """
    list: list_cls = list_cls
    """
    list command of diffuse_irradiation.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of diffuse_irradiation.
    """
    make_a_copy: make_a_copy_cls = make_a_copy_cls
    """
    make_a_copy command of diffuse_irradiation.
    """
    child_object_type: fixes_child = fixes_child
    """
    child_object_type of diffuse_irradiation.
    """
