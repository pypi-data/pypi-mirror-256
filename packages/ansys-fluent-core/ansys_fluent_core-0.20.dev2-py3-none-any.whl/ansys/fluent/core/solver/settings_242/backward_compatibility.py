#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pre_24r2_mp_discretization import pre_24r2_mp_discretization as pre_24r2_mp_discretization_cls
class backward_compatibility(Group):
    """
    List of backward compatbility options for GTI.
    """

    fluent_name = "backward-compatibility"

    command_names = \
        ['pre_24r2_mp_discretization']

    pre_24r2_mp_discretization: pre_24r2_mp_discretization_cls = pre_24r2_mp_discretization_cls
    """
    pre_24r2_mp_discretization command of backward_compatibility.
    """
