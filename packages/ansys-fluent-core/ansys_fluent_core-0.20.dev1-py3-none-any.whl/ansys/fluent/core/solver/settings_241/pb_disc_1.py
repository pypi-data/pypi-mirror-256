#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .mean_and_std_deviation import mean_and_std_deviation as mean_and_std_deviation_cls
from .pb_disc_components import pb_disc_components as pb_disc_components_cls
class pb_disc(Group):
    """
    'pb_disc' child.
    """

    fluent_name = "pb-disc"

    child_names = \
        ['mean_and_std_deviation', 'pb_disc_components']

    mean_and_std_deviation: mean_and_std_deviation_cls = mean_and_std_deviation_cls
    """
    mean_and_std_deviation child of pb_disc.
    """
    pb_disc_components: pb_disc_components_cls = pb_disc_components_cls
    """
    pb_disc_components child of pb_disc.
    """
