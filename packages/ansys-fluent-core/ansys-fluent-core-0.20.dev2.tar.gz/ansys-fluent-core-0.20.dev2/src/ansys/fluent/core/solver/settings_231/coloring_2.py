#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .banded_coloring import banded_coloring as banded_coloring_cls
from .number_of_bands import number_of_bands as number_of_bands_cls
class coloring(Group):
    """
    Select coloring option.
    """

    fluent_name = "coloring"

    child_names = \
        ['banded_coloring', 'number_of_bands']

    banded_coloring: banded_coloring_cls = banded_coloring_cls
    """
    banded_coloring child of coloring.
    """
    number_of_bands: number_of_bands_cls = number_of_bands_cls
    """
    number_of_bands child of coloring.
    """
