#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .mass_flow_specification import mass_flow_specification as mass_flow_specification_cls
from .mass_flow_rate_1 import mass_flow_rate as mass_flow_rate_cls
from .mass_flux import mass_flux as mass_flux_cls
from .participates_in_solar_ray_tracing import participates_in_solar_ray_tracing as participates_in_solar_ray_tracing_cls
from .solar_transmissivity_factor import solar_transmissivity_factor as solar_transmissivity_factor_cls
class recirculation_outlet(Group):
    """
    Help not available.
    """

    fluent_name = "recirculation-outlet"

    child_names = \
        ['mass_flow_specification', 'mass_flow_rate', 'mass_flux',
         'participates_in_solar_ray_tracing', 'solar_transmissivity_factor']

    mass_flow_specification: mass_flow_specification_cls = mass_flow_specification_cls
    """
    mass_flow_specification child of recirculation_outlet.
    """
    mass_flow_rate: mass_flow_rate_cls = mass_flow_rate_cls
    """
    mass_flow_rate child of recirculation_outlet.
    """
    mass_flux: mass_flux_cls = mass_flux_cls
    """
    mass_flux child of recirculation_outlet.
    """
    participates_in_solar_ray_tracing: participates_in_solar_ray_tracing_cls = participates_in_solar_ray_tracing_cls
    """
    participates_in_solar_ray_tracing child of recirculation_outlet.
    """
    solar_transmissivity_factor: solar_transmissivity_factor_cls = solar_transmissivity_factor_cls
    """
    solar_transmissivity_factor child of recirculation_outlet.
    """
