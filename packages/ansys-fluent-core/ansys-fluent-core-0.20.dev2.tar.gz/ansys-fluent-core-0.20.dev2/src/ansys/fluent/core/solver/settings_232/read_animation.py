#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .read_from_file import read_from_file as read_from_file_cls
from .animation_file_name import animation_file_name as animation_file_name_cls
from .select_from_available import select_from_available as select_from_available_cls
from .animation_name import animation_name as animation_name_cls
class read_animation(Command):
    """
    Read new animation from file or already-defined animations.
    
    Parameters
    ----------
        read_from_file : bool
            'read_from_file' child.
        animation_file_name : str
            'animation_file_name' child.
        select_from_available : bool
            'select_from_available' child.
        animation_name : str
            'animation_name' child.
    
    """

    fluent_name = "read-animation"

    argument_names = \
        ['read_from_file', 'animation_file_name', 'select_from_available',
         'animation_name']

    read_from_file: read_from_file_cls = read_from_file_cls
    """
    read_from_file argument of read_animation.
    """
    animation_file_name: animation_file_name_cls = animation_file_name_cls
    """
    animation_file_name argument of read_animation.
    """
    select_from_available: select_from_available_cls = select_from_available_cls
    """
    select_from_available argument of read_animation.
    """
    animation_name: animation_name_cls = animation_name_cls
    """
    animation_name argument of read_animation.
    """
