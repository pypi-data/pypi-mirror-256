#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .autosave import autosave as autosave_cls
class calculation_activities(Group):
    """
    Enter the calculation activities menu.
    """

    fluent_name = "calculation-activities"

    command_names = \
        ['autosave']

    autosave: autosave_cls = autosave_cls
    """
    autosave command of calculation_activities.
    """
