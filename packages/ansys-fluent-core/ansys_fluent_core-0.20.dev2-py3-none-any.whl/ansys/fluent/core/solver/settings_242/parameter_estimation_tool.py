#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .echem_model_1 import echem_model as echem_model_cls
from .thermal_abuse_fitting import thermal_abuse_fitting as thermal_abuse_fitting_cls
from .ntgk_curve_fitting import ntgk_curve_fitting as ntgk_curve_fitting_cls
from .ecm_curve_fitting import ecm_curve_fitting as ecm_curve_fitting_cls
class parameter_estimation_tool(Group):
    """
    Parameter estimation tool.
    """

    fluent_name = "parameter-estimation-tool"

    child_names = \
        ['echem_model', 'thermal_abuse_fitting']

    echem_model: echem_model_cls = echem_model_cls
    """
    echem_model child of parameter_estimation_tool.
    """
    thermal_abuse_fitting: thermal_abuse_fitting_cls = thermal_abuse_fitting_cls
    """
    thermal_abuse_fitting child of parameter_estimation_tool.
    """
    command_names = \
        ['ntgk_curve_fitting', 'ecm_curve_fitting']

    ntgk_curve_fitting: ntgk_curve_fitting_cls = ntgk_curve_fitting_cls
    """
    ntgk_curve_fitting command of parameter_estimation_tool.
    """
    ecm_curve_fitting: ecm_curve_fitting_cls = ecm_curve_fitting_cls
    """
    ecm_curve_fitting command of parameter_estimation_tool.
    """
