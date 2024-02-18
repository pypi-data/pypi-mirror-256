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
class per_dispx(Group):
    """
    'per_dispx' child.
    """

    fluent_name = "per-dispx"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option_cls = option_cls
    """
    option child of per_dispx.
    """
    value: value_cls = value_cls
    """
    value child of per_dispx.
    """
    profile_name: profile_name_cls = profile_name_cls
    """
    profile_name child of per_dispx.
    """
    field_name: field_name_cls = field_name_cls
    """
    field_name child of per_dispx.
    """
    udf: udf_cls = udf_cls
    """
    udf child of per_dispx.
    """
