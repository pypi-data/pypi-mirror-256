#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .two_stage_runge_kutta import two_stage_runge_kutta as two_stage_runge_kutta_cls
from .default_multi_stage_runge_kutta import default_multi_stage_runge_kutta as default_multi_stage_runge_kutta_cls
class rk2(Group):
    """
    'rk2' child.
    """

    fluent_name = "rk2"

    child_names = \
        ['two_stage_runge_kutta', 'default_multi_stage_runge_kutta']

    two_stage_runge_kutta: two_stage_runge_kutta_cls = two_stage_runge_kutta_cls
    """
    two_stage_runge_kutta child of rk2.
    """
    default_multi_stage_runge_kutta: default_multi_stage_runge_kutta_cls = default_multi_stage_runge_kutta_cls
    """
    default_multi_stage_runge_kutta child of rk2.
    """
