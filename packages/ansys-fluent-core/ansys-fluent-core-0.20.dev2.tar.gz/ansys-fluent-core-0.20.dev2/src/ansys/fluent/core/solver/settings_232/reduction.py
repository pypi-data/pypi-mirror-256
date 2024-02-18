#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .setup_reduction import setup_reduction as setup_reduction_cls
from .pick_sample_to_reduce import pick_sample_to_reduce as pick_sample_to_reduce_cls
from .reduce_picked_sample import reduce_picked_sample as reduce_picked_sample_cls
class reduction(Group):
    """
    'reduction' child.
    """

    fluent_name = "reduction"

    child_names = \
        ['setup_reduction']

    setup_reduction: setup_reduction_cls = setup_reduction_cls
    """
    setup_reduction child of reduction.
    """
    command_names = \
        ['pick_sample_to_reduce', 'reduce_picked_sample']

    pick_sample_to_reduce: pick_sample_to_reduce_cls = pick_sample_to_reduce_cls
    """
    pick_sample_to_reduce command of reduction.
    """
    reduce_picked_sample: reduce_picked_sample_cls = reduce_picked_sample_cls
    """
    reduce_picked_sample command of reduction.
    """
