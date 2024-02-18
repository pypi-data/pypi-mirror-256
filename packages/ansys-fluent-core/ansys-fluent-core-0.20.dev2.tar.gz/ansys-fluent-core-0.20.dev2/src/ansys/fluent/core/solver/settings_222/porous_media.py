#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .relative_permeability import relative_permeability as relative_permeability_cls
class porous_media(Group):
    """
    'porous_media' child.
    """

    fluent_name = "porous-media"

    child_names = \
        ['relative_permeability']

    relative_permeability: relative_permeability_cls = relative_permeability_cls
    """
    relative_permeability child of porous_media.
    """
