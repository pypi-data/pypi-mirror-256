#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .design_point import design_point as design_point_cls
class set_as_current(Command):
    """
    Set current design point.
    
    Parameters
    ----------
        design_point : str
            'design_point' child.
    
    """

    fluent_name = "set-as-current"

    argument_names = \
        ['design_point']

    design_point: design_point_cls = design_point_cls
    """
    design_point argument of set_as_current.
    """
