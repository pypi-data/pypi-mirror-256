#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .type_1 import type as type_cls
from .method import method as method_cls
from .specified_time_step import specified_time_step as specified_time_step_cls
from .incremental_time import incremental_time as incremental_time_cls
from .max_iterations_per_time_step import max_iterations_per_time_step as max_iterations_per_time_step_cls
from .number_of_time_steps import number_of_time_steps as number_of_time_steps_cls
from .total_number_of_time_steps import total_number_of_time_steps as total_number_of_time_steps_cls
from .total_time import total_time as total_time_cls
from .time_step_size import time_step_size as time_step_size_cls
from .solution_status import solution_status as solution_status_cls
from .extrapolate_vars import extrapolate_vars as extrapolate_vars_cls
from .max_flow_time import max_flow_time as max_flow_time_cls
from .control_time_step_size_variation import control_time_step_size_variation as control_time_step_size_variation_cls
from .use_average_cfl import use_average_cfl as use_average_cfl_cls
from .cfl_type import cfl_type as cfl_type_cls
from .cfl_based_time_stepping import cfl_based_time_stepping as cfl_based_time_stepping_cls
from .error_based_time_stepping import error_based_time_stepping as error_based_time_stepping_cls
from .undo_timestep import undo_timestep as undo_timestep_cls
from .predict_next import predict_next as predict_next_cls
from .rotating_mesh_flow_predictor import rotating_mesh_flow_predictor as rotating_mesh_flow_predictor_cls
from .mp_specific_time_stepping import mp_specific_time_stepping as mp_specific_time_stepping_cls
from .udf_hook import udf_hook as udf_hook_cls
class transient_controls(Group):
    """
    'transient_controls' child.
    """

    fluent_name = "transient-controls"

    child_names = \
        ['type', 'method', 'specified_time_step', 'incremental_time',
         'max_iterations_per_time_step', 'number_of_time_steps',
         'total_number_of_time_steps', 'total_time', 'time_step_size',
         'solution_status', 'extrapolate_vars', 'max_flow_time',
         'control_time_step_size_variation', 'use_average_cfl', 'cfl_type',
         'cfl_based_time_stepping', 'error_based_time_stepping',
         'undo_timestep', 'predict_next', 'rotating_mesh_flow_predictor',
         'mp_specific_time_stepping', 'udf_hook']

    type: type_cls = type_cls
    """
    type child of transient_controls.
    """
    method: method_cls = method_cls
    """
    method child of transient_controls.
    """
    specified_time_step: specified_time_step_cls = specified_time_step_cls
    """
    specified_time_step child of transient_controls.
    """
    incremental_time: incremental_time_cls = incremental_time_cls
    """
    incremental_time child of transient_controls.
    """
    max_iterations_per_time_step: max_iterations_per_time_step_cls = max_iterations_per_time_step_cls
    """
    max_iterations_per_time_step child of transient_controls.
    """
    number_of_time_steps: number_of_time_steps_cls = number_of_time_steps_cls
    """
    number_of_time_steps child of transient_controls.
    """
    total_number_of_time_steps: total_number_of_time_steps_cls = total_number_of_time_steps_cls
    """
    total_number_of_time_steps child of transient_controls.
    """
    total_time: total_time_cls = total_time_cls
    """
    total_time child of transient_controls.
    """
    time_step_size: time_step_size_cls = time_step_size_cls
    """
    time_step_size child of transient_controls.
    """
    solution_status: solution_status_cls = solution_status_cls
    """
    solution_status child of transient_controls.
    """
    extrapolate_vars: extrapolate_vars_cls = extrapolate_vars_cls
    """
    extrapolate_vars child of transient_controls.
    """
    max_flow_time: max_flow_time_cls = max_flow_time_cls
    """
    max_flow_time child of transient_controls.
    """
    control_time_step_size_variation: control_time_step_size_variation_cls = control_time_step_size_variation_cls
    """
    control_time_step_size_variation child of transient_controls.
    """
    use_average_cfl: use_average_cfl_cls = use_average_cfl_cls
    """
    use_average_cfl child of transient_controls.
    """
    cfl_type: cfl_type_cls = cfl_type_cls
    """
    cfl_type child of transient_controls.
    """
    cfl_based_time_stepping: cfl_based_time_stepping_cls = cfl_based_time_stepping_cls
    """
    cfl_based_time_stepping child of transient_controls.
    """
    error_based_time_stepping: error_based_time_stepping_cls = error_based_time_stepping_cls
    """
    error_based_time_stepping child of transient_controls.
    """
    undo_timestep: undo_timestep_cls = undo_timestep_cls
    """
    undo_timestep child of transient_controls.
    """
    predict_next: predict_next_cls = predict_next_cls
    """
    predict_next child of transient_controls.
    """
    rotating_mesh_flow_predictor: rotating_mesh_flow_predictor_cls = rotating_mesh_flow_predictor_cls
    """
    rotating_mesh_flow_predictor child of transient_controls.
    """
    mp_specific_time_stepping: mp_specific_time_stepping_cls = mp_specific_time_stepping_cls
    """
    mp_specific_time_stepping child of transient_controls.
    """
    udf_hook: udf_hook_cls = udf_hook_cls
    """
    udf_hook child of transient_controls.
    """
