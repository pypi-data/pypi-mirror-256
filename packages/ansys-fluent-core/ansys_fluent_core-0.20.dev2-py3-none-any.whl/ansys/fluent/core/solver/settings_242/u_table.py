#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .row_number import row_number as row_number_cls
from .column_number import column_number as column_number_cls
from .row_value import row_value as row_value_cls
from .column_value import column_value as column_value_cls
from .table_value import table_value as table_value_cls
from .write_table import write_table as write_table_cls
from .read_table import read_table as read_table_cls
from .print_table import print_table as print_table_cls
class u_table(Group):
    """
    'u_table' child.
    """

    fluent_name = "u-table"

    child_names = \
        ['row_number', 'column_number', 'row_value', 'column_value',
         'table_value']

    row_number: row_number_cls = row_number_cls
    """
    row_number child of u_table.
    """
    column_number: column_number_cls = column_number_cls
    """
    column_number child of u_table.
    """
    row_value: row_value_cls = row_value_cls
    """
    row_value child of u_table.
    """
    column_value: column_value_cls = column_value_cls
    """
    column_value child of u_table.
    """
    table_value: table_value_cls = table_value_cls
    """
    table_value child of u_table.
    """
    command_names = \
        ['write_table', 'read_table', 'print_table']

    write_table: write_table_cls = write_table_cls
    """
    write_table command of u_table.
    """
    read_table: read_table_cls = read_table_cls
    """
    read_table command of u_table.
    """
    print_table: print_table_cls = print_table_cls
    """
    print_table command of u_table.
    """
