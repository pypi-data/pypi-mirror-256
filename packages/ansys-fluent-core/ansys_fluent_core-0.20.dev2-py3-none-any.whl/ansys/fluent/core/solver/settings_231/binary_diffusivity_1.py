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
from .film_averaged import film_averaged as film_averaged_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial import polynomial as polynomial_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class binary_diffusivity(Group):
    """
    'binary_diffusivity' child.
    """

    fluent_name = "binary-diffusivity"

    child_names = \
        ['option', 'value', 'film_averaged', 'piecewise_linear',
         'piecewise_polynomial', 'polynomial', 'user_defined_function']

    option: option_cls = option_cls
    """
    option child of binary_diffusivity.
    """
    value: value_cls = value_cls
    """
    value child of binary_diffusivity.
    """
    film_averaged: film_averaged_cls = film_averaged_cls
    """
    film_averaged child of binary_diffusivity.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of binary_diffusivity.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of binary_diffusivity.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of binary_diffusivity.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of binary_diffusivity.
    """
