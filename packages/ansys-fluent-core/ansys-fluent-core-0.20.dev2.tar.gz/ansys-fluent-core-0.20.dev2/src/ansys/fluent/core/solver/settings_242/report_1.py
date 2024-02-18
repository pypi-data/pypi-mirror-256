#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .electrolyte_area import electrolyte_area as electrolyte_area_cls
from .monitor_enable import monitor_enable as monitor_enable_cls
from .monitor_frequency import monitor_frequency as monitor_frequency_cls
class report(Group):
    """
    Report settings.
    """

    fluent_name = "report"

    child_names = \
        ['electrolyte_area', 'monitor_enable', 'monitor_frequency']

    electrolyte_area: electrolyte_area_cls = electrolyte_area_cls
    """
    electrolyte_area child of report.
    """
    monitor_enable: monitor_enable_cls = monitor_enable_cls
    """
    monitor_enable child of report.
    """
    monitor_frequency: monitor_frequency_cls = monitor_frequency_cls
    """
    monitor_frequency child of report.
    """
