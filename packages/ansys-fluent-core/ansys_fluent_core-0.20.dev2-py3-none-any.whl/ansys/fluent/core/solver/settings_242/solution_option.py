#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .number_substeps import number_substeps as number_substeps_cls
from .joule_heat_in_passive_zone import joule_heat_in_passive_zone as joule_heat_in_passive_zone_cls
from .joule_heat_in_active_zone import joule_heat_in_active_zone as joule_heat_in_active_zone_cls
from .echem_heat_enabled import echem_heat_enabled as echem_heat_enabled_cls
from .entropic_heat import entropic_heat as entropic_heat_cls
from .current_urf import current_urf as current_urf_cls
from .voltage_correction_urf import voltage_correction_urf as voltage_correction_urf_cls
from .q_correct_enabled import q_correct_enabled as q_correct_enabled_cls
from .heat_correct_table import heat_correct_table as heat_correct_table_cls
class solution_option(Group):
    """
    'solution_option' child.
    """

    fluent_name = "solution-option"

    child_names = \
        ['number_substeps', 'joule_heat_in_passive_zone',
         'joule_heat_in_active_zone', 'echem_heat_enabled', 'entropic_heat',
         'current_urf', 'voltage_correction_urf', 'q_correct_enabled',
         'heat_correct_table']

    number_substeps: number_substeps_cls = number_substeps_cls
    """
    number_substeps child of solution_option.
    """
    joule_heat_in_passive_zone: joule_heat_in_passive_zone_cls = joule_heat_in_passive_zone_cls
    """
    joule_heat_in_passive_zone child of solution_option.
    """
    joule_heat_in_active_zone: joule_heat_in_active_zone_cls = joule_heat_in_active_zone_cls
    """
    joule_heat_in_active_zone child of solution_option.
    """
    echem_heat_enabled: echem_heat_enabled_cls = echem_heat_enabled_cls
    """
    echem_heat_enabled child of solution_option.
    """
    entropic_heat: entropic_heat_cls = entropic_heat_cls
    """
    entropic_heat child of solution_option.
    """
    current_urf: current_urf_cls = current_urf_cls
    """
    current_urf child of solution_option.
    """
    voltage_correction_urf: voltage_correction_urf_cls = voltage_correction_urf_cls
    """
    voltage_correction_urf child of solution_option.
    """
    q_correct_enabled: q_correct_enabled_cls = q_correct_enabled_cls
    """
    q_correct_enabled child of solution_option.
    """
    heat_correct_table: heat_correct_table_cls = heat_correct_table_cls
    """
    heat_correct_table child of solution_option.
    """
