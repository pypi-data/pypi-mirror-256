#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .heat_exchanger import heat_exchanger as heat_exchanger_cls
from .fluid_zone import fluid_zone as fluid_zone_cls
from .boundary_zone import boundary_zone as boundary_zone_cls
from .report_type import report_type as report_type_cls
from .write_to_file import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_file import append_file as append_file_cls
from .overwrite import overwrite as overwrite_cls
class specific_heat(Command):
    """
    'specific_heat' command.
    
    Parameters
    ----------
        heat_exchanger : str
            'heat_exchanger' child.
        fluid_zone : str
            'fluid_zone' child.
        boundary_zone : str
            'boundary_zone' child.
        report_type : str
            'report_type' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_file : bool
            'append_file' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "specific-heat"

    argument_names = \
        ['heat_exchanger', 'fluid_zone', 'boundary_zone', 'report_type',
         'write_to_file', 'file_name', 'append_file', 'overwrite']

    heat_exchanger: heat_exchanger_cls = heat_exchanger_cls
    """
    heat_exchanger argument of specific_heat.
    """
    fluid_zone: fluid_zone_cls = fluid_zone_cls
    """
    fluid_zone argument of specific_heat.
    """
    boundary_zone: boundary_zone_cls = boundary_zone_cls
    """
    boundary_zone argument of specific_heat.
    """
    report_type: report_type_cls = report_type_cls
    """
    report_type argument of specific_heat.
    """
    write_to_file: write_to_file_cls = write_to_file_cls
    """
    write_to_file argument of specific_heat.
    """
    file_name: file_name_cls = file_name_cls
    """
    file_name argument of specific_heat.
    """
    append_file: append_file_cls = append_file_cls
    """
    append_file argument of specific_heat.
    """
    overwrite: overwrite_cls = overwrite_cls
    """
    overwrite argument of specific_heat.
    """
