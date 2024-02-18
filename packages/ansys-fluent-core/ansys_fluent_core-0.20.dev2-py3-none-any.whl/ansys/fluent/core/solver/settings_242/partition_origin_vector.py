#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .band_diffuse_frac_child import band_diffuse_frac_child

class partition_origin_vector(ListObject[band_diffuse_frac_child]):
    """
    'partition_origin_vector' child.
    """

    fluent_name = "partition-origin-vector"

    command_names = \
        ['list_properties', 'resize']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of partition_origin_vector.
    """
    resize: resize_cls = resize_cls
    """
    resize command of partition_origin_vector.
    """
    child_object_type: band_diffuse_frac_child = band_diffuse_frac_child
    """
    child_object_type of partition_origin_vector.
    """
