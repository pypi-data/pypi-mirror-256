#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .design_points import design_points as design_points_cls
class clear_generated_data(Command):
    """
    Clear Generated Data.
    
    Parameters
    ----------
        design_points : typing.List[str]
            'design_points' child.
    
    """

    fluent_name = "clear-generated-data"

    argument_names = \
        ['design_points']

    design_points: design_points_cls = design_points_cls
    """
    design_points argument of clear_generated_data.
    """
