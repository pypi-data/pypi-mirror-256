#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .constant import constant as constant_cls
from .profile_name import profile_name as profile_name_cls
from .field_name import field_name as field_name_cls
from .udf import udf as udf_cls
class heat_transfer_coeff(Group):
    """
    'heat_transfer_coeff' child.
    """

    fluent_name = "heat-transfer-coeff"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option_cls = option_cls
    """
    option child of heat_transfer_coeff.
    """
    constant: constant_cls = constant_cls
    """
    constant child of heat_transfer_coeff.
    """
    profile_name: profile_name_cls = profile_name_cls
    """
    profile_name child of heat_transfer_coeff.
    """
    field_name: field_name_cls = field_name_cls
    """
    field_name child of heat_transfer_coeff.
    """
    udf: udf_cls = udf_cls
    """
    udf child of heat_transfer_coeff.
    """
