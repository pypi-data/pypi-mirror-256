#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .gauge_pressure import gauge_pressure as gauge_pressure_cls
from .m_1 import m as m_cls
from .non_equil_boundary import non_equil_boundary as non_equil_boundary_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
class momentum(Group):
    """
    Help not available.
    """

    fluent_name = "momentum"

    child_names = \
        ['gauge_pressure', 'm', 'non_equil_boundary', 'coordinate_system',
         'flow_direction', 'axis_direction', 'axis_origin']

    gauge_pressure: gauge_pressure_cls = gauge_pressure_cls
    """
    gauge_pressure child of momentum.
    """
    m: m_cls = m_cls
    """
    m child of momentum.
    """
    non_equil_boundary: non_equil_boundary_cls = non_equil_boundary_cls
    """
    non_equil_boundary child of momentum.
    """
    coordinate_system: coordinate_system_cls = coordinate_system_cls
    """
    coordinate_system child of momentum.
    """
    flow_direction: flow_direction_cls = flow_direction_cls
    """
    flow_direction child of momentum.
    """
    axis_direction: axis_direction_cls = axis_direction_cls
    """
    axis_direction child of momentum.
    """
    axis_origin: axis_origin_cls = axis_origin_cls
    """
    axis_origin child of momentum.
    """
