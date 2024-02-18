#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .iteration_count import iteration_count as iteration_count_cls
from .initialize_stabilization import initialize_stabilization as initialize_stabilization_cls
from .calculation_activities import calculation_activities as calculation_activities_cls
from .initialize_2 import initialize as initialize_cls
from .calculate_1 import calculate as calculate_cls
class calculation(Group):
    """
    Enter the adjoint calculation menu.
    """

    fluent_name = "calculation"

    child_names = \
        ['iteration_count', 'initialize_stabilization',
         'calculation_activities']

    iteration_count: iteration_count_cls = iteration_count_cls
    """
    iteration_count child of calculation.
    """
    initialize_stabilization: initialize_stabilization_cls = initialize_stabilization_cls
    """
    initialize_stabilization child of calculation.
    """
    calculation_activities: calculation_activities_cls = calculation_activities_cls
    """
    calculation_activities child of calculation.
    """
    command_names = \
        ['initialize', 'calculate']

    initialize: initialize_cls = initialize_cls
    """
    initialize command of calculation.
    """
    calculate: calculate_cls = calculate_cls
    """
    calculate command of calculation.
    """
