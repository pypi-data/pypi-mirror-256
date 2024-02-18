#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .data_reduction import data_reduction as data_reduction_cls
class parcel_count_control(Group):
    """
    'parcel_count_control' child.
    """

    fluent_name = "parcel-count-control"

    child_names = \
        ['data_reduction']

    data_reduction: data_reduction_cls = data_reduction_cls
    """
    data_reduction child of parcel_count_control.
    """
