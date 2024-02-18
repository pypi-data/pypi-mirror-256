#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .submit import submit as submit_cls
class stack_submit_fcu(Command):
    """
    Apply stack units settings.
    
    Parameters
    ----------
        submit : bool
            'submit' child.
    
    """

    fluent_name = "stack-submit-fcu"

    argument_names = \
        ['submit']

    submit: submit_cls = submit_cls
    """
    submit argument of stack_submit_fcu.
    """
