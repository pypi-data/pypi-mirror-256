#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .import_files_enabled import import_files_enabled as import_files_enabled_cls
from .number_of_files import number_of_files as number_of_files_cls
from .files import files as files_cls
from .capacify_fade_enabled import capacify_fade_enabled as capacify_fade_enabled_cls
class raw_data(Command):
    """
    Specify U and Y parameters using raw data.
    
    Parameters
    ----------
        import_files_enabled : bool
            'import_files_enabled' child.
        number_of_files : int
            'number_of_files' child.
        files : typing.List[str]
            'files' child.
        capacify_fade_enabled : bool
            'capacify_fade_enabled' child.
    
    """

    fluent_name = "raw-data"

    argument_names = \
        ['import_files_enabled', 'number_of_files', 'files',
         'capacify_fade_enabled']

    import_files_enabled: import_files_enabled_cls = import_files_enabled_cls
    """
    import_files_enabled argument of raw_data.
    """
    number_of_files: number_of_files_cls = number_of_files_cls
    """
    number_of_files argument of raw_data.
    """
    files: files_cls = files_cls
    """
    files argument of raw_data.
    """
    capacify_fade_enabled: capacify_fade_enabled_cls = capacify_fade_enabled_cls
    """
    capacify_fade_enabled argument of raw_data.
    """
