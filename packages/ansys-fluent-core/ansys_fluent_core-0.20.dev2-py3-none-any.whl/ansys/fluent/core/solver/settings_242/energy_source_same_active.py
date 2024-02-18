#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .data_type_1 import data_type as data_type_cls
from .value_1 import value as value_cls
from .profile_1 import profile as profile_cls
class energy_source_same_active(Group):
    """
    'energy_source_same_active' child.
    """

    fluent_name = "energy-source-same-active"

    child_names = \
        ['data_type', 'value', 'profile']

    data_type: data_type_cls = data_type_cls
    """
    data_type child of energy_source_same_active.
    """
    value: value_cls = value_cls
    """
    value child of energy_source_same_active.
    """
    profile: profile_cls = profile_cls
    """
    profile child of energy_source_same_active.
    """
