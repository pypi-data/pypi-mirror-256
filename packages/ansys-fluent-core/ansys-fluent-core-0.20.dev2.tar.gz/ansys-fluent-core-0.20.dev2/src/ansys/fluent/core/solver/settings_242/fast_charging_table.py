#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .write_table import write_table as write_table_cls
from .read_table import read_table as read_table_cls
from .print_table import print_table as print_table_cls
class fast_charging_table(Group):
    """
    'fast_charging_table' child.
    """

    fluent_name = "fast-charging-table"

    command_names = \
        ['write_table', 'read_table', 'print_table']

    write_table: write_table_cls = write_table_cls
    """
    write_table command of fast_charging_table.
    """
    read_table: read_table_cls = read_table_cls
    """
    read_table command of fast_charging_table.
    """
    print_table: print_table_cls = print_table_cls
    """
    print_table command of fast_charging_table.
    """
