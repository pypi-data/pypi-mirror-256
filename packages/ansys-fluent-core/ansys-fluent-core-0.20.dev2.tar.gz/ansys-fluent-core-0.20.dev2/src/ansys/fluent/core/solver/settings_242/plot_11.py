#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .xy_plot import xy_plot as xy_plot_cls
from .histogram import histogram as histogram_cls
from .cumulative_plot import cumulative_plot as cumulative_plot_cls
from .solution_plot import solution_plot as solution_plot_cls
from .profile_data import profile_data as profile_data_cls
from .interpolated_data import interpolated_data as interpolated_data_cls
class plot(Group):
    """
    'plot' child.
    """

    fluent_name = "plot"

    child_names = \
        ['xy_plot', 'histogram', 'cumulative_plot', 'solution_plot',
         'profile_data', 'interpolated_data']

    xy_plot: xy_plot_cls = xy_plot_cls
    """
    xy_plot child of plot.
    """
    histogram: histogram_cls = histogram_cls
    """
    histogram child of plot.
    """
    cumulative_plot: cumulative_plot_cls = cumulative_plot_cls
    """
    cumulative_plot child of plot.
    """
    solution_plot: solution_plot_cls = solution_plot_cls
    """
    solution_plot child of plot.
    """
    profile_data: profile_data_cls = profile_data_cls
    """
    profile_data child of plot.
    """
    interpolated_data: interpolated_data_cls = interpolated_data_cls
    """
    interpolated_data child of plot.
    """
