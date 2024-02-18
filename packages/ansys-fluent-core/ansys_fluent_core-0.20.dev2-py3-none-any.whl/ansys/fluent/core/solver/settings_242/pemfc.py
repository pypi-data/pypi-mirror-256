#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_19 import enabled as enabled_cls
from .options_5 import options as options_cls
from .parameters_1 import parameters as parameters_cls
from .anode_1 import anode as anode_cls
from .membrane import membrane as membrane_cls
from .cathode_1 import cathode as cathode_cls
from .electrical_tab import electrical_tab as electrical_tab_cls
from .advanced_1 import advanced as advanced_cls
from .report_1 import report as report_cls
class pemfc(Group):
    """
    Enter PEMFC model settings.
    """

    fluent_name = "pemfc"

    child_names = \
        ['enabled', 'options', 'parameters', 'anode', 'membrane', 'cathode',
         'electrical_tab', 'advanced', 'report']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of pemfc.
    """
    options: options_cls = options_cls
    """
    options child of pemfc.
    """
    parameters: parameters_cls = parameters_cls
    """
    parameters child of pemfc.
    """
    anode: anode_cls = anode_cls
    """
    anode child of pemfc.
    """
    membrane: membrane_cls = membrane_cls
    """
    membrane child of pemfc.
    """
    cathode: cathode_cls = cathode_cls
    """
    cathode child of pemfc.
    """
    electrical_tab: electrical_tab_cls = electrical_tab_cls
    """
    electrical_tab child of pemfc.
    """
    advanced: advanced_cls = advanced_cls
    """
    advanced child of pemfc.
    """
    report: report_cls = report_cls
    """
    report child of pemfc.
    """
