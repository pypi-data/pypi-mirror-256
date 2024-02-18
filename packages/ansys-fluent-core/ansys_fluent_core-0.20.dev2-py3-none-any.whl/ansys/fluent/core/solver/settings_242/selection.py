#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .adjoint_observable import adjoint_observable as adjoint_observable_cls
from .evaluate import evaluate as evaluate_cls
from .write_to_file_2 import write_to_file as write_to_file_cls
class selection(Group):
    """
    Observable selection menu.
    """

    fluent_name = "selection"

    child_names = \
        ['adjoint_observable']

    adjoint_observable: adjoint_observable_cls = adjoint_observable_cls
    """
    adjoint_observable child of selection.
    """
    command_names = \
        ['evaluate', 'write_to_file']

    evaluate: evaluate_cls = evaluate_cls
    """
    evaluate command of selection.
    """
    write_to_file: write_to_file_cls = write_to_file_cls
    """
    write_to_file command of selection.
    """
