#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .histogram_1 import histogram as histogram_cls
from .sample_trajectories import sample_trajectories as sample_trajectories_cls
from .zone_types_to_calc_exchange_data_on import zone_types_to_calc_exchange_data_on as zone_types_to_calc_exchange_data_on_cls
from .exch_details_in_dpm_summ_rep_enabled import exch_details_in_dpm_summ_rep_enabled as exch_details_in_dpm_summ_rep_enabled_cls
from .summary import summary as summary_cls
from .extended_summary import extended_summary as extended_summary_cls
from .zone_summaries_per_injection import zone_summaries_per_injection as zone_summaries_per_injection_cls
class discrete_phase(Group):
    """
    'discrete_phase' child.
    """

    fluent_name = "discrete-phase"

    child_names = \
        ['histogram', 'sample_trajectories',
         'zone_types_to_calc_exchange_data_on',
         'exch_details_in_dpm_summ_rep_enabled']

    histogram: histogram_cls = histogram_cls
    """
    histogram child of discrete_phase.
    """
    sample_trajectories: sample_trajectories_cls = sample_trajectories_cls
    """
    sample_trajectories child of discrete_phase.
    """
    zone_types_to_calc_exchange_data_on: zone_types_to_calc_exchange_data_on_cls = zone_types_to_calc_exchange_data_on_cls
    """
    zone_types_to_calc_exchange_data_on child of discrete_phase.
    """
    exch_details_in_dpm_summ_rep_enabled: exch_details_in_dpm_summ_rep_enabled_cls = exch_details_in_dpm_summ_rep_enabled_cls
    """
    exch_details_in_dpm_summ_rep_enabled child of discrete_phase.
    """
    command_names = \
        ['summary', 'extended_summary', 'zone_summaries_per_injection']

    summary: summary_cls = summary_cls
    """
    summary command of discrete_phase.
    """
    extended_summary: extended_summary_cls = extended_summary_cls
    """
    extended_summary command of discrete_phase.
    """
    zone_summaries_per_injection: zone_summaries_per_injection_cls = zone_summaries_per_injection_cls
    """
    zone_summaries_per_injection command of discrete_phase.
    """
