#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .cathode_gdl_zone_list import cathode_gdl_zone_list as cathode_gdl_zone_list_cls
from .cathode_gdl_update import cathode_gdl_update as cathode_gdl_update_cls
from .cathode_gdl_material import cathode_gdl_material as cathode_gdl_material_cls
from .cathode_gdl_porosity import cathode_gdl_porosity as cathode_gdl_porosity_cls
from .cathode_gdl_permeability import cathode_gdl_permeability as cathode_gdl_permeability_cls
from .cathode_gdl_angle import cathode_gdl_angle as cathode_gdl_angle_cls
from .cathode_gdl_angle_hi import cathode_gdl_angle_hi as cathode_gdl_angle_hi_cls
from .cathode_gdl_fraction import cathode_gdl_fraction as cathode_gdl_fraction_cls
from .cathode_gdl_waterremoval import cathode_gdl_waterremoval as cathode_gdl_waterremoval_cls
from .cathode_gdl_a import cathode_gdl_a as cathode_gdl_a_cls
from .cathode_gdl_b import cathode_gdl_b as cathode_gdl_b_cls
from .cathode_gdl_c import cathode_gdl_c as cathode_gdl_c_cls
from .cathode_gdl_condensation import cathode_gdl_condensation as cathode_gdl_condensation_cls
from .cathode_gdl_evaporation import cathode_gdl_evaporation as cathode_gdl_evaporation_cls
from .cathode_gdl_poresize import cathode_gdl_poresize as cathode_gdl_poresize_cls
class cathode_gdl_zone(Group):
    """
    Set up cathode GDL.
    """

    fluent_name = "cathode-gdl-zone"

    child_names = \
        ['cathode_gdl_zone_list', 'cathode_gdl_update',
         'cathode_gdl_material', 'cathode_gdl_porosity',
         'cathode_gdl_permeability', 'cathode_gdl_angle',
         'cathode_gdl_angle_hi', 'cathode_gdl_fraction',
         'cathode_gdl_waterremoval', 'cathode_gdl_a', 'cathode_gdl_b',
         'cathode_gdl_c', 'cathode_gdl_condensation',
         'cathode_gdl_evaporation', 'cathode_gdl_poresize']

    cathode_gdl_zone_list: cathode_gdl_zone_list_cls = cathode_gdl_zone_list_cls
    """
    cathode_gdl_zone_list child of cathode_gdl_zone.
    """
    cathode_gdl_update: cathode_gdl_update_cls = cathode_gdl_update_cls
    """
    cathode_gdl_update child of cathode_gdl_zone.
    """
    cathode_gdl_material: cathode_gdl_material_cls = cathode_gdl_material_cls
    """
    cathode_gdl_material child of cathode_gdl_zone.
    """
    cathode_gdl_porosity: cathode_gdl_porosity_cls = cathode_gdl_porosity_cls
    """
    cathode_gdl_porosity child of cathode_gdl_zone.
    """
    cathode_gdl_permeability: cathode_gdl_permeability_cls = cathode_gdl_permeability_cls
    """
    cathode_gdl_permeability child of cathode_gdl_zone.
    """
    cathode_gdl_angle: cathode_gdl_angle_cls = cathode_gdl_angle_cls
    """
    cathode_gdl_angle child of cathode_gdl_zone.
    """
    cathode_gdl_angle_hi: cathode_gdl_angle_hi_cls = cathode_gdl_angle_hi_cls
    """
    cathode_gdl_angle_hi child of cathode_gdl_zone.
    """
    cathode_gdl_fraction: cathode_gdl_fraction_cls = cathode_gdl_fraction_cls
    """
    cathode_gdl_fraction child of cathode_gdl_zone.
    """
    cathode_gdl_waterremoval: cathode_gdl_waterremoval_cls = cathode_gdl_waterremoval_cls
    """
    cathode_gdl_waterremoval child of cathode_gdl_zone.
    """
    cathode_gdl_a: cathode_gdl_a_cls = cathode_gdl_a_cls
    """
    cathode_gdl_a child of cathode_gdl_zone.
    """
    cathode_gdl_b: cathode_gdl_b_cls = cathode_gdl_b_cls
    """
    cathode_gdl_b child of cathode_gdl_zone.
    """
    cathode_gdl_c: cathode_gdl_c_cls = cathode_gdl_c_cls
    """
    cathode_gdl_c child of cathode_gdl_zone.
    """
    cathode_gdl_condensation: cathode_gdl_condensation_cls = cathode_gdl_condensation_cls
    """
    cathode_gdl_condensation child of cathode_gdl_zone.
    """
    cathode_gdl_evaporation: cathode_gdl_evaporation_cls = cathode_gdl_evaporation_cls
    """
    cathode_gdl_evaporation child of cathode_gdl_zone.
    """
    cathode_gdl_poresize: cathode_gdl_poresize_cls = cathode_gdl_poresize_cls
    """
    cathode_gdl_poresize child of cathode_gdl_zone.
    """
