#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_22 import enabled as enabled_cls
class pre_24r2_mp_discretization(Command):
    """
    Pre 24R2 discretization for the mixing-plane.
    
    Parameters
    ----------
        enabled : bool
            Enable/Disable enhanced discretization for the mixing-plane.
    
    """

    fluent_name = "pre-24r2-mp-discretization"

    argument_names = \
        ['enabled']

    enabled: enabled_cls = enabled_cls
    """
    enabled argument of pre_24r2_mp_discretization.
    """
