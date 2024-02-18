#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .value import value as value_cls
from .profile_name import profile_name as profile_name_cls
from .field_name import field_name as field_name_cls
from .udf import udf as udf_cls
class prob_mode_1(Group):
    """
    'prob_mode_1' child.
    """

    fluent_name = "prob-mode-1"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option_cls = option_cls
    """
    option child of prob_mode_1.
    """
    value: value_cls = value_cls
    """
    value child of prob_mode_1.
    """
    profile_name: profile_name_cls = profile_name_cls
    """
    profile_name child of prob_mode_1.
    """
    field_name: field_name_cls = field_name_cls
    """
    field_name child of prob_mode_1.
    """
    udf: udf_cls = udf_cls
    """
    udf child of prob_mode_1.
    """
