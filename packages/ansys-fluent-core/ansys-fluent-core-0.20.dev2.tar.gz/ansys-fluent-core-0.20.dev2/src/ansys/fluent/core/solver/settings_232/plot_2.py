#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .xy_plot import xy_plot as xy_plot_cls
class plot(Group):
    """
    'plot' child.
    """

    fluent_name = "plot"

    child_names = \
        ['xy_plot']

    xy_plot: xy_plot_cls = xy_plot_cls
    """
    xy_plot child of plot.
    """
