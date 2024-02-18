#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .size import size as size_cls
class resize(CommandWithPositionalArgs):
    """
    Set number of objects for list-object.
    
    Parameters
    ----------
        size : int
            New size for list-object.
    
    """

    fluent_name = "resize"

    argument_names = \
        ['size']

    size: size_cls = size_cls
    """
    size argument of resize.
    """
