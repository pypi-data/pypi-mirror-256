#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .feature_angle import feature_angle as feature_angle_cls
class feature(Group):
    """
    'feature' child.
    """

    fluent_name = "feature"

    child_names = \
        ['feature_angle']

    feature_angle: feature_angle_cls = feature_angle_cls
    """
    feature_angle child of feature.
    """
