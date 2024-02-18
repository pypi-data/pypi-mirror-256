#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .mem_zone_list_1 import mem_zone_list as mem_zone_list_cls
from .mem_update import mem_update as mem_update_cls
from .mem_material import mem_material as mem_material_cls
from .mem_eqv_weight import mem_eqv_weight as mem_eqv_weight_cls
from .mem_alpha import mem_alpha as mem_alpha_cls
from .mem_beta import mem_beta as mem_beta_cls
from .mem_diff_corr import mem_diff_corr as mem_diff_corr_cls
from .mem_permeability import mem_permeability as mem_permeability_cls
from .mem_act import mem_act as mem_act_cls
class membrane(Group):
    """
    Set up membrane.
    """

    fluent_name = "membrane"

    child_names = \
        ['mem_zone_list', 'mem_update', 'mem_material', 'mem_eqv_weight',
         'mem_alpha', 'mem_beta', 'mem_diff_corr', 'mem_permeability',
         'mem_act']

    mem_zone_list: mem_zone_list_cls = mem_zone_list_cls
    """
    mem_zone_list child of membrane.
    """
    mem_update: mem_update_cls = mem_update_cls
    """
    mem_update child of membrane.
    """
    mem_material: mem_material_cls = mem_material_cls
    """
    mem_material child of membrane.
    """
    mem_eqv_weight: mem_eqv_weight_cls = mem_eqv_weight_cls
    """
    mem_eqv_weight child of membrane.
    """
    mem_alpha: mem_alpha_cls = mem_alpha_cls
    """
    mem_alpha child of membrane.
    """
    mem_beta: mem_beta_cls = mem_beta_cls
    """
    mem_beta child of membrane.
    """
    mem_diff_corr: mem_diff_corr_cls = mem_diff_corr_cls
    """
    mem_diff_corr child of membrane.
    """
    mem_permeability: mem_permeability_cls = mem_permeability_cls
    """
    mem_permeability child of membrane.
    """
    mem_act: mem_act_cls = mem_act_cls
    """
    mem_act child of membrane.
    """
