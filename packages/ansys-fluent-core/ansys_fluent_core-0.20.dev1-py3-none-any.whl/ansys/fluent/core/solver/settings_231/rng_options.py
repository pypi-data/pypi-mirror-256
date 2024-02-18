#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .differential_viscosity_model import differential_viscosity_model as differential_viscosity_model_cls
from .swirl_dominated_flow import swirl_dominated_flow as swirl_dominated_flow_cls
class rng_options(Group):
    """
    'rng_options' child.
    """

    fluent_name = "rng-options"

    child_names = \
        ['differential_viscosity_model', 'swirl_dominated_flow']

    differential_viscosity_model: differential_viscosity_model_cls = differential_viscosity_model_cls
    """
    differential_viscosity_model child of rng_options.
    """
    swirl_dominated_flow: swirl_dominated_flow_cls = swirl_dominated_flow_cls
    """
    swirl_dominated_flow child of rng_options.
    """
