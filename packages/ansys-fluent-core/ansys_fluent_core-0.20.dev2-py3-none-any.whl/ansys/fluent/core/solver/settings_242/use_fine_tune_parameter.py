#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .apply_1 import apply as apply_cls
class use_fine_tune_parameter(Command):
    """
    Use fine-tuned parameters.
    
    Parameters
    ----------
        apply : bool
            'apply' child.
    
    """

    fluent_name = "use-fine-tune-parameter"

    argument_names = \
        ['apply']

    apply: apply_cls = apply_cls
    """
    apply argument of use_fine_tune_parameter.
    """
