#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .function_of import function_of as function_of_cls
from .range import range as range_cls
class piecewise_polynomial(Group):
    """
    'piecewise_polynomial' child.
    """

    fluent_name = "piecewise-polynomial"

    child_names = \
        ['function_of', 'range']

    function_of: function_of_cls = function_of_cls
    """
    function_of child of piecewise_polynomial.
    """
    range: range_cls = range_cls
    """
    range child of piecewise_polynomial.
    """
