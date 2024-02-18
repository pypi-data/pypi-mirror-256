#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .reset import reset as reset_cls
class stack_reset_fcu(Command):
    """
    Reset stack units.
    
    Parameters
    ----------
        reset : bool
            'reset' child.
    
    """

    fluent_name = "stack-reset-fcu"

    argument_names = \
        ['reset']

    reset: reset_cls = reset_cls
    """
    reset argument of stack_reset_fcu.
    """
