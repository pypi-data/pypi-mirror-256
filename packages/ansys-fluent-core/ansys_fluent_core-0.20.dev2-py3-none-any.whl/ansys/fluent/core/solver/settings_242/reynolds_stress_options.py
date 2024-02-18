#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .solve_tke import solve_tke as solve_tke_cls
from .wall_echo import wall_echo as wall_echo_cls
class reynolds_stress_options(Group):
    """
    'reynolds_stress_options' child.
    """

    fluent_name = "reynolds-stress-options"

    child_names = \
        ['solve_tke', 'wall_echo']

    solve_tke: solve_tke_cls = solve_tke_cls
    """
    solve_tke child of reynolds_stress_options.
    """
    wall_echo: wall_echo_cls = wall_echo_cls
    """
    wall_echo child of reynolds_stress_options.
    """
