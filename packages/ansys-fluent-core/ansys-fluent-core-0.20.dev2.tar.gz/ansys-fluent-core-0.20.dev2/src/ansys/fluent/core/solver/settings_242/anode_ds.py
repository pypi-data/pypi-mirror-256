#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .method_4 import method as method_cls
from .value_1 import value as value_cls
from .piecewise_linear_1 import piecewise_linear as piecewise_linear_cls
from .polynomial import polynomial as polynomial_cls
from .user_defined import user_defined as user_defined_cls
class anode_ds(Group):
    """
    'anode_ds' child.
    """

    fluent_name = "anode-ds"

    child_names = \
        ['method', 'value', 'piecewise_linear', 'polynomial', 'user_defined']

    method: method_cls = method_cls
    """
    method child of anode_ds.
    """
    value: value_cls = value_cls
    """
    value child of anode_ds.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of anode_ds.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of anode_ds.
    """
    user_defined: user_defined_cls = user_defined_cls
    """
    user_defined child of anode_ds.
    """
