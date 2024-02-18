#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .fluid_2 import fluid as fluid_cls
from .solid_2 import solid as solid_cls
class volumes(Group):
    """
    Select type of volume.
    """

    fluent_name = "volumes"

    child_names = \
        ['fluid', 'solid']

    fluid: fluid_cls = fluid_cls
    """
    fluid child of volumes.
    """
    solid: solid_cls = solid_cls
    """
    solid child of volumes.
    """
