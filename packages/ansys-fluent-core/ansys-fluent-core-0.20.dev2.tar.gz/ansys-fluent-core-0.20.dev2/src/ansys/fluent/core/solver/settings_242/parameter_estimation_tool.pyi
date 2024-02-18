#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class parameter_estimation_tool:
    fluent_name = ...
    child_names = ...
    echem_model = ...
    thermal_abuse_fitting = ...
    command_names = ...

    def ntgk_curve_fitting(self, filename: List[str], capacity: Union[float, str], number_dod_level: int, min_dod: Union[float, str], max_dod: Union[float, str], capacity_fade_enabled: bool):
        """
        NTGK parameter estimation tool.
        
        Parameters
        ----------
            filename : typing.List[str]
                'filename' child.
            capacity : real
                'capacity' child.
            number_dod_level : int
                'number_dod_level' child.
            min_dod : real
                'min_dod' child.
            max_dod : real
                'max_dod' child.
            capacity_fade_enabled : bool
                'capacity_fade_enabled' child.
        
        """

    def ecm_curve_fitting(self, filename: List[str], capacity: Union[float, str], circuit_model: str, fitting_method: str, rs_fix: List[Union[float, str]], capacity_fade_enabled: bool, read_discharge_file_enabled: bool, number_discharge_file: int, discharge_filename: List[str]):
        """
        ECM parameter estimation tool.
        
        Parameters
        ----------
            filename : typing.List[str]
                'filename' child.
            capacity : real
                'capacity' child.
            circuit_model : str
                'circuit_model' child.
            fitting_method : str
                'fitting_method' child.
            rs_fix : typing.List[real]
                'rs_fix' child.
            capacity_fade_enabled : bool
                'capacity_fade_enabled' child.
            read_discharge_file_enabled : bool
                'read_discharge_file_enabled' child.
            number_discharge_file : int
                'number_discharge_file' child.
            discharge_filename : typing.List[str]
                'discharge_filename' child.
        
        """

