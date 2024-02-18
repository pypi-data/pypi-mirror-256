#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .energy_source_active_1 import energy_source_active as energy_source_active_cls
from .tab_elec_current_1 import tab_elec_current as tab_elec_current_cls
class fmu_model_settings(Group):
    """
    'fmu_model_settings' child.
    """

    fluent_name = "fmu-model-settings"

    child_names = \
        ['energy_source_active', 'tab_elec_current']

    energy_source_active: energy_source_active_cls = energy_source_active_cls
    """
    energy_source_active child of fmu_model_settings.
    """
    tab_elec_current: tab_elec_current_cls = tab_elec_current_cls
    """
    tab_elec_current child of fmu_model_settings.
    """
