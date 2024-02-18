#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .general_settings import general_settings as general_settings_cls
from .turbulent_setting import turbulent_setting as turbulent_setting_cls
class set_hybrid_init_options(Group):
    """
    'set_hybrid_init_options' child.
    """

    fluent_name = "set-hybrid-init-options"

    child_names = \
        ['general_settings', 'turbulent_setting']

    general_settings: general_settings_cls = general_settings_cls
    """
    general_settings child of set_hybrid_init_options.
    """
    turbulent_setting: turbulent_setting_cls = turbulent_setting_cls
    """
    turbulent_setting child of set_hybrid_init_options.
    """
