#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class thermal_abuse_fitting:
    fluent_name = ...
    child_names = ...
    test_data_sets = ...
    rhocp = ...
    area = ...
    vol = ...
    epsilon = ...
    fixm_enabled = ...
    mvalue = ...
    fixn_enabled = ...
    nvalue = ...
    filename = ...
    initial_temp = ...
    ambient_temp = ...
    external_ht_coeff = ...
    enclosure_temp = ...
    command_names = ...

    def abuse_curve_fitting(self, ):
        """
        Thermal abuse curve fitting.
        """

    def fine_tune_parameter(self, user_a: Union[float, str], user_e: Union[float, str], user_m: Union[float, str], user_n: Union[float, str]):
        """
        Fine tune Arrhenius rate parameters.
        
        Parameters
        ----------
            user_a : real
                'user_a' child.
            user_e : real
                'user_e' child.
            user_m : real
                'user_m' child.
            user_n : real
                'user_n' child.
        
        """

    def use_fine_tune_parameter(self, apply: bool):
        """
        Use fine-tuned parameters.
        
        Parameters
        ----------
            apply : bool
                'apply' child.
        
        """

