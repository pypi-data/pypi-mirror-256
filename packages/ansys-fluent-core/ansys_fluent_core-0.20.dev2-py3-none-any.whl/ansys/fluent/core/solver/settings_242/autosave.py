#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .file_name_2 import file_name as file_name_cls
from .frequency_3 import frequency as frequency_cls
from .max_files_1 import max_files as max_files_cls
class autosave(Command):
    """
    Menu for adjoint autosave.
    
    Parameters
    ----------
        file_name : str
            File name prefix for auto-saved files.
        frequency : int
            Autosave adjoint iteration frequency.
        max_files : int
            Maximum number of files retained.
    
    """

    fluent_name = "autosave"

    argument_names = \
        ['file_name', 'frequency', 'max_files']

    file_name: file_name_cls = file_name_cls
    """
    file_name argument of autosave.
    """
    frequency: frequency_cls = frequency_cls
    """
    frequency argument of autosave.
    """
    max_files: max_files_cls = max_files_cls
    """
    max_files argument of autosave.
    """
