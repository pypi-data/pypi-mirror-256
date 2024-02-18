#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .local_dt import local_dt as local_dt_cls
from .global_dt import global_dt as global_dt_cls
class advanced_options(Group):
    """
    'advanced_options' child.
    """

    fluent_name = "advanced-options"

    child_names = \
        ['local_dt', 'global_dt']

    local_dt: local_dt_cls = local_dt_cls
    """
    local_dt child of advanced_options.
    """
    global_dt: global_dt_cls = global_dt_cls
    """
    global_dt child of advanced_options.
    """
