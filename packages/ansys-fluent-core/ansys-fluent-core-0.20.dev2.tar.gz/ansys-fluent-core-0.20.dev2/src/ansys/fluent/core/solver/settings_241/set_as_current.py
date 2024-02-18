#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .study_name import study_name as study_name_cls
class set_as_current(Command):
    """
    Set As Current Study.
    
    Parameters
    ----------
        study_name : str
            'study_name' child.
    
    """

    fluent_name = "set-as-current"

    argument_names = \
        ['study_name']

    study_name: study_name_cls = study_name_cls
    """
    study_name argument of set_as_current.
    """
