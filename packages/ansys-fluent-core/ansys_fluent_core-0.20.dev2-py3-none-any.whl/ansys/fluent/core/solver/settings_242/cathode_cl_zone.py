#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .cathode_cl_zone_list import cathode_cl_zone_list as cathode_cl_zone_list_cls
from .cathode_cl_update import cathode_cl_update as cathode_cl_update_cls
from .cathode_cl_material import cathode_cl_material as cathode_cl_material_cls
from .cathode_cl_porosity import cathode_cl_porosity as cathode_cl_porosity_cls
from .cathode_cl_kr import cathode_cl_kr as cathode_cl_kr_cls
from .cathode_cl_svratio import cathode_cl_svratio as cathode_cl_svratio_cls
from .cathode_cl_thickness import cathode_cl_thickness as cathode_cl_thickness_cls
from .cathode_cl_cp_function import cathode_cl_cp_function as cathode_cl_cp_function_cls
from .cathode_cl_angle import cathode_cl_angle as cathode_cl_angle_cls
from .cathode_cl_a import cathode_cl_a as cathode_cl_a_cls
from .cathode_cl_b import cathode_cl_b as cathode_cl_b_cls
from .cathode_cl_c import cathode_cl_c as cathode_cl_c_cls
class cathode_cl_zone(Group):
    """
    Set up cathode catalyst layer.
    """

    fluent_name = "cathode-cl-zone"

    child_names = \
        ['cathode_cl_zone_list', 'cathode_cl_update', 'cathode_cl_material',
         'cathode_cl_porosity', 'cathode_cl_kr', 'cathode_cl_svratio',
         'cathode_cl_thickness', 'cathode_cl_cp_function', 'cathode_cl_angle',
         'cathode_cl_a', 'cathode_cl_b', 'cathode_cl_c']

    cathode_cl_zone_list: cathode_cl_zone_list_cls = cathode_cl_zone_list_cls
    """
    cathode_cl_zone_list child of cathode_cl_zone.
    """
    cathode_cl_update: cathode_cl_update_cls = cathode_cl_update_cls
    """
    cathode_cl_update child of cathode_cl_zone.
    """
    cathode_cl_material: cathode_cl_material_cls = cathode_cl_material_cls
    """
    cathode_cl_material child of cathode_cl_zone.
    """
    cathode_cl_porosity: cathode_cl_porosity_cls = cathode_cl_porosity_cls
    """
    cathode_cl_porosity child of cathode_cl_zone.
    """
    cathode_cl_kr: cathode_cl_kr_cls = cathode_cl_kr_cls
    """
    cathode_cl_kr child of cathode_cl_zone.
    """
    cathode_cl_svratio: cathode_cl_svratio_cls = cathode_cl_svratio_cls
    """
    cathode_cl_svratio child of cathode_cl_zone.
    """
    cathode_cl_thickness: cathode_cl_thickness_cls = cathode_cl_thickness_cls
    """
    cathode_cl_thickness child of cathode_cl_zone.
    """
    cathode_cl_cp_function: cathode_cl_cp_function_cls = cathode_cl_cp_function_cls
    """
    cathode_cl_cp_function child of cathode_cl_zone.
    """
    cathode_cl_angle: cathode_cl_angle_cls = cathode_cl_angle_cls
    """
    cathode_cl_angle child of cathode_cl_zone.
    """
    cathode_cl_a: cathode_cl_a_cls = cathode_cl_a_cls
    """
    cathode_cl_a child of cathode_cl_zone.
    """
    cathode_cl_b: cathode_cl_b_cls = cathode_cl_b_cls
    """
    cathode_cl_b child of cathode_cl_zone.
    """
    cathode_cl_c: cathode_cl_c_cls = cathode_cl_c_cls
    """
    cathode_cl_c child of cathode_cl_zone.
    """
