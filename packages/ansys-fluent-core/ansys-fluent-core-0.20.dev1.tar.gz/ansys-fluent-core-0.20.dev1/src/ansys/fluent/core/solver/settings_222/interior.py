#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .change_type import change_type as change_type_cls
from .interior_child import interior_child

class interior(NamedObject[interior_child], _CreatableNamedObjectMixin[interior_child]):
    """
    'interior' child.
    """

    fluent_name = "interior"

    command_names = \
        ['change_type']

    change_type: change_type_cls = change_type_cls
    """
    change_type command of interior.
    """
    child_object_type: interior_child = interior_child
    """
    child_object_type of interior.
    """
