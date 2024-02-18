#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .bands import bands as bands_cls
class on_all_interfaces(Command):
    """
    Maximum number of bands to be employed at all the mixing planes.
    
    Parameters
    ----------
        bands : int
            Maximum number of band counts.
    
    """

    fluent_name = "on-all-interfaces"

    argument_names = \
        ['bands']

    bands: bands_cls = bands_cls
    """
    bands argument of on_all_interfaces.
    """
