#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .settings_2 import settings as settings_cls
from .reset import reset as reset_cls
from .invert import invert as invert_cls
class transparency_options(Group):
    """
    'transparency_options' child.
    """

    fluent_name = "transparency-options"

    child_names = \
        ['settings', 'reset', 'invert']

    settings: settings_cls = settings_cls
    """
    settings child of transparency_options.
    """
    reset: reset_cls = reset_cls
    """
    reset child of transparency_options.
    """
    invert: invert_cls = invert_cls
    """
    invert child of transparency_options.
    """
