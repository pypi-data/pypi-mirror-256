#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .value_1 import value as value_cls
from .profile_name import profile_name as profile_name_cls
from .field_name import field_name as field_name_cls
from .udf import udf as udf_cls
class wave_ht(Group):
    """
    'wave_ht' child.
    """

    fluent_name = "wave-ht"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option_cls = option_cls
    """
    option child of wave_ht.
    """
    value: value_cls = value_cls
    """
    value child of wave_ht.
    """
    profile_name: profile_name_cls = profile_name_cls
    """
    profile_name child of wave_ht.
    """
    field_name: field_name_cls = field_name_cls
    """
    field_name child of wave_ht.
    """
    udf: udf_cls = udf_cls
    """
    udf child of wave_ht.
    """
