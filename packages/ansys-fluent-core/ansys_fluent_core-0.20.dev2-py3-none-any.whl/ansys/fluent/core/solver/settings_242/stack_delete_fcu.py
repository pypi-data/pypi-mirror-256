#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .fcu_name import fcu_name as fcu_name_cls
class stack_delete_fcu(Command):
    """
    Delete stack units.
    
    Parameters
    ----------
        fcu_name : str
            'fcu_name' child.
    
    """

    fluent_name = "stack-delete-fcu"

    argument_names = \
        ['fcu_name']

    fcu_name: fcu_name_cls = fcu_name_cls
    """
    fcu_name argument of stack_delete_fcu.
    """
