#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .coefficient_3 import coefficient as coefficient_cls
from .observable import observable as observable_cls
from .power import power as power_cls
class entries_child(Group):
    """
    'child_object_type' of entries.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['coefficient', 'observable', 'power']

    coefficient: coefficient_cls = coefficient_cls
    """
    coefficient child of entries_child.
    """
    observable: observable_cls = observable_cls
    """
    observable child of entries_child.
    """
    power: power_cls = power_cls
    """
    power child of entries_child.
    """
