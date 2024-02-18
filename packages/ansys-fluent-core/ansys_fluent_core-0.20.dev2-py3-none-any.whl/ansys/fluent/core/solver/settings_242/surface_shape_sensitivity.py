#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .method_10 import method as method_cls
from .smoothness import smoothness as smoothness_cls
class surface_shape_sensitivity(Group):
    """
    'surface_shape_sensitivity' child.
    """

    fluent_name = "surface-shape-sensitivity"

    child_names = \
        ['method', 'smoothness']

    method: method_cls = method_cls
    """
    method child of surface_shape_sensitivity.
    """
    smoothness: smoothness_cls = smoothness_cls
    """
    smoothness child of surface_shape_sensitivity.
    """
