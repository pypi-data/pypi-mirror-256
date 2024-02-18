#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .home_options import home_options as home_options_cls
from .transparency_options import transparency_options as transparency_options_cls
from .isovalue_options import isovalue_options as isovalue_options_cls
from .clip_box_options import clip_box_options as clip_box_options_cls
from .clip_sphere_options import clip_sphere_options as clip_sphere_options_cls
from .compute_node_count import compute_node_count as compute_node_count_cls
from .display_3 import display as display_cls
class volumes_child(Group):
    """
    'child_object_type' of volumes.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'home_options', 'transparency_options', 'isovalue_options',
         'clip_box_options', 'clip_sphere_options', 'compute_node_count']

    name: name_cls = name_cls
    """
    name child of volumes_child.
    """
    home_options: home_options_cls = home_options_cls
    """
    home_options child of volumes_child.
    """
    transparency_options: transparency_options_cls = transparency_options_cls
    """
    transparency_options child of volumes_child.
    """
    isovalue_options: isovalue_options_cls = isovalue_options_cls
    """
    isovalue_options child of volumes_child.
    """
    clip_box_options: clip_box_options_cls = clip_box_options_cls
    """
    clip_box_options child of volumes_child.
    """
    clip_sphere_options: clip_sphere_options_cls = clip_sphere_options_cls
    """
    clip_sphere_options child of volumes_child.
    """
    compute_node_count: compute_node_count_cls = compute_node_count_cls
    """
    compute_node_count child of volumes_child.
    """
    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of volumes_child.
    """
