#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
from .value import value as value_cls
class lennard_jones_energy(Group):
    """
    'lennard_jones_energy' child.
    """

    fluent_name = "lennard-jones-energy"

    child_names = \
        ['option', 'value']

    option: option_cls = option_cls
    """
    option child of lennard_jones_energy.
    """
    value: value_cls = value_cls
    """
    value child of lennard_jones_energy.
    """
