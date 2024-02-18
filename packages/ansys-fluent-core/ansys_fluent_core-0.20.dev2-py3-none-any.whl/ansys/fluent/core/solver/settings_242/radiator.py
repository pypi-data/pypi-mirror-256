#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment as porous_jump_turb_wall_treatment_cls
from .loss_coefficient import loss_coefficient as loss_coefficient_cls
from .hc import hc as hc_cls
from .t_1 import t as t_cls
from .heat_flux import heat_flux as heat_flux_cls
from .discrete_phase_bc_type import discrete_phase_bc_type as discrete_phase_bc_type_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .discrete_phase_bc_function import discrete_phase_bc_function as discrete_phase_bc_function_cls
from .strength import strength as strength_cls
class radiator(Group):
    """
    Help not available.
    """

    fluent_name = "radiator"

    child_names = \
        ['porous_jump_turb_wall_treatment', 'loss_coefficient', 'hc', 't',
         'heat_flux', 'discrete_phase_bc_type', 'dem_collision_partner',
         'reinj_inj', 'discrete_phase_bc_function', 'strength']

    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment_cls = porous_jump_turb_wall_treatment_cls
    """
    porous_jump_turb_wall_treatment child of radiator.
    """
    loss_coefficient: loss_coefficient_cls = loss_coefficient_cls
    """
    loss_coefficient child of radiator.
    """
    hc: hc_cls = hc_cls
    """
    hc child of radiator.
    """
    t: t_cls = t_cls
    """
    t child of radiator.
    """
    heat_flux: heat_flux_cls = heat_flux_cls
    """
    heat_flux child of radiator.
    """
    discrete_phase_bc_type: discrete_phase_bc_type_cls = discrete_phase_bc_type_cls
    """
    discrete_phase_bc_type child of radiator.
    """
    dem_collision_partner: dem_collision_partner_cls = dem_collision_partner_cls
    """
    dem_collision_partner child of radiator.
    """
    reinj_inj: reinj_inj_cls = reinj_inj_cls
    """
    reinj_inj child of radiator.
    """
    discrete_phase_bc_function: discrete_phase_bc_function_cls = discrete_phase_bc_function_cls
    """
    discrete_phase_bc_function child of radiator.
    """
    strength: strength_cls = strength_cls
    """
    strength child of radiator.
    """
