#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .is_not_a_rans_les_interface import is_not_a_rans_les_interface as is_not_a_rans_les_interface_cls
class interior(Group):
    """
    Help not available.
    """

    fluent_name = "interior"

    child_names = \
        ['is_not_a_rans_les_interface']

    is_not_a_rans_les_interface: is_not_a_rans_les_interface_cls = is_not_a_rans_les_interface_cls
    """
    is_not_a_rans_les_interface child of interior.
    """
