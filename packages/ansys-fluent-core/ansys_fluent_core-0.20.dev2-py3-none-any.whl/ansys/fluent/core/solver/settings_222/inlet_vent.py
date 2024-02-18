#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .change_type import change_type as change_type_cls
from .inlet_vent_child import inlet_vent_child

class inlet_vent(NamedObject[inlet_vent_child], _CreatableNamedObjectMixin[inlet_vent_child]):
    """
    'inlet_vent' child.
    """

    fluent_name = "inlet-vent"

    command_names = \
        ['change_type']

    change_type: change_type_cls = change_type_cls
    """
    change_type command of inlet_vent.
    """
    child_object_type: inlet_vent_child = inlet_vent_child
    """
    child_object_type of inlet_vent.
    """
