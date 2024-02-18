#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .cathode_fc_zone_list import cathode_fc_zone_list as cathode_fc_zone_list_cls
from .cathode_fc_condensation import cathode_fc_condensation as cathode_fc_condensation_cls
from .cathode_fc_evaporation import cathode_fc_evaporation as cathode_fc_evaporation_cls
class cathode_fc_zone(Group):
    """
    Set up cathode flow channel.
    """

    fluent_name = "cathode-fc-zone"

    child_names = \
        ['cathode_fc_zone_list', 'cathode_fc_condensation',
         'cathode_fc_evaporation']

    cathode_fc_zone_list: cathode_fc_zone_list_cls = cathode_fc_zone_list_cls
    """
    cathode_fc_zone_list child of cathode_fc_zone.
    """
    cathode_fc_condensation: cathode_fc_condensation_cls = cathode_fc_condensation_cls
    """
    cathode_fc_condensation child of cathode_fc_zone.
    """
    cathode_fc_evaporation: cathode_fc_evaporation_cls = cathode_fc_evaporation_cls
    """
    cathode_fc_evaporation child of cathode_fc_zone.
    """
