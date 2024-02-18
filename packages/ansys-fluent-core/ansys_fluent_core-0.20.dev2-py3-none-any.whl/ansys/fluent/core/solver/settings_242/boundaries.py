#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .axis_2 import axis as axis_cls
from .degassing_1 import degassing as degassing_cls
from .exhaust_fan_1 import exhaust_fan as exhaust_fan_cls
from .fan_2 import fan as fan_cls
from .geometry_5 import geometry as geometry_cls
from .inlet_vent_1 import inlet_vent as inlet_vent_cls
from .intake_fan_1 import intake_fan as intake_fan_cls
from .interface_3 import interface as interface_cls
from .interior_2 import interior as interior_cls
from .mass_flow_inlet_1 import mass_flow_inlet as mass_flow_inlet_cls
from .mass_flow_outlet_1 import mass_flow_outlet as mass_flow_outlet_cls
from .network_1 import network as network_cls
from .network_end_2 import network_end as network_end_cls
from .outflow_1 import outflow as outflow_cls
from .outlet_vent_1 import outlet_vent as outlet_vent_cls
from .overset_1 import overset as overset_cls
from .periodic_3 import periodic as periodic_cls
from .porous_jump_2 import porous_jump as porous_jump_cls
from .pressure_far_field_2 import pressure_far_field as pressure_far_field_cls
from .pressure_inlet_1 import pressure_inlet as pressure_inlet_cls
from .pressure_outlet_2 import pressure_outlet as pressure_outlet_cls
from .radiator_2 import radiator as radiator_cls
from .rans_les_interface_1 import rans_les_interface as rans_les_interface_cls
from .recirculation_inlet_2 import recirculation_inlet as recirculation_inlet_cls
from .recirculation_outlet_2 import recirculation_outlet as recirculation_outlet_cls
from .shadow_1 import shadow as shadow_cls
from .symmetry_1 import symmetry as symmetry_cls
from .velocity_inlet_1 import velocity_inlet as velocity_inlet_cls
from .wall_1 import wall as wall_cls
class boundaries(Group):
    """
    'boundaries' child.
    """

    fluent_name = "boundaries"

    child_names = \
        ['axis', 'degassing', 'exhaust_fan', 'fan', 'geometry', 'inlet_vent',
         'intake_fan', 'interface', 'interior', 'mass_flow_inlet',
         'mass_flow_outlet', 'network', 'network_end', 'outflow',
         'outlet_vent', 'overset', 'periodic', 'porous_jump',
         'pressure_far_field', 'pressure_inlet', 'pressure_outlet',
         'radiator', 'rans_les_interface', 'recirculation_inlet',
         'recirculation_outlet', 'shadow', 'symmetry', 'velocity_inlet',
         'wall']

    axis: axis_cls = axis_cls
    """
    axis child of boundaries.
    """
    degassing: degassing_cls = degassing_cls
    """
    degassing child of boundaries.
    """
    exhaust_fan: exhaust_fan_cls = exhaust_fan_cls
    """
    exhaust_fan child of boundaries.
    """
    fan: fan_cls = fan_cls
    """
    fan child of boundaries.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of boundaries.
    """
    inlet_vent: inlet_vent_cls = inlet_vent_cls
    """
    inlet_vent child of boundaries.
    """
    intake_fan: intake_fan_cls = intake_fan_cls
    """
    intake_fan child of boundaries.
    """
    interface: interface_cls = interface_cls
    """
    interface child of boundaries.
    """
    interior: interior_cls = interior_cls
    """
    interior child of boundaries.
    """
    mass_flow_inlet: mass_flow_inlet_cls = mass_flow_inlet_cls
    """
    mass_flow_inlet child of boundaries.
    """
    mass_flow_outlet: mass_flow_outlet_cls = mass_flow_outlet_cls
    """
    mass_flow_outlet child of boundaries.
    """
    network: network_cls = network_cls
    """
    network child of boundaries.
    """
    network_end: network_end_cls = network_end_cls
    """
    network_end child of boundaries.
    """
    outflow: outflow_cls = outflow_cls
    """
    outflow child of boundaries.
    """
    outlet_vent: outlet_vent_cls = outlet_vent_cls
    """
    outlet_vent child of boundaries.
    """
    overset: overset_cls = overset_cls
    """
    overset child of boundaries.
    """
    periodic: periodic_cls = periodic_cls
    """
    periodic child of boundaries.
    """
    porous_jump: porous_jump_cls = porous_jump_cls
    """
    porous_jump child of boundaries.
    """
    pressure_far_field: pressure_far_field_cls = pressure_far_field_cls
    """
    pressure_far_field child of boundaries.
    """
    pressure_inlet: pressure_inlet_cls = pressure_inlet_cls
    """
    pressure_inlet child of boundaries.
    """
    pressure_outlet: pressure_outlet_cls = pressure_outlet_cls
    """
    pressure_outlet child of boundaries.
    """
    radiator: radiator_cls = radiator_cls
    """
    radiator child of boundaries.
    """
    rans_les_interface: rans_les_interface_cls = rans_les_interface_cls
    """
    rans_les_interface child of boundaries.
    """
    recirculation_inlet: recirculation_inlet_cls = recirculation_inlet_cls
    """
    recirculation_inlet child of boundaries.
    """
    recirculation_outlet: recirculation_outlet_cls = recirculation_outlet_cls
    """
    recirculation_outlet child of boundaries.
    """
    shadow: shadow_cls = shadow_cls
    """
    shadow child of boundaries.
    """
    symmetry: symmetry_cls = symmetry_cls
    """
    symmetry child of boundaries.
    """
    velocity_inlet: velocity_inlet_cls = velocity_inlet_cls
    """
    velocity_inlet child of boundaries.
    """
    wall: wall_cls = wall_cls
    """
    wall child of boundaries.
    """
