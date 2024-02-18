#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .print_5 import print as print_cls
from .plot_12 import plot as plot_cls
from .n_display_1 import n_display as n_display_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['print', 'plot', 'n_display']

    print: print_cls = print_cls
    """
    print child of options.
    """
    plot: plot_cls = plot_cls
    """
    plot child of options.
    """
    n_display: n_display_cls = n_display_cls
    """
    n_display child of options.
    """
