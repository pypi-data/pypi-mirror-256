#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .sensitivity_orientation import sensitivity_orientation as sensitivity_orientation_cls
from .surface_shape_sensitivity import surface_shape_sensitivity as surface_shape_sensitivity_cls
from .reset_default import reset_default as reset_default_cls
class postprocess_options(Group):
    """
    Enter the postprocessing options menu.
    """

    fluent_name = "postprocess-options"

    child_names = \
        ['sensitivity_orientation', 'surface_shape_sensitivity']

    sensitivity_orientation: sensitivity_orientation_cls = sensitivity_orientation_cls
    """
    sensitivity_orientation child of postprocess_options.
    """
    surface_shape_sensitivity: surface_shape_sensitivity_cls = surface_shape_sensitivity_cls
    """
    surface_shape_sensitivity child of postprocess_options.
    """
    command_names = \
        ['reset_default']

    reset_default: reset_default_cls = reset_default_cls
    """
    reset_default command of postprocess_options.
    """
