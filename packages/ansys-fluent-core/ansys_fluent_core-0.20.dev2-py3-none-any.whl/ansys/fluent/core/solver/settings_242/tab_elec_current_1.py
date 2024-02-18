#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .data_type_2 import data_type as data_type_cls
from .value_1 import value as value_cls
from .profile_1 import profile as profile_cls
class tab_elec_current(Group):
    """
    'tab_elec_current' child.
    """

    fluent_name = "tab-elec-current"

    child_names = \
        ['data_type', 'value', 'profile']

    data_type: data_type_cls = data_type_cls
    """
    data_type child of tab_elec_current.
    """
    value: value_cls = value_cls
    """
    value child of tab_elec_current.
    """
    profile: profile_cls = profile_cls
    """
    profile child of tab_elec_current.
    """
