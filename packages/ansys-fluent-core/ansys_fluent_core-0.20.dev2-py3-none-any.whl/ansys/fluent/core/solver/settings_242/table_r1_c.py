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
class table_r1_c(Group):
    """
    'table_r1_c' child.
    """

    fluent_name = "table-r1-c"

    child_names = \
        ['row_number', 'column_number', 'row_value', 'column_value',
         'table_value']

    row_number: row_number_cls = row_number_cls
    """
    row_number child of table_r1_c.
    """
    column_number: column_number_cls = column_number_cls
    """
    column_number child of table_r1_c.
    """
    row_value: row_value_cls = row_value_cls
    """
    row_value child of table_r1_c.
    """
    column_value: column_value_cls = column_value_cls
    """
    column_value child of table_r1_c.
    """
    table_value: table_value_cls = table_value_cls
    """
    table_value child of table_r1_c.
    """
    command_names = \
        ['write_table', 'read_table', 'print_table']

    write_table: write_table_cls = write_table_cls
    """
    write_table command of table_r1_c.
    """
    read_table: read_table_cls = read_table_cls
    """
    read_table command of table_r1_c.
    """
    print_table: print_table_cls = print_table_cls
    """
    print_table command of table_r1_c.
    """
