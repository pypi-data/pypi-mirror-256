#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
from .value import value as value_cls
from .gray_band_coefficients import gray_band_coefficients as gray_band_coefficients_cls
class refractive_index(Group):
    """
    'refractive_index' child.
    """

    fluent_name = "refractive-index"

    child_names = \
        ['option', 'value', 'gray_band_coefficients']

    option: option_cls = option_cls
    """
    option child of refractive_index.
    """
    value: value_cls = value_cls
    """
    value child of refractive_index.
    """
    gray_band_coefficients: gray_band_coefficients_cls = gray_band_coefficients_cls
    """
    gray_band_coefficients child of refractive_index.
    """
