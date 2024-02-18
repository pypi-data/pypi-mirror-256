#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .gradient_based import gradient_based as gradient_based_cls
class design(Group):
    """
    'design' child.
    """

    fluent_name = "design"

    child_names = \
        ['gradient_based']

    gradient_based: gradient_based_cls = gradient_based_cls
    """
    gradient_based child of design.
    """
