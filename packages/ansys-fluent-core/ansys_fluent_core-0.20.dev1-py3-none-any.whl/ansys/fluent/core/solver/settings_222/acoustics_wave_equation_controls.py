#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .expert import expert as expert_cls
from .relative_convergence_criterion import relative_convergence_criterion as relative_convergence_criterion_cls
from .max_iterations_per_timestep import max_iterations_per_timestep as max_iterations_per_timestep_cls
class acoustics_wave_equation_controls(Group):
    """
    'acoustics_wave_equation_controls' child.
    """

    fluent_name = "acoustics-wave-equation-controls"

    child_names = \
        ['expert', 'relative_convergence_criterion',
         'max_iterations_per_timestep']

    expert: expert_cls = expert_cls
    """
    expert child of acoustics_wave_equation_controls.
    """
    relative_convergence_criterion: relative_convergence_criterion_cls = relative_convergence_criterion_cls
    """
    relative_convergence_criterion child of acoustics_wave_equation_controls.
    """
    max_iterations_per_timestep: max_iterations_per_timestep_cls = max_iterations_per_timestep_cls
    """
    max_iterations_per_timestep child of acoustics_wave_equation_controls.
    """
