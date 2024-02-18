#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_fc_units import list_fc_units as list_fc_units_cls
from .stack_create_fcu import stack_create_fcu as stack_create_fcu_cls
from .stack_modify_fcu import stack_modify_fcu as stack_modify_fcu_cls
from .stack_delete_fcu import stack_delete_fcu as stack_delete_fcu_cls
from .stack_reset_fcu import stack_reset_fcu as stack_reset_fcu_cls
from .stack_submit_fcu import stack_submit_fcu as stack_submit_fcu_cls
class stack_management(Group):
    """
    Stack management.
    """

    fluent_name = "stack-management"

    command_names = \
        ['list_fc_units', 'stack_create_fcu', 'stack_modify_fcu',
         'stack_delete_fcu', 'stack_reset_fcu', 'stack_submit_fcu']

    list_fc_units: list_fc_units_cls = list_fc_units_cls
    """
    list_fc_units command of stack_management.
    """
    stack_create_fcu: stack_create_fcu_cls = stack_create_fcu_cls
    """
    stack_create_fcu command of stack_management.
    """
    stack_modify_fcu: stack_modify_fcu_cls = stack_modify_fcu_cls
    """
    stack_modify_fcu command of stack_management.
    """
    stack_delete_fcu: stack_delete_fcu_cls = stack_delete_fcu_cls
    """
    stack_delete_fcu command of stack_management.
    """
    stack_reset_fcu: stack_reset_fcu_cls = stack_reset_fcu_cls
    """
    stack_reset_fcu command of stack_management.
    """
    stack_submit_fcu: stack_submit_fcu_cls = stack_submit_fcu_cls
    """
    stack_submit_fcu command of stack_management.
    """
