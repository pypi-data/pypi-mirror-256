#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .rom_type_1 import rom_type as rom_type_cls
class rom_data_creator(Command):
    """
    ROM data creator.
    
    Parameters
    ----------
        rom_type : int
            'rom_type' child.
    
    """

    fluent_name = "rom-data-creator"

    argument_names = \
        ['rom_type']

    rom_type: rom_type_cls = rom_type_cls
    """
    rom_type argument of rom_data_creator.
    """
