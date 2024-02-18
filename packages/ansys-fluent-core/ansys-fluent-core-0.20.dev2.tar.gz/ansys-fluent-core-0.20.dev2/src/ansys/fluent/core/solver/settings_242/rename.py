#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .new_1 import new as new_cls
from .old import old as old_cls
class rename(CommandWithPositionalArgs):
    """
    Rename the object.
    
    Parameters
    ----------
        new : str
            New name for the object.
        old : str
            Select object to rename.
    
    """

    fluent_name = "rename"

    argument_names = \
        ['new', 'old']

    new: new_cls = new_cls
    """
    new argument of rename.
    """
    old: old_cls = old_cls
    """
    old argument of rename.
    """
