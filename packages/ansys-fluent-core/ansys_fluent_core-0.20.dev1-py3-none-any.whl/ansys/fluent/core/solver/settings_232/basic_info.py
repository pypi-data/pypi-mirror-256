#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .number_of_blades import number_of_blades as number_of_blades_cls
from .rotor_speed import rotor_speed as rotor_speed_cls
from .tip_radius import tip_radius as tip_radius_cls
from .root_radius import root_radius as root_radius_cls
class basic_info(Group):
    """
    Menu to define the rotor basic informations:
    
     - Number of Blades 
     - Rotor Speed  , 
     - Tip Radius 
     - Root Radius , 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "basic-info"

    child_names = \
        ['number_of_blades', 'rotor_speed', 'tip_radius', 'root_radius']

    number_of_blades: number_of_blades_cls = number_of_blades_cls
    """
    number_of_blades child of basic_info.
    """
    rotor_speed: rotor_speed_cls = rotor_speed_cls
    """
    rotor_speed child of basic_info.
    """
    tip_radius: tip_radius_cls = tip_radius_cls
    """
    tip_radius child of basic_info.
    """
    root_radius: root_radius_cls = root_radius_cls
    """
    root_radius child of basic_info.
    """
