#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .view_1 import view as view_cls
class stored_view(Command):
    """
    Play the 3D animation sequence using the view stored in the sequence.
    
    Parameters
    ----------
        view : bool
            Yes: "Stored View", no: "Different View".
    
    """

    fluent_name = "stored-view?"

    argument_names = \
        ['view']

    view: view_cls = view_cls
    """
    view argument of stored_view.
    """
