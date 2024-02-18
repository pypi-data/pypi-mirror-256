#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .report_name import report_name as report_name_cls
class delete_simulation_report(Command):
    """
    Delete the provided simulation report.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
    
    """

    fluent_name = "delete-simulation-report"

    argument_names = \
        ['report_name']

    report_name: report_name_cls = report_name_cls
    """
    report_name argument of delete_simulation_report.
    """
