#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .flux_type import flux_type as flux_type_cls
class dbns_cases(Group):
    """
    'dbns_cases' child.
    """

    fluent_name = "dbns_cases"

    child_names = \
        ['flux_type']

    flux_type: flux_type_cls = flux_type_cls
    """
    flux_type child of dbns_cases.
    """
