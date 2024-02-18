#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .check_convergence import check_convergence as check_convergence_cls
from .absolute_criteria import absolute_criteria as absolute_criteria_cls
class adjoint_equations_child(Group):
    """
    'child_object_type' of adjoint_equations.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['check_convergence', 'absolute_criteria']

    check_convergence: check_convergence_cls = check_convergence_cls
    """
    check_convergence child of adjoint_equations_child.
    """
    absolute_criteria: absolute_criteria_cls = absolute_criteria_cls
    """
    absolute_criteria child of adjoint_equations_child.
    """
