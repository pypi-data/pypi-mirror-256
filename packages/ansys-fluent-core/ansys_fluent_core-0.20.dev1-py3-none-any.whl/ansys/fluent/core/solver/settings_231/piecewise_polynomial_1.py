#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .piecewise_polynomial_child_1 import piecewise_polynomial_child

class piecewise_polynomial(ListObject[piecewise_polynomial_child]):
    """
    'piecewise_polynomial' child.
    """

    fluent_name = "piecewise-polynomial"

    child_object_type: piecewise_polynomial_child = piecewise_polynomial_child
    """
    child_object_type of piecewise_polynomial.
    """
