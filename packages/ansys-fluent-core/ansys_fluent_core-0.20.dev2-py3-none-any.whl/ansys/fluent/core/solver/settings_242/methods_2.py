#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .discretization_1 import discretization as discretization_cls
from .default_1 import default as default_cls
from .balanced import balanced as balanced_cls
from .best_match import best_match as best_match_cls
class methods(Group):
    """
    Adjoint method or discretization menu.
    """

    fluent_name = "methods"

    child_names = \
        ['discretization']

    discretization: discretization_cls = discretization_cls
    """
    discretization child of methods.
    """
    command_names = \
        ['default', 'balanced', 'best_match']

    default: default_cls = default_cls
    """
    default command of methods.
    """
    balanced: balanced_cls = balanced_cls
    """
    balanced command of methods.
    """
    best_match: best_match_cls = best_match_cls
    """
    best_match command of methods.
    """
