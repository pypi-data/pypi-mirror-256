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
from .number_dod_level import number_dod_level as number_dod_level_cls
from .min_dod import min_dod as min_dod_cls
from .max_dod import max_dod as max_dod_cls
from .capacity_fade_enabled import capacity_fade_enabled as capacity_fade_enabled_cls
class ntgk_curve_fitting(Command):
    """
    NTGK parameter estimation tool.
    
    Parameters
    ----------
        filename : typing.List[str]
            'filename' child.
        capacity : real
            'capacity' child.
        number_dod_level : int
            'number_dod_level' child.
        min_dod : real
            'min_dod' child.
        max_dod : real
            'max_dod' child.
        capacity_fade_enabled : bool
            'capacity_fade_enabled' child.
    
    """

    fluent_name = "ntgk-curve-fitting"

    argument_names = \
        ['filename', 'capacity', 'number_dod_level', 'min_dod', 'max_dod',
         'capacity_fade_enabled']

    filename: filename_cls = filename_cls
    """
    filename argument of ntgk_curve_fitting.
    """
    capacity: capacity_cls = capacity_cls
    """
    capacity argument of ntgk_curve_fitting.
    """
    number_dod_level: number_dod_level_cls = number_dod_level_cls
    """
    number_dod_level argument of ntgk_curve_fitting.
    """
    min_dod: min_dod_cls = min_dod_cls
    """
    min_dod argument of ntgk_curve_fitting.
    """
    max_dod: max_dod_cls = max_dod_cls
    """
    max_dod argument of ntgk_curve_fitting.
    """
    capacity_fade_enabled: capacity_fade_enabled_cls = capacity_fade_enabled_cls
    """
    capacity_fade_enabled argument of ntgk_curve_fitting.
    """
