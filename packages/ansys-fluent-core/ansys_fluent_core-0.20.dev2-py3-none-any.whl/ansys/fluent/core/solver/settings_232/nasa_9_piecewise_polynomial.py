#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_properties_1 import list_properties as list_properties_cls
from .piecewise_polynomial_child import piecewise_polynomial_child

class nasa_9_piecewise_polynomial(ListObject[piecewise_polynomial_child]):
    """
    'nasa_9_piecewise_polynomial' child.
    """

    fluent_name = "nasa-9-piecewise-polynomial"

    command_names = \
        ['list_properties']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of nasa_9_piecewise_polynomial.
    """
    child_object_type: piecewise_polynomial_child = piecewise_polynomial_child
    """
    child_object_type of nasa_9_piecewise_polynomial.
    """
