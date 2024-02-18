#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .interface_name_3 import interface_name as interface_name_cls
from .bands import bands as bands_cls
class on_specified_interface(Command):
    """
    Maximum number of bands to be employed at the specified mixing plane interface.
    
    Parameters
    ----------
        interface_name : str
            Define the mixing plane interface to specify band count.
        bands : int
            Maximum number of band counts.
    
    """

    fluent_name = "on-specified-interface"

    argument_names = \
        ['interface_name', 'bands']

    interface_name: interface_name_cls = interface_name_cls
    """
    interface_name argument of on_specified_interface.
    """
    bands: bands_cls = bands_cls
    """
    bands argument of on_specified_interface.
    """
