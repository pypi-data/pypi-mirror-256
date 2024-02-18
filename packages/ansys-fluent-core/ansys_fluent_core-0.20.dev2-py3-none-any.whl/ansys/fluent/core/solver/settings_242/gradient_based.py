#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .postprocess_options import postprocess_options as postprocess_options_cls
from .monitors import monitors as monitors_cls
from .methods_2 import methods as methods_cls
from .calculation import calculation as calculation_cls
from .observables import observables as observables_cls
from .enable_16 import enable as enable_cls
class gradient_based(Group):
    """
    Gradient-based design menu.
    """

    fluent_name = "gradient-based"

    child_names = \
        ['postprocess_options', 'monitors', 'methods', 'calculation',
         'observables']

    postprocess_options: postprocess_options_cls = postprocess_options_cls
    """
    postprocess_options child of gradient_based.
    """
    monitors: monitors_cls = monitors_cls
    """
    monitors child of gradient_based.
    """
    methods: methods_cls = methods_cls
    """
    methods child of gradient_based.
    """
    calculation: calculation_cls = calculation_cls
    """
    calculation child of gradient_based.
    """
    observables: observables_cls = observables_cls
    """
    observables child of gradient_based.
    """
    command_names = \
        ['enable']

    enable: enable_cls = enable_cls
    """
    enable command of gradient_based.
    """
