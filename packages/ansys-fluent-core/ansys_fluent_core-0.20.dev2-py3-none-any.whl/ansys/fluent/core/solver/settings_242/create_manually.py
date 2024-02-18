#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .si_name import si_name as si_name_cls
from .zone1_2 import zone1 as zone1_cls
from .zone2_2 import zone2 as zone2_cls
class create_manually(Command):
    """
    Create one-to-one interfaces between two groups of boundary zones even if they do not currently overlap.
    
    Parameters
    ----------
        si_name : str
            Enter a prefix for mesh interface names.
        zone1 : typing.List[str]
            Enter the boundary zones belonging to the first group.
        zone2 : typing.List[str]
            Enter the boundary zones belonging to the second group.
    
    """

    fluent_name = "create-manually"

    argument_names = \
        ['si_name', 'zone1', 'zone2']

    si_name: si_name_cls = si_name_cls
    """
    si_name argument of create_manually.
    """
    zone1: zone1_cls = zone1_cls
    """
    zone1 argument of create_manually.
    """
    zone2: zone2_cls = zone2_cls
    """
    zone2 argument of create_manually.
    """
