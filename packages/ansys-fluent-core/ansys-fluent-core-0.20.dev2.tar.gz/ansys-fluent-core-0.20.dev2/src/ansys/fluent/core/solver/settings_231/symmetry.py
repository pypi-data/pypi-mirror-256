#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .axis_child import axis_child

class symmetry(NamedObject[axis_child], _NonCreatableNamedObjectMixin[axis_child]):
    """
    'symmetry' child.
    """

    fluent_name = "symmetry"

    child_object_type: axis_child = axis_child
    """
    child_object_type of symmetry.
    """
