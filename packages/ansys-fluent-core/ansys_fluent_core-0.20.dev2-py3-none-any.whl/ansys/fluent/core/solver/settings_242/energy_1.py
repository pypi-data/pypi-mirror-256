#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phasic_wall_heat_flux_form import phasic_wall_heat_flux_form as phasic_wall_heat_flux_form_cls
class energy(Group):
    """
    Multiphase energy options menu.
    """

    fluent_name = "energy"

    child_names = \
        ['phasic_wall_heat_flux_form']

    phasic_wall_heat_flux_form: phasic_wall_heat_flux_form_cls = phasic_wall_heat_flux_form_cls
    """
    phasic_wall_heat_flux_form child of energy.
    """
