#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .non_overlap_zone_name import non_overlap_zone_name as non_overlap_zone_name_cls
class interface(Group):
    """
    Help not available.
    """

    fluent_name = "interface"

    child_names = \
        ['non_overlap_zone_name']

    non_overlap_zone_name: non_overlap_zone_name_cls = non_overlap_zone_name_cls
    """
    non_overlap_zone_name child of interface.
    """
