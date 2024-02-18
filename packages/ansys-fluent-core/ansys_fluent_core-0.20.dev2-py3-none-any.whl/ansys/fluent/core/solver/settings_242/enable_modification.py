#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .mod_name import mod_name as mod_name_cls
class enable_modification(Command):
    """
    Enable a single defined case modification.
    
    Parameters
    ----------
        mod_name : str
            'mod_name' child.
    
    """

    fluent_name = "enable-modification"

    argument_names = \
        ['mod_name']

    mod_name: mod_name_cls = mod_name_cls
    """
    mod_name argument of enable_modification.
    """
