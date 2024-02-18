#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .mass_flow_inlet_child import mass_flow_inlet_child

class mass_flow_outlet(NamedObject[mass_flow_inlet_child], _NonCreatableNamedObjectMixin[mass_flow_inlet_child]):
    """
    'mass_flow_outlet' child.
    """

    fluent_name = "mass-flow-outlet"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of mass_flow_outlet.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of mass_flow_outlet.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of mass_flow_outlet.
    """
    child_object_type: mass_flow_inlet_child = mass_flow_inlet_child
    """
    child_object_type of mass_flow_outlet.
    """
