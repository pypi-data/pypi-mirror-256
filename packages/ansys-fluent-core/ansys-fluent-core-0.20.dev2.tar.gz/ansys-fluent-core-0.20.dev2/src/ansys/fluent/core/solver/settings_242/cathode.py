#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .cathode_cc_zone import cathode_cc_zone as cathode_cc_zone_cls
from .cathode_fc_zone import cathode_fc_zone as cathode_fc_zone_cls
from .cathode_pl_zone import cathode_pl_zone as cathode_pl_zone_cls
from .cathode_cl_zone import cathode_cl_zone as cathode_cl_zone_cls
class cathode(Group):
    """
    Set up cathode.
    """

    fluent_name = "cathode"

    child_names = \
        ['cathode_cc_zone', 'cathode_fc_zone', 'cathode_pl_zone',
         'cathode_cl_zone']

    cathode_cc_zone: cathode_cc_zone_cls = cathode_cc_zone_cls
    """
    cathode_cc_zone child of cathode.
    """
    cathode_fc_zone: cathode_fc_zone_cls = cathode_fc_zone_cls
    """
    cathode_fc_zone child of cathode.
    """
    cathode_pl_zone: cathode_pl_zone_cls = cathode_pl_zone_cls
    """
    cathode_pl_zone child of cathode.
    """
    cathode_cl_zone: cathode_cl_zone_cls = cathode_cl_zone_cls
    """
    cathode_cl_zone child of cathode.
    """
