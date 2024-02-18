#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .model_tip_loss import model_tip_loss as model_tip_loss_cls
from .tip_loss_limit import tip_loss_limit as tip_loss_limit_cls
from .prandtl_tuning_coefficient import prandtl_tuning_coefficient as prandtl_tuning_coefficient_cls
class tip_loss(Group):
    """
    Menu to define the rotor tip loss model.
    
     - method  : define the method to model rotor tip loss, quadratic-tip-loss, prandtl-tip-loss
     - tip-loss-limit : tip-loss-limit, 
     - prandtl-tuning-coefficient: prandtl-tuning-coefficient, 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "tip-loss"

    child_names = \
        ['model_tip_loss', 'tip_loss_limit', 'prandtl_tuning_coefficient']

    model_tip_loss: model_tip_loss_cls = model_tip_loss_cls
    """
    model_tip_loss child of tip_loss.
    """
    tip_loss_limit: tip_loss_limit_cls = tip_loss_limit_cls
    """
    tip_loss_limit child of tip_loss.
    """
    prandtl_tuning_coefficient: prandtl_tuning_coefficient_cls = prandtl_tuning_coefficient_cls
    """
    prandtl_tuning_coefficient child of tip_loss.
    """
