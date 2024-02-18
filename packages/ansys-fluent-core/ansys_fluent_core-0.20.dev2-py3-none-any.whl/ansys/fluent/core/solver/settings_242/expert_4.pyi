#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class expert:
    fluent_name = ...
    child_names = ...
    backward_compatibility = ...
    command_names = ...

    def flux_scaling(self, enabled_all: bool, disabled_all: bool, interface_name: str, scale: bool):
        """
        Enable or disable flux scaling at the turbo interfaces.
        
        Parameters
        ----------
            enabled_all : bool
                Enable flux scaling for all the interfaces.
            disabled_all : bool
                Disable flux scaling for all the interfaces.
            interface_name : str
                Define the turbo interface to enable/disable flux scaling.
            scale : bool
                Enable or disable flux scaling for the turbo interface.
        
        """

    def print_settings(self, ):
        """
        Display the current status(on/off) of flux scaling for the turbo interfaces.
        """

