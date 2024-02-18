#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .filename_3 import filename as filename_cls
from .boundary_list_1 import boundary_list as boundary_list_cls
from .global_ import global_ as global__cls
class export_boundary_mesh(Command):
    """
    Export boundary mesh file.
    
    Parameters
    ----------
        filename : str
            Output file name.
        boundary_list : typing.List[str]
            Select boundary zones for exporting mesh.
        global_ : bool
            Enable/disable output of mesh global number.
    
    """

    fluent_name = "export-boundary-mesh"

    argument_names = \
        ['filename', 'boundary_list', 'global_']

    filename: filename_cls = filename_cls
    """
    filename argument of export_boundary_mesh.
    """
    boundary_list: boundary_list_cls = boundary_list_cls
    """
    boundary_list argument of export_boundary_mesh.
    """
    global_: global__cls = global__cls
    """
    global_ argument of export_boundary_mesh.
    """
