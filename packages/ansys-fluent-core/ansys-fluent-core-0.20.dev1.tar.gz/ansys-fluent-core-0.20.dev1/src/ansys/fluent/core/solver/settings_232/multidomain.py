#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .conjugate_heat_transfer import conjugate_heat_transfer as conjugate_heat_transfer_cls
from .solve import solve as solve_cls
class multidomain(Group):
    """
    'multidomain' child.
    """

    fluent_name = "multidomain"

    child_names = \
        ['conjugate_heat_transfer', 'solve']

    conjugate_heat_transfer: conjugate_heat_transfer_cls = conjugate_heat_transfer_cls
    """
    conjugate_heat_transfer child of multidomain.
    """
    solve: solve_cls = solve_cls
    """
    solve child of multidomain.
    """
