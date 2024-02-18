#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .across_injections_enabled import across_injections_enabled as across_injections_enabled_cls
class data_reduction(Group):
    """
    'data_reduction' child.
    """

    fluent_name = "data-reduction"

    child_names = \
        ['across_injections_enabled']

    across_injections_enabled: across_injections_enabled_cls = across_injections_enabled_cls
    """
    across_injections_enabled child of data_reduction.
    """
