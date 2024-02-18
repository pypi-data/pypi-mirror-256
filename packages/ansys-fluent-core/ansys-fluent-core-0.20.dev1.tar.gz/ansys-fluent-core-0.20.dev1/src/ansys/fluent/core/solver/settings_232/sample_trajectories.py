#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .user_defined_functions_1 import user_defined_functions as user_defined_functions_cls
from .sort_sample_files import sort_sample_files as sort_sample_files_cls
from .sample_1 import sample as sample_cls
class sample_trajectories(Group):
    """
    'sample_trajectories' child.
    """

    fluent_name = "sample-trajectories"

    child_names = \
        ['user_defined_functions', 'sort_sample_files']

    user_defined_functions: user_defined_functions_cls = user_defined_functions_cls
    """
    user_defined_functions child of sample_trajectories.
    """
    sort_sample_files: sort_sample_files_cls = sort_sample_files_cls
    """
    sort_sample_files child of sample_trajectories.
    """
    command_names = \
        ['sample']

    sample: sample_cls = sample_cls
    """
    sample command of sample_trajectories.
    """
