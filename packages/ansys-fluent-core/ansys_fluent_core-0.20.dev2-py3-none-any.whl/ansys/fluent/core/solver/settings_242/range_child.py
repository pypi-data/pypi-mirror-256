#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .minimum import minimum as minimum_cls
from .maximum import maximum as maximum_cls
from .coefficients_1 import coefficients as coefficients_cls
class range_child(Group):
    """
    'child_object_type' of range.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['minimum', 'maximum', 'coefficients']

    minimum: minimum_cls = minimum_cls
    """
    minimum child of range_child.
    """
    maximum: maximum_cls = maximum_cls
    """
    maximum child of range_child.
    """
    coefficients: coefficients_cls = coefficients_cls
    """
    coefficients child of range_child.
    """
