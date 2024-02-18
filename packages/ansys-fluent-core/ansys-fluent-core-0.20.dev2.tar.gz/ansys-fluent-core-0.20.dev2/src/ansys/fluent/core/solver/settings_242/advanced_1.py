#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .contact_resis import contact_resis as contact_resis_cls
from .coolant_channel import coolant_channel as coolant_channel_cls
from .stack_management import stack_management as stack_management_cls
class advanced(Group):
    """
    Advanced settings.
    """

    fluent_name = "advanced"

    child_names = \
        ['contact_resis', 'coolant_channel', 'stack_management']

    contact_resis: contact_resis_cls = contact_resis_cls
    """
    contact_resis child of advanced.
    """
    coolant_channel: coolant_channel_cls = coolant_channel_cls
    """
    coolant_channel child of advanced.
    """
    stack_management: stack_management_cls = stack_management_cls
    """
    stack_management child of advanced.
    """
