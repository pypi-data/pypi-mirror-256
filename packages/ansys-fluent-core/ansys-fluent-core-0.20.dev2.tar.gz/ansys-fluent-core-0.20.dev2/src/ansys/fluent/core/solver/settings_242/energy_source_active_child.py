#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .method_2 import method as method_cls
from .value_1 import value as value_cls
from .profile_1 import profile as profile_cls
class energy_source_active_child(Group):
    """
    'child_object_type' of energy_source_active.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['method', 'value', 'profile']

    method: method_cls = method_cls
    """
    method child of energy_source_active_child.
    """
    value: value_cls = value_cls
    """
    value child of energy_source_active_child.
    """
    profile: profile_cls = profile_cls
    """
    profile child of energy_source_active_child.
    """
