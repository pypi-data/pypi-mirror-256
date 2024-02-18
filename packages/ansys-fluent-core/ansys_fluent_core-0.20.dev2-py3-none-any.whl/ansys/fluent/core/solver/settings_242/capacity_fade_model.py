#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_12 import enabled as enabled_cls
from .capacity_fade_table import capacity_fade_table as capacity_fade_table_cls
class capacity_fade_model(Group):
    """
    'capacity_fade_model' child.
    """

    fluent_name = "capacity-fade-model"

    child_names = \
        ['enabled', 'capacity_fade_table']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of capacity_fade_model.
    """
    capacity_fade_table: capacity_fade_table_cls = capacity_fade_table_cls
    """
    capacity_fade_table child of capacity_fade_model.
    """
