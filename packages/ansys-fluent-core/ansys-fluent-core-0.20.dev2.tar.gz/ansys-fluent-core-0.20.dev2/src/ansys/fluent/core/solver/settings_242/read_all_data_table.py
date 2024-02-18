#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_12 import enabled as enabled_cls
from .file_name_1 import file_name as file_name_cls
class read_all_data_table(Command):
    """
    'read_all_data_table' command.
    
    Parameters
    ----------
        enabled : bool
            'enabled' child.
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "read-all-data-table"

    argument_names = \
        ['enabled', 'file_name']

    enabled: enabled_cls = enabled_cls
    """
    enabled argument of read_all_data_table.
    """
    file_name: file_name_cls = file_name_cls
    """
    file_name argument of read_all_data_table.
    """
