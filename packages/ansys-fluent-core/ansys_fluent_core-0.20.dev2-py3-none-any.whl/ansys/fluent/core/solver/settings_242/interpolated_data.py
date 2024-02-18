#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .zone_1 import zone as zone_cls
from .y_axis_function_1 import y_axis_function as y_axis_function_cls
from .x_axis_function_1 import x_axis_function as x_axis_function_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .plot_10 import plot as plot_cls
class interpolated_data(Group):
    """
    Display interpolated data.
    """

    fluent_name = "interpolated-data"

    child_names = \
        ['zone', 'y_axis_function', 'x_axis_function', 'axes', 'curves']

    zone: zone_cls = zone_cls
    """
    zone child of interpolated_data.
    """
    y_axis_function: y_axis_function_cls = y_axis_function_cls
    """
    y_axis_function child of interpolated_data.
    """
    x_axis_function: x_axis_function_cls = x_axis_function_cls
    """
    x_axis_function child of interpolated_data.
    """
    axes: axes_cls = axes_cls
    """
    axes child of interpolated_data.
    """
    curves: curves_cls = curves_cls
    """
    curves child of interpolated_data.
    """
    command_names = \
        ['plot']

    plot: plot_cls = plot_cls
    """
    plot command of interpolated_data.
    """
