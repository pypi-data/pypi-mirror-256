#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .filename_2 import filename as filename_cls
from .capacity import capacity as capacity_cls
from .circuit_model import circuit_model as circuit_model_cls
from .fitting_method import fitting_method as fitting_method_cls
from .rs_fix import rs_fix as rs_fix_cls
from .capacity_fade_enabled import capacity_fade_enabled as capacity_fade_enabled_cls
from .read_discharge_file_enabled import read_discharge_file_enabled as read_discharge_file_enabled_cls
from .number_discharge_file import number_discharge_file as number_discharge_file_cls
from .discharge_filename import discharge_filename as discharge_filename_cls
class ecm_curve_fitting(Command):
    """
    ECM parameter estimation tool.
    
    Parameters
    ----------
        filename : typing.List[str]
            'filename' child.
        capacity : real
            'capacity' child.
        circuit_model : str
            'circuit_model' child.
        fitting_method : str
            'fitting_method' child.
        rs_fix : typing.List[real]
            'rs_fix' child.
        capacity_fade_enabled : bool
            'capacity_fade_enabled' child.
        read_discharge_file_enabled : bool
            'read_discharge_file_enabled' child.
        number_discharge_file : int
            'number_discharge_file' child.
        discharge_filename : typing.List[str]
            'discharge_filename' child.
    
    """

    fluent_name = "ecm-curve-fitting"

    argument_names = \
        ['filename', 'capacity', 'circuit_model', 'fitting_method', 'rs_fix',
         'capacity_fade_enabled', 'read_discharge_file_enabled',
         'number_discharge_file', 'discharge_filename']

    filename: filename_cls = filename_cls
    """
    filename argument of ecm_curve_fitting.
    """
    capacity: capacity_cls = capacity_cls
    """
    capacity argument of ecm_curve_fitting.
    """
    circuit_model: circuit_model_cls = circuit_model_cls
    """
    circuit_model argument of ecm_curve_fitting.
    """
    fitting_method: fitting_method_cls = fitting_method_cls
    """
    fitting_method argument of ecm_curve_fitting.
    """
    rs_fix: rs_fix_cls = rs_fix_cls
    """
    rs_fix argument of ecm_curve_fitting.
    """
    capacity_fade_enabled: capacity_fade_enabled_cls = capacity_fade_enabled_cls
    """
    capacity_fade_enabled argument of ecm_curve_fitting.
    """
    read_discharge_file_enabled: read_discharge_file_enabled_cls = read_discharge_file_enabled_cls
    """
    read_discharge_file_enabled argument of ecm_curve_fitting.
    """
    number_discharge_file: number_discharge_file_cls = number_discharge_file_cls
    """
    number_discharge_file argument of ecm_curve_fitting.
    """
    discharge_filename: discharge_filename_cls = discharge_filename_cls
    """
    discharge_filename argument of ecm_curve_fitting.
    """
