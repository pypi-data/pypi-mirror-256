#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .field_3 import field as field_cls
from .node_values_3 import node_values as node_values_cls
from .zones_5 import zones as zones_cls
from .surfaces_8 import surfaces as surfaces_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .plot_8 import plot as plot_cls
class solution_plot(Group):
    """
    Plot the solution data.
    """

    fluent_name = "solution-plot"

    child_names = \
        ['field', 'node_values', 'zones', 'surfaces', 'axes', 'curves']

    field: field_cls = field_cls
    """
    field child of solution_plot.
    """
    node_values: node_values_cls = node_values_cls
    """
    node_values child of solution_plot.
    """
    zones: zones_cls = zones_cls
    """
    zones child of solution_plot.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces child of solution_plot.
    """
    axes: axes_cls = axes_cls
    """
    axes child of solution_plot.
    """
    curves: curves_cls = curves_cls
    """
    curves child of solution_plot.
    """
    command_names = \
        ['plot']

    plot: plot_cls = plot_cls
    """
    plot command of solution_plot.
    """
