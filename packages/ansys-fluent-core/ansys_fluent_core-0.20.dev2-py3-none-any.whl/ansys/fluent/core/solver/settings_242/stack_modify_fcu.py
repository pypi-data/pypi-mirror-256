#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .fcu_name import fcu_name as fcu_name_cls
from .cellzones_1 import cellzones as cellzones_cls
class stack_modify_fcu(Command):
    """
    Modify stack units.
    
    Parameters
    ----------
        fcu_name : str
            'fcu_name' child.
        cellzones : typing.List[str]
            Enter cell zone name list.
    
    """

    fluent_name = "stack-modify-fcu"

    argument_names = \
        ['fcu_name', 'cellzones']

    fcu_name: fcu_name_cls = fcu_name_cls
    """
    fcu_name argument of stack_modify_fcu.
    """
    cellzones: cellzones_cls = cellzones_cls
    """
    cellzones argument of stack_modify_fcu.
    """
