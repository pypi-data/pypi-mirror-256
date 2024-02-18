#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .f_length import f_length as f_length_cls
from .re_theta_c import re_theta_c as re_theta_c_cls
from .re_theta_t import re_theta_t as re_theta_t_cls
class user_defined_transition(Group):
    """
    Set user-defined transition correlations.
    """

    fluent_name = "user-defined-transition"

    child_names = \
        ['f_length', 're_theta_c', 're_theta_t']

    f_length: f_length_cls = f_length_cls
    """
    f_length child of user_defined_transition.
    """
    re_theta_c: re_theta_c_cls = re_theta_c_cls
    """
    re_theta_c child of user_defined_transition.
    """
    re_theta_t: re_theta_t_cls = re_theta_t_cls
    """
    re_theta_t child of user_defined_transition.
    """
