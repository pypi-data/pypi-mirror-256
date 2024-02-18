#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_12 import enabled as enabled_cls
from .cell_type_1 import cell_type as cell_type_cls
from .cyl_axis_vec import cyl_axis_vec as cyl_axis_vec_cls
from .prism_axis_vec_1 import prism_axis_vec as prism_axis_vec_cls
from .prism_vec2_1 import prism_vec2 as prism_vec2_cls
from .pouch_normal_vec import pouch_normal_vec as pouch_normal_vec_cls
from .thermal_conductivity import thermal_conductivity as thermal_conductivity_cls
class orthotropic_k(Group):
    """
    'orthotropic_k' child.
    """

    fluent_name = "orthotropic-k"

    child_names = \
        ['enabled', 'cell_type', 'cyl_axis_vec', 'prism_axis_vec',
         'prism_vec2', 'pouch_normal_vec', 'thermal_conductivity']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of orthotropic_k.
    """
    cell_type: cell_type_cls = cell_type_cls
    """
    cell_type child of orthotropic_k.
    """
    cyl_axis_vec: cyl_axis_vec_cls = cyl_axis_vec_cls
    """
    cyl_axis_vec child of orthotropic_k.
    """
    prism_axis_vec: prism_axis_vec_cls = prism_axis_vec_cls
    """
    prism_axis_vec child of orthotropic_k.
    """
    prism_vec2: prism_vec2_cls = prism_vec2_cls
    """
    prism_vec2 child of orthotropic_k.
    """
    pouch_normal_vec: pouch_normal_vec_cls = pouch_normal_vec_cls
    """
    pouch_normal_vec child of orthotropic_k.
    """
    thermal_conductivity: thermal_conductivity_cls = thermal_conductivity_cls
    """
    thermal_conductivity child of orthotropic_k.
    """
