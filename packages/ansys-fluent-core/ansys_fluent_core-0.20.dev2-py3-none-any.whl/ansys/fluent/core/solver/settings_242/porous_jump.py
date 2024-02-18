#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .porous_jump_turb_wall_treatment_1 import porous_jump_turb_wall_treatment as porous_jump_turb_wall_treatment_cls
from .alpha import alpha as alpha_cls
from .dm import dm as dm_cls
from .c2_1 import c2 as c2_cls
from .thermal_ctk import thermal_ctk as thermal_ctk_cls
from .solar_fluxes import solar_fluxes as solar_fluxes_cls
from .v_absp import v_absp as v_absp_cls
from .ir_absp import ir_absp as ir_absp_cls
from .ir_trans import ir_trans as ir_trans_cls
from .v_trans import v_trans as v_trans_cls
from .discrete_phase_bc_type import discrete_phase_bc_type as discrete_phase_bc_type_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .discrete_phase_bc_function import discrete_phase_bc_function as discrete_phase_bc_function_cls
from .strength import strength as strength_cls
from .jump_adhesion import jump_adhesion as jump_adhesion_cls
from .adhesion_constrained import adhesion_constrained as adhesion_constrained_cls
from .contact_angles import contact_angles as contact_angles_cls
from .x_displacement_type import x_displacement_type as x_displacement_type_cls
from .x_displacement_value import x_displacement_value as x_displacement_value_cls
from .y_displacement_type import y_displacement_type as y_displacement_type_cls
from .y_displacement_value import y_displacement_value as y_displacement_value_cls
from .z_displacement_type import z_displacement_type as z_displacement_type_cls
from .z_displacement_value import z_displacement_value as z_displacement_value_cls
class porous_jump(Group):
    """
    Help not available.
    """

    fluent_name = "porous-jump"

    child_names = \
        ['porous_jump_turb_wall_treatment', 'alpha', 'dm', 'c2',
         'thermal_ctk', 'solar_fluxes', 'v_absp', 'ir_absp', 'ir_trans',
         'v_trans', 'discrete_phase_bc_type', 'dem_collision_partner',
         'reinj_inj', 'discrete_phase_bc_function', 'strength',
         'jump_adhesion', 'adhesion_constrained', 'contact_angles',
         'x_displacement_type', 'x_displacement_value', 'y_displacement_type',
         'y_displacement_value', 'z_displacement_type',
         'z_displacement_value']

    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment_cls = porous_jump_turb_wall_treatment_cls
    """
    porous_jump_turb_wall_treatment child of porous_jump.
    """
    alpha: alpha_cls = alpha_cls
    """
    alpha child of porous_jump.
    """
    dm: dm_cls = dm_cls
    """
    dm child of porous_jump.
    """
    c2: c2_cls = c2_cls
    """
    c2 child of porous_jump.
    """
    thermal_ctk: thermal_ctk_cls = thermal_ctk_cls
    """
    thermal_ctk child of porous_jump.
    """
    solar_fluxes: solar_fluxes_cls = solar_fluxes_cls
    """
    solar_fluxes child of porous_jump.
    """
    v_absp: v_absp_cls = v_absp_cls
    """
    v_absp child of porous_jump.
    """
    ir_absp: ir_absp_cls = ir_absp_cls
    """
    ir_absp child of porous_jump.
    """
    ir_trans: ir_trans_cls = ir_trans_cls
    """
    ir_trans child of porous_jump.
    """
    v_trans: v_trans_cls = v_trans_cls
    """
    v_trans child of porous_jump.
    """
    discrete_phase_bc_type: discrete_phase_bc_type_cls = discrete_phase_bc_type_cls
    """
    discrete_phase_bc_type child of porous_jump.
    """
    dem_collision_partner: dem_collision_partner_cls = dem_collision_partner_cls
    """
    dem_collision_partner child of porous_jump.
    """
    reinj_inj: reinj_inj_cls = reinj_inj_cls
    """
    reinj_inj child of porous_jump.
    """
    discrete_phase_bc_function: discrete_phase_bc_function_cls = discrete_phase_bc_function_cls
    """
    discrete_phase_bc_function child of porous_jump.
    """
    strength: strength_cls = strength_cls
    """
    strength child of porous_jump.
    """
    jump_adhesion: jump_adhesion_cls = jump_adhesion_cls
    """
    jump_adhesion child of porous_jump.
    """
    adhesion_constrained: adhesion_constrained_cls = adhesion_constrained_cls
    """
    adhesion_constrained child of porous_jump.
    """
    contact_angles: contact_angles_cls = contact_angles_cls
    """
    contact_angles child of porous_jump.
    """
    x_displacement_type: x_displacement_type_cls = x_displacement_type_cls
    """
    x_displacement_type child of porous_jump.
    """
    x_displacement_value: x_displacement_value_cls = x_displacement_value_cls
    """
    x_displacement_value child of porous_jump.
    """
    y_displacement_type: y_displacement_type_cls = y_displacement_type_cls
    """
    y_displacement_type child of porous_jump.
    """
    y_displacement_value: y_displacement_value_cls = y_displacement_value_cls
    """
    y_displacement_value child of porous_jump.
    """
    z_displacement_type: z_displacement_type_cls = z_displacement_type_cls
    """
    z_displacement_type child of porous_jump.
    """
    z_displacement_value: z_displacement_value_cls = z_displacement_value_cls
    """
    z_displacement_value child of porous_jump.
    """
