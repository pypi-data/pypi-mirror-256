#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .rom_type_1 import rom_type as rom_type_cls
class create_journal_file(Command):
    """
    Create journal file.
    
    Parameters
    ----------
        rom_type : int
            'rom_type' child.
    
    """

    fluent_name = "create-journal-file"

    argument_names = \
        ['rom_type']

    rom_type: rom_type_cls = rom_type_cls
    """
    rom_type argument of create_journal_file.
    """
