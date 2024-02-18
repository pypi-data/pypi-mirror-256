#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .domain_val import domain_val as domain_val_cls
class species_mass_flow(Command):
    """
    'species_mass_flow' command.
    
    Parameters
    ----------
        domain_val : str
            'domain_val' child.
    
    """

    fluent_name = "species-mass-flow"

    argument_names = \
        ['domain_val']

    domain_val: domain_val_cls = domain_val_cls
    """
    domain_val argument of species_mass_flow.
    """
