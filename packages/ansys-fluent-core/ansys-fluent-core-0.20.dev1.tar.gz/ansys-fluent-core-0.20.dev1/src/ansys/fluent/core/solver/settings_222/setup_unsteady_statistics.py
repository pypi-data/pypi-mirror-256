#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .udf_cf_names import udf_cf_names as udf_cf_names_cls
class setup_unsteady_statistics(Command):
    """
    'setup_unsteady_statistics' command.
    
    Parameters
    ----------
        udf_cf_names : typing.List[str]
            'udf_cf_names' child.
    
    """

    fluent_name = "setup-unsteady-statistics"

    argument_names = \
        ['udf_cf_names']

    udf_cf_names: udf_cf_names_cls = udf_cf_names_cls
    """
    udf_cf_names argument of setup_unsteady_statistics.
    """
