#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .multi_phase_setting import multi_phase_setting as multi_phase_setting_cls
from .single_phase_setting import single_phase_setting as single_phase_setting_cls
class hybrid_nita_settings(Group):
    """
    Select a hybrid NITA settings option for faster performance and better robustness.
    """

    fluent_name = "hybrid-nita-settings"

    child_names = \
        ['multi_phase_setting', 'single_phase_setting']

    multi_phase_setting: multi_phase_setting_cls = multi_phase_setting_cls
    """
    multi_phase_setting child of hybrid_nita_settings.
    """
    single_phase_setting: single_phase_setting_cls = single_phase_setting_cls
    """
    single_phase_setting child of hybrid_nita_settings.
    """
