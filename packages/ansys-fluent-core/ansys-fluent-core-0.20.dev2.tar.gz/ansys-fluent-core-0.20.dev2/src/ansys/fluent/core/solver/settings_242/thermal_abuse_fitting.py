#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .test_data_sets import test_data_sets as test_data_sets_cls
from .rhocp import rhocp as rhocp_cls
from .area import area as area_cls
from .vol import vol as vol_cls
from .epsilon import epsilon as epsilon_cls
from .fixm_enabled import fixm_enabled as fixm_enabled_cls
from .mvalue import mvalue as mvalue_cls
from .fixn_enabled import fixn_enabled as fixn_enabled_cls
from .nvalue import nvalue as nvalue_cls
from .filename_1 import filename as filename_cls
from .initial_temp import initial_temp as initial_temp_cls
from .ambient_temp import ambient_temp as ambient_temp_cls
from .external_ht_coeff import external_ht_coeff as external_ht_coeff_cls
from .enclosure_temp import enclosure_temp as enclosure_temp_cls
from .abuse_curve_fitting import abuse_curve_fitting as abuse_curve_fitting_cls
from .fine_tune_parameter import fine_tune_parameter as fine_tune_parameter_cls
from .use_fine_tune_parameter import use_fine_tune_parameter as use_fine_tune_parameter_cls
class thermal_abuse_fitting(Group):
    """
    Thermal abuse parameter estimation menu.
    """

    fluent_name = "thermal-abuse-fitting"

    child_names = \
        ['test_data_sets', 'rhocp', 'area', 'vol', 'epsilon', 'fixm_enabled',
         'mvalue', 'fixn_enabled', 'nvalue', 'filename', 'initial_temp',
         'ambient_temp', 'external_ht_coeff', 'enclosure_temp']

    test_data_sets: test_data_sets_cls = test_data_sets_cls
    """
    test_data_sets child of thermal_abuse_fitting.
    """
    rhocp: rhocp_cls = rhocp_cls
    """
    rhocp child of thermal_abuse_fitting.
    """
    area: area_cls = area_cls
    """
    area child of thermal_abuse_fitting.
    """
    vol: vol_cls = vol_cls
    """
    vol child of thermal_abuse_fitting.
    """
    epsilon: epsilon_cls = epsilon_cls
    """
    epsilon child of thermal_abuse_fitting.
    """
    fixm_enabled: fixm_enabled_cls = fixm_enabled_cls
    """
    fixm_enabled child of thermal_abuse_fitting.
    """
    mvalue: mvalue_cls = mvalue_cls
    """
    mvalue child of thermal_abuse_fitting.
    """
    fixn_enabled: fixn_enabled_cls = fixn_enabled_cls
    """
    fixn_enabled child of thermal_abuse_fitting.
    """
    nvalue: nvalue_cls = nvalue_cls
    """
    nvalue child of thermal_abuse_fitting.
    """
    filename: filename_cls = filename_cls
    """
    filename child of thermal_abuse_fitting.
    """
    initial_temp: initial_temp_cls = initial_temp_cls
    """
    initial_temp child of thermal_abuse_fitting.
    """
    ambient_temp: ambient_temp_cls = ambient_temp_cls
    """
    ambient_temp child of thermal_abuse_fitting.
    """
    external_ht_coeff: external_ht_coeff_cls = external_ht_coeff_cls
    """
    external_ht_coeff child of thermal_abuse_fitting.
    """
    enclosure_temp: enclosure_temp_cls = enclosure_temp_cls
    """
    enclosure_temp child of thermal_abuse_fitting.
    """
    command_names = \
        ['abuse_curve_fitting', 'fine_tune_parameter',
         'use_fine_tune_parameter']

    abuse_curve_fitting: abuse_curve_fitting_cls = abuse_curve_fitting_cls
    """
    abuse_curve_fitting command of thermal_abuse_fitting.
    """
    fine_tune_parameter: fine_tune_parameter_cls = fine_tune_parameter_cls
    """
    fine_tune_parameter command of thermal_abuse_fitting.
    """
    use_fine_tune_parameter: use_fine_tune_parameter_cls = use_fine_tune_parameter_cls
    """
    use_fine_tune_parameter command of thermal_abuse_fitting.
    """
