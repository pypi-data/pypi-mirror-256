#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .uds_bc_child import uds_bc_child

class pb_disc_bc(NamedObject[uds_bc_child], _CreatableNamedObjectMixin[uds_bc_child]):
    """
    'pb_disc_bc' child.
    """

    fluent_name = "pb-disc-bc"

    child_object_type: uds_bc_child = uds_bc_child
    """
    child_object_type of pb_disc_bc.
    """
