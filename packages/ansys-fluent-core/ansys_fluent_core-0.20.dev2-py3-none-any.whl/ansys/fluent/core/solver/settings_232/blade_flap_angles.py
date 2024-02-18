#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .blade_flapping_cone import blade_flapping_cone as blade_flapping_cone_cls
from .blade_flapping_cyclic_sin import blade_flapping_cyclic_sin as blade_flapping_cyclic_sin_cls
from .blade_flapping_cyclic_cos import blade_flapping_cyclic_cos as blade_flapping_cyclic_cos_cls
class blade_flap_angles(Group):
    """
    Menu to define the rotor pitch angles.
    
     - blade-flapping-cone       : , 
     - blade-flapping-cyclic-sin : , 
     - blade-flapping-cyclic-cos : , 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "blade-flap-angles"

    child_names = \
        ['blade_flapping_cone', 'blade_flapping_cyclic_sin',
         'blade_flapping_cyclic_cos']

    blade_flapping_cone: blade_flapping_cone_cls = blade_flapping_cone_cls
    """
    blade_flapping_cone child of blade_flap_angles.
    """
    blade_flapping_cyclic_sin: blade_flapping_cyclic_sin_cls = blade_flapping_cyclic_sin_cls
    """
    blade_flapping_cyclic_sin child of blade_flap_angles.
    """
    blade_flapping_cyclic_cos: blade_flapping_cyclic_cos_cls = blade_flapping_cyclic_cos_cls
    """
    blade_flapping_cyclic_cos child of blade_flap_angles.
    """
