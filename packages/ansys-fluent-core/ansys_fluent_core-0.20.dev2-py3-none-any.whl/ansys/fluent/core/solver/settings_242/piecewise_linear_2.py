#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .function_of import function_of as function_of_cls
from .data_points import data_points as data_points_cls
class piecewise_linear(Group):
    """
    Specify ranges and values for piecewise-linear property.
    """

    fluent_name = "piecewise-linear"

    child_names = \
        ['function_of', 'data_points']

    function_of: function_of_cls = function_of_cls
    """
    function_of child of piecewise_linear.
    """
    data_points: data_points_cls = data_points_cls
    """
    data_points child of piecewise_linear.
    """
