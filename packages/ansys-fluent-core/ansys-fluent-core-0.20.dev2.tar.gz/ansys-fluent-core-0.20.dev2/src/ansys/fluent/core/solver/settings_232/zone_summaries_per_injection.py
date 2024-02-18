#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .summary_state import summary_state as summary_state_cls
from .reset_dpm_summaries import reset_dpm_summaries as reset_dpm_summaries_cls
class zone_summaries_per_injection(Command):
    """
    Enable per-injection zone DPM summaries.
    
    Parameters
    ----------
        summary_state : bool
            'summary_state' child.
        reset_dpm_summaries : bool
            'reset_dpm_summaries' child.
    
    """

    fluent_name = "zone-summaries-per-injection?"

    argument_names = \
        ['summary_state', 'reset_dpm_summaries']

    summary_state: summary_state_cls = summary_state_cls
    """
    summary_state argument of zone_summaries_per_injection.
    """
    reset_dpm_summaries: reset_dpm_summaries_cls = reset_dpm_summaries_cls
    """
    reset_dpm_summaries argument of zone_summaries_per_injection.
    """
