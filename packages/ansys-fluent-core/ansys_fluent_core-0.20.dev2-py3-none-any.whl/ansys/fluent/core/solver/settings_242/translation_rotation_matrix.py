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
from .piecewise_linear_child import piecewise_linear_child

class translation_rotation_matrix(ListObject[piecewise_linear_child]):
    """
    'translation_rotation_matrix' child.
    """

    fluent_name = "translation-rotation-matrix"

    command_names = \
        ['list_properties', 'resize']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of translation_rotation_matrix.
    """
    resize: resize_cls = resize_cls
    """
    resize command of translation_rotation_matrix.
    """
    child_object_type: piecewise_linear_child = piecewise_linear_child
    """
    child_object_type of translation_rotation_matrix.
    """
