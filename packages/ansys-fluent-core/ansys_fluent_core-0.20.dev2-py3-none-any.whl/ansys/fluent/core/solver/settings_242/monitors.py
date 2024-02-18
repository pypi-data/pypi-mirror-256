#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .adjoint_equations import adjoint_equations as adjoint_equations_cls
from .options_17 import options as options_cls
from .plot_1 import plot as plot_cls
class monitors(Group):
    """
    Enter the residual monitors menu.
    """

    fluent_name = "monitors"

    child_names = \
        ['adjoint_equations', 'options']

    adjoint_equations: adjoint_equations_cls = adjoint_equations_cls
    """
    adjoint_equations child of monitors.
    """
    options: options_cls = options_cls
    """
    options child of monitors.
    """
    command_names = \
        ['plot']

    plot: plot_cls = plot_cls
    """
    plot command of monitors.
    """
