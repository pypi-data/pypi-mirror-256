#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .initial_time_steps import initial_time_steps as initial_time_steps_cls
from .initial_outer_iter import initial_outer_iter as initial_outer_iter_cls
class initial_outer_iterations(Group):
    """
    Set hybrid nita start-up controls.
    """

    fluent_name = "initial-outer-iterations"

    child_names = \
        ['initial_time_steps', 'initial_outer_iter']

    initial_time_steps: initial_time_steps_cls = initial_time_steps_cls
    """
    initial_time_steps child of initial_outer_iterations.
    """
    initial_outer_iter: initial_outer_iter_cls = initial_outer_iter_cls
    """
    initial_outer_iter child of initial_outer_iterations.
    """
