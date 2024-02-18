#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .initial_dod import initial_dod as initial_dod_cls
from .ref_capacity import ref_capacity as ref_capacity_cls
from .data_type import data_type as data_type_cls
from .poly_u_function import poly_u_function as poly_u_function_cls
from .poly_y_function import poly_y_function as poly_y_function_cls
from .poly_t_dependence import poly_t_dependence as poly_t_dependence_cls
from .u_table import u_table as u_table_cls
from .y_table import y_table as y_table_cls
from .internal_resistance_table import internal_resistance_table as internal_resistance_table_cls
from .limit_current_enabled import limit_current_enabled as limit_current_enabled_cls
from .provide_utable_enabled import provide_utable_enabled as provide_utable_enabled_cls
from .limit_current_table import limit_current_table as limit_current_table_cls
from .monitor_names import monitor_names as monitor_names_cls
from .raw_data import raw_data as raw_data_cls
class ntgk_model_settings(Group):
    """
    'ntgk_model_settings' child.
    """

    fluent_name = "ntgk-model-settings"

    child_names = \
        ['initial_dod', 'ref_capacity', 'data_type', 'poly_u_function',
         'poly_y_function', 'poly_t_dependence', 'u_table', 'y_table',
         'internal_resistance_table', 'limit_current_enabled',
         'provide_utable_enabled', 'limit_current_table', 'monitor_names']

    initial_dod: initial_dod_cls = initial_dod_cls
    """
    initial_dod child of ntgk_model_settings.
    """
    ref_capacity: ref_capacity_cls = ref_capacity_cls
    """
    ref_capacity child of ntgk_model_settings.
    """
    data_type: data_type_cls = data_type_cls
    """
    data_type child of ntgk_model_settings.
    """
    poly_u_function: poly_u_function_cls = poly_u_function_cls
    """
    poly_u_function child of ntgk_model_settings.
    """
    poly_y_function: poly_y_function_cls = poly_y_function_cls
    """
    poly_y_function child of ntgk_model_settings.
    """
    poly_t_dependence: poly_t_dependence_cls = poly_t_dependence_cls
    """
    poly_t_dependence child of ntgk_model_settings.
    """
    u_table: u_table_cls = u_table_cls
    """
    u_table child of ntgk_model_settings.
    """
    y_table: y_table_cls = y_table_cls
    """
    y_table child of ntgk_model_settings.
    """
    internal_resistance_table: internal_resistance_table_cls = internal_resistance_table_cls
    """
    internal_resistance_table child of ntgk_model_settings.
    """
    limit_current_enabled: limit_current_enabled_cls = limit_current_enabled_cls
    """
    limit_current_enabled child of ntgk_model_settings.
    """
    provide_utable_enabled: provide_utable_enabled_cls = provide_utable_enabled_cls
    """
    provide_utable_enabled child of ntgk_model_settings.
    """
    limit_current_table: limit_current_table_cls = limit_current_table_cls
    """
    limit_current_table child of ntgk_model_settings.
    """
    monitor_names: monitor_names_cls = monitor_names_cls
    """
    monitor_names child of ntgk_model_settings.
    """
    command_names = \
        ['raw_data']

    raw_data: raw_data_cls = raw_data_cls
    """
    raw_data command of ntgk_model_settings.
    """
