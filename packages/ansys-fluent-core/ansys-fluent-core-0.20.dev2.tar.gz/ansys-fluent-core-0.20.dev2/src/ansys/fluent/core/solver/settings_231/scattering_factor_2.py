#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
class scattering_factor(Group):
    """
    'scattering_factor' child.
    """

    fluent_name = "scattering-factor"

    child_names = \
        ['option']

    option: option_cls = option_cls
    """
    option child of scattering_factor.
    """
