#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .cathode_cc_zone import cathode_cc_zone as cathode_cc_zone_cls
from .cathode_fc_zone_1 import cathode_fc_zone as cathode_fc_zone_cls
from .cathode_gdl_zone import cathode_gdl_zone as cathode_gdl_zone_cls
from .cathode_mpl_zone import cathode_mpl_zone as cathode_mpl_zone_cls
from .cathode_ca_zone import cathode_ca_zone as cathode_ca_zone_cls
class cathode(Group):
    """
    Set up cathode.
    """

    fluent_name = "cathode"

    child_names = \
        ['cathode_cc_zone', 'cathode_fc_zone', 'cathode_gdl_zone',
         'cathode_mpl_zone', 'cathode_ca_zone']

    cathode_cc_zone: cathode_cc_zone_cls = cathode_cc_zone_cls
    """
    cathode_cc_zone child of cathode.
    """
    cathode_fc_zone: cathode_fc_zone_cls = cathode_fc_zone_cls
    """
    cathode_fc_zone child of cathode.
    """
    cathode_gdl_zone: cathode_gdl_zone_cls = cathode_gdl_zone_cls
    """
    cathode_gdl_zone child of cathode.
    """
    cathode_mpl_zone: cathode_mpl_zone_cls = cathode_mpl_zone_cls
    """
    cathode_mpl_zone child of cathode.
    """
    cathode_ca_zone: cathode_ca_zone_cls = cathode_ca_zone_cls
    """
    cathode_ca_zone child of cathode.
    """
