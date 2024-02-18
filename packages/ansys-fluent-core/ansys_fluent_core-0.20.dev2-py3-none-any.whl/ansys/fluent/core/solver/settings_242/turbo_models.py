#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_21 import enabled as enabled_cls
from .general_turbo_interface import general_turbo_interface as general_turbo_interface_cls
from .export_boundary_mesh import export_boundary_mesh as export_boundary_mesh_cls
class turbo_models(Group):
    """
    Enter the turbo-models settings.
    """

    fluent_name = "turbo-models"

    child_names = \
        ['enabled', 'general_turbo_interface']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of turbo_models.
    """
    general_turbo_interface: general_turbo_interface_cls = general_turbo_interface_cls
    """
    general_turbo_interface child of turbo_models.
    """
    command_names = \
        ['export_boundary_mesh']

    export_boundary_mesh: export_boundary_mesh_cls = export_boundary_mesh_cls
    """
    export_boundary_mesh command of turbo_models.
    """
