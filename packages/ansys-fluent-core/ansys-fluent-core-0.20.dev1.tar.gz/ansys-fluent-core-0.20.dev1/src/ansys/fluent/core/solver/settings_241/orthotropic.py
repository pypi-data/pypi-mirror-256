#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .direction_0 import direction_0 as direction_0_cls
from .direction_1 import direction_1 as direction_1_cls
from .diffusivity_0 import diffusivity_0 as diffusivity_0_cls
from .diffusivity_1 import diffusivity_1 as diffusivity_1_cls
from .diffusivity_2 import diffusivity_2 as diffusivity_2_cls
class orthotropic(Group):
    """
    'orthotropic' child.
    """

    fluent_name = "orthotropic"

    child_names = \
        ['direction_0', 'direction_1', 'diffusivity_0', 'diffusivity_1',
         'diffusivity_2']

    direction_0: direction_0_cls = direction_0_cls
    """
    direction_0 child of orthotropic.
    """
    direction_1: direction_1_cls = direction_1_cls
    """
    direction_1 child of orthotropic.
    """
    diffusivity_0: diffusivity_0_cls = diffusivity_0_cls
    """
    diffusivity_0 child of orthotropic.
    """
    diffusivity_1: diffusivity_1_cls = diffusivity_1_cls
    """
    diffusivity_1 child of orthotropic.
    """
    diffusivity_2: diffusivity_2_cls = diffusivity_2_cls
    """
    diffusivity_2 child of orthotropic.
    """
