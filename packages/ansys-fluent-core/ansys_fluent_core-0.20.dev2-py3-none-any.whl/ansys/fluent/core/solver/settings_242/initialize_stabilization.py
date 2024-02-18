#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .strategy import strategy as strategy_cls
from .scheme_2 import scheme as scheme_cls
class initialize_stabilization(Group):
    """
    Enter the stabilization initialization menu.
    """

    fluent_name = "initialize-stabilization"

    command_names = \
        ['strategy', 'scheme']

    strategy: strategy_cls = strategy_cls
    """
    strategy command of initialize_stabilization.
    """
    scheme: scheme_cls = scheme_cls
    """
    scheme command of initialize_stabilization.
    """
