#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .les_spec_name import les_spec_name as les_spec_name_cls
from .rfg_number_of_modes import rfg_number_of_modes as rfg_number_of_modes_cls
from .vm_nvortices import vm_nvortices as vm_nvortices_cls
from .les_embedded_fluctuations import les_embedded_fluctuations as les_embedded_fluctuations_cls
class turbulence(Group):
    """
    Help not available.
    """

    fluent_name = "turbulence"

    child_names = \
        ['les_spec_name', 'rfg_number_of_modes', 'vm_nvortices',
         'les_embedded_fluctuations']

    les_spec_name: les_spec_name_cls = les_spec_name_cls
    """
    les_spec_name child of turbulence.
    """
    rfg_number_of_modes: rfg_number_of_modes_cls = rfg_number_of_modes_cls
    """
    rfg_number_of_modes child of turbulence.
    """
    vm_nvortices: vm_nvortices_cls = vm_nvortices_cls
    """
    vm_nvortices child of turbulence.
    """
    les_embedded_fluctuations: les_embedded_fluctuations_cls = les_embedded_fluctuations_cls
    """
    les_embedded_fluctuations child of turbulence.
    """
