#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .invalidate_case import invalidate_case as invalidate_case_cls
from .delete_all_compute_nodes import delete_all_compute_nodes as delete_all_compute_nodes_cls
class kill_all_nodes(Command):
    """
    Delete all compute nodes from virtual machine.
    
    Parameters
    ----------
        invalidate_case : bool
            'invalidate_case' child.
        delete_all_compute_nodes : bool
            'delete_all_compute_nodes' child.
    
    """

    fluent_name = "kill-all-nodes"

    argument_names = \
        ['invalidate_case', 'delete_all_compute_nodes']

    invalidate_case: invalidate_case_cls = invalidate_case_cls
    """
    invalidate_case argument of kill_all_nodes.
    """
    delete_all_compute_nodes: delete_all_compute_nodes_cls = delete_all_compute_nodes_cls
    """
    delete_all_compute_nodes argument of kill_all_nodes.
    """
