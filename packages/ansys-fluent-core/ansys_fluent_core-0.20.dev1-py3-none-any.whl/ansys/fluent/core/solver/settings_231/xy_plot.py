#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .display_1 import display as display_cls
from .copy_3 import copy as copy_cls
from .add_to_graphics import add_to_graphics as add_to_graphics_cls
from .clear_history import clear_history as clear_history_cls
from .xy_plot_child import xy_plot_child

class xy_plot(NamedObject[xy_plot_child], _CreatableNamedObjectMixin[xy_plot_child]):
    """
    'xy_plot' child.
    """

    fluent_name = "xy-plot"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

    display: display_cls = display_cls
    """
    display command of xy_plot.
    """
    copy: copy_cls = copy_cls
    """
    copy command of xy_plot.
    """
    add_to_graphics: add_to_graphics_cls = add_to_graphics_cls
    """
    add_to_graphics command of xy_plot.
    """
    clear_history: clear_history_cls = clear_history_cls
    """
    clear_history command of xy_plot.
    """
    child_object_type: xy_plot_child = xy_plot_child
    """
    child_object_type of xy_plot.
    """
