#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .function_of import function_of as function_of_cls
from .coefficients import coefficients as coefficients_cls
class polynomial(Group):
    """
    'polynomial' child.
    """

    fluent_name = "polynomial"

    child_names = \
        ['function_of', 'coefficients']

    function_of: function_of_cls = function_of_cls
    """
    function_of child of polynomial.
    """
    coefficients: coefficients_cls = coefficients_cls
    """
    coefficients child of polynomial.
    """
