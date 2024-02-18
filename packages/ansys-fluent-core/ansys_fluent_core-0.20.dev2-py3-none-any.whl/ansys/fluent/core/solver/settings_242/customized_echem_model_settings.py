#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .memory_num_per_cell import memory_num_per_cell as memory_num_per_cell_cls
from .initial_soc_1 import initial_soc as initial_soc_cls
from .reference_capacity import reference_capacity as reference_capacity_cls
class customized_echem_model_settings(Group):
    """
    User-defined echem model.
    """

    fluent_name = "customized-echem-model-settings"

    child_names = \
        ['memory_num_per_cell', 'initial_soc', 'reference_capacity']

    memory_num_per_cell: memory_num_per_cell_cls = memory_num_per_cell_cls
    """
    memory_num_per_cell child of customized_echem_model_settings.
    """
    initial_soc: initial_soc_cls = initial_soc_cls
    """
    initial_soc child of customized_echem_model_settings.
    """
    reference_capacity: reference_capacity_cls = reference_capacity_cls
    """
    reference_capacity child of customized_echem_model_settings.
    """
