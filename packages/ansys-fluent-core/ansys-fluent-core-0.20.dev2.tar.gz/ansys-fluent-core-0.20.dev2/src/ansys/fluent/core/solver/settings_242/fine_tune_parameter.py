#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .user_a import user_a as user_a_cls
from .user_e import user_e as user_e_cls
from .user_m import user_m as user_m_cls
from .user_n import user_n as user_n_cls
class fine_tune_parameter(Command):
    """
    Fine tune Arrhenius rate parameters.
    
    Parameters
    ----------
        user_a : real
            'user_a' child.
        user_e : real
            'user_e' child.
        user_m : real
            'user_m' child.
        user_n : real
            'user_n' child.
    
    """

    fluent_name = "fine-tune-parameter"

    argument_names = \
        ['user_a', 'user_e', 'user_m', 'user_n']

    user_a: user_a_cls = user_a_cls
    """
    user_a argument of fine_tune_parameter.
    """
    user_e: user_e_cls = user_e_cls
    """
    user_e argument of fine_tune_parameter.
    """
    user_m: user_m_cls = user_m_cls
    """
    user_m argument of fine_tune_parameter.
    """
    user_n: user_n_cls = user_n_cls
    """
    user_n argument of fine_tune_parameter.
    """
