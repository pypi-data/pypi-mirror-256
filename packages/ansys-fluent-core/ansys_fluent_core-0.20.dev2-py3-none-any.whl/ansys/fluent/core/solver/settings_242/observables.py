#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .named_expressions import named_expressions as named_expressions_cls
from .templated import templated as templated_cls
from .selection import selection as selection_cls
class observables(Group):
    """
    Enter the postprocessing options menu.
    """

    fluent_name = "observables"

    child_names = \
        ['named_expressions', 'templated', 'selection']

    named_expressions: named_expressions_cls = named_expressions_cls
    """
    named_expressions child of observables.
    """
    templated: templated_cls = templated_cls
    """
    templated child of observables.
    """
    selection: selection_cls = selection_cls
    """
    selection child of observables.
    """
