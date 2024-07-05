import yaml
import os
import pathlib
from datetime import datetime
from utils.user_project import UserProject


# Global values in order to facilitate the expansion of new resources
VALID_METHODOLOGIES = ["static_ipet",
                       "hybrid_ipet", "wpevt", "dynamic_ga", "evt"]
VALID_ARCHITECTURE_STATIC_IPET = ["avr", "x86_64"]
VALID_ARCHITECTURE_INSTRUMENTATION = ["avr"]


class ConfigParser():
    """
    Reading, filter and update the UserProject using informations of config.yaml.

    Also, create new folder to this WCET analysis.


    Parameters
    ----------
        None


    Attributes
    ----------
    __path_yaml : str
        Directory of config.yaml file of current analysis

    __config : dict
        All information read of config.yaml

    methodology : str
        The methodology name. The valid options are declared in the VALID_METHODOLOGIES constant

    user_project : UserProject
        DTO if contain all information to the next components  
    """

    def __init__(self, path_yaml) -> None:
        self.__path_yaml = path_yaml    # Directory and filename of current config.yaml
        self.config = None              # All values read of config.yaml
        self.methodology = None         # Current methodology chosen by the user
        self.user_project = None        # DTO UserProject


    def run_config_parser(self):
        '''
        Façade to config.yaml reading pipeline.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        self.open_yaml_file()
        self.filter_and_create_user_project()
        self.filter_values_of_one_methodology()
        self.create_output_folder()


    def open_yaml_file(self):
        '''
        Open the config.yaml file and check if any errors occur


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        try:
            with open(self.__path_yaml, "r") as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
        except Exception:
            print("\33[41mError! The cannot open this config.yaml file.\33[0m")
            exit(1)


    def filter_and_create_user_project(self):
        '''
        Check the values of config.yaml and create the DTO UserProject with common values for all methodologies


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # Check if the mains fields exists
        try:
            self.methodology = self.config["run"]["methods"]
            temp_main_file_name = self.config["metadata"]["project_name"]
            temp_input_directory = self.config["metadata"]["c_program_path"]
            temp_output_directory = self.config["metadata"]["project_output"]
            temp_architecture = self.config["metadata"]["architecture"]
            temp_vendor = self.config["metadata"]["vendor"]
            temp_operational_system = self.config["metadata"][
                "operational_system"]
            temp_microcontroller_unit = self.config["metadata"][
                "microcontroller_unit"]
            temp_function_target = self.config["run"]["function_target"]
            temp_report_format = self.config["run"]["report"]
            temp_deadline = self.config["run"]["deadline"]
        except KeyError:
            self.__config_error_reading("'methods' or block 'run'")

        if not (self.methodology in VALID_METHODOLOGIES):
            self.__config_error_invalid_value("methods", VALID_METHODOLOGIES, 2)

        if temp_main_file_name == None:
            self.__config_error_invalid_value(
                "project_name", "<Valid filename>", 3)

        if temp_input_directory == None:
            self.__config_error_invalid_value(
                "c_program_path", "<Absolute directory is non null value>", 4)
        if not (os.path.isabs(temp_input_directory)):
            self.__config_error_invalid_value(
                "c_program_path", "<Valid absolute directory>", 5)
        if not (os.path.exists(temp_input_directory)):
            self.__config_error_invalid_value(
                "c_program_path", "<The directory must exist>", 6)

        if temp_output_directory == None:
            self.__config_error_invalid_value(
                "project_output", "<Absolute directory is non null value>", 7)
        if not (os.path.isabs(temp_output_directory)):
            self.__config_error_invalid_value(
                "project_output", "<Valid absolute directory>", 8)
        if not (os.path.exists(temp_output_directory)):
            self.__config_error_invalid_value(
                "project_output", "<The directory must exist>", 9)

        # Triple target
        if (self.methodology == "static_ipet"):
            if (not (temp_architecture in VALID_ARCHITECTURE_STATIC_IPET)):
                self.__config_error_invalid_value(
                    "architecture", VALID_ARCHITECTURE_STATIC_IPET, 10)
        elif (self.methodology in ["hybrid_ipet", "wpevt"]):
            if (not (temp_architecture in VALID_ARCHITECTURE_INSTRUMENTATION)):
                self.__config_error_invalid_value(
                    "architecture", VALID_ARCHITECTURE_INSTRUMENTATION, 11)
        else:
            if temp_architecture == None:
                self.__config_error_invalid_value(
                    "architecture", "<Architecture must be non null value>", 12)

        if temp_vendor == None:
            self.__config_error_invalid_value("vendor", "atmel, pc", 13)

        if temp_operational_system == None:
            self.__config_error_invalid_value(
                "operational_system", "none, windows, linux", 14)

        if temp_microcontroller_unit == None:
            self.__config_error_invalid_value(
                "microcontroller_unit", "atmega328, none", 15)

        if temp_function_target == None:
            temp_function_target = self.__config_warning_default_value(
                "function_target",
                "main")

        # Check if there are list and elements, finally check if there are valid options
        if not (type(temp_report_format) is list):
            temp_report_format = self.__config_warning_default_value("report", [
                                                                     "pdf"])
        else:
            if (len(temp_report_format) > 0):
                if (not ("pdf" in temp_report_format[0] or "json" in temp_report_format[0])):
                    temp_report_format = self.__config_warning_default_value("report", [
                                                                             "pdf"])
            else:
                temp_report_format = self.__config_warning_default_value(
                    "report",
                    ["pdf"])

        if temp_deadline == None or temp_deadline < 0:
            temp_deadline = self.__config_warning_default_value("deadline", 0)

        self.user_project = UserProject(
            main_file_name=temp_main_file_name,
            input_directory=temp_input_directory,
            output_directory="",  # This value will be updated in "create_output_folder"
            architecture=temp_architecture,
            vendor=temp_vendor,
            operational_system=temp_operational_system,
            microcontroller_unit=temp_microcontroller_unit,
            function_target=temp_function_target,
            report_format=temp_report_format,
            deadline=temp_deadline)


    def filter_values_of_one_methodology(self) -> None:
        '''
        Check the values of config.yaml for one methodology. The others values can be ignored.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # External libs - Mostly used by static or hybrid analysis
        if (self.methodology in ["static_ipet", "hybrid_ipet", "dynamic_ga", "wpevt"]):
            try:
                temp_llvm_path = self.config["external_libs"]["llvm_path"]
                temp_cbmc_path = self.config["external_libs"]["cbmc_path"]
            except KeyError:
                self.__config_error_reading("external_libs")

            if temp_llvm_path != None:
                if (not (os.path.isabs(temp_llvm_path))):
                    self.__config_error_invalid_value(
                        "llvm_path",
                        "<Valid absolute directory or null directory>", 16)

            if temp_cbmc_path != None:
                if (not (os.path.isabs(temp_cbmc_path))):
                    self.__config_error_invalid_value(
                        "cbmc_path",
                        "<Valid absolute directory or null directory>", 17)

            self.user_project.set_external_libs(temp_llvm_path, temp_cbmc_path)

        # Target - Used by hybrid or dynamic methodologies
        if (self.methodology in ["hybrid_ipet", "wpevt", "dynamic_ga", "evt"]):
            try:
                temp_board = self.config["target"]["board"]
                temp_serial_port = self.config["target"]["usb_port"]
                temp_flash_board = self.config["target"]["flash_board"]
            except KeyError:
                self.__config_error_reading("target")

            if (temp_board == None):
                temp_board = self.__config_warning_default_value("board", True)
            elif (not (temp_board in [True, False])):
                self.__config_error_invalid_value("board", "[True | False]", 18)

            if (temp_serial_port == None):
                self.__config_error_invalid_value(
                    "usb_port", "<Valid serial port is non null>", 19)
                
            if(temp_flash_board == None):
                temp_flash_board = self.__config_warning_default_value("flash_board", False)
            elif(type(temp_flash_board) is not bool):
                self.__config_error_invalid_value(
                    "flash_board", "[True | False]", 44)

            self.user_project.set_target(temp_board, temp_serial_port, temp_flash_board)

        # Inputs - Used by hybrid or dynamic methodologies
        if (self.methodology in ["hybrid_ipet", "wpevt", "dynamic_ga", "evt"]):
            try:
                temp_chosen_input = self.config["inputs"]["chosen_input"]
                temp_input_types = self.config["inputs"]["types"]
                temp_input_bounds_min = self.config["inputs"]["bounds_min"]
                temp_input_bounds_max = self.config["inputs"]["bounds_max"]
                temp_input_gen_method = self.config["inputs"]["gen_method"]
                temp_input_n_test_cases = self.config["inputs"]["n_test_cases"]
            except KeyError:
                self.__config_error_reading("inputs")

            if(self.methodology != "dynamic_ga"):
                if(temp_input_gen_method is None or temp_input_gen_method == "none"):
                    if (not (type(temp_chosen_input) is list)):
                        self.__config_error_invalid_value(
                            "chosen_input", "<Valid input values is a list>", 20)

            if (type(temp_input_types) is list):
                if (len(temp_input_types) == 0):
                    self.__config_error_invalid_value(
                        "types", "<Valid input type must contain elements>", 21)
            else:
                self.__config_error_invalid_value(
                    "types", "<Valid input type is a list>", 22)

            if (not (type(temp_input_bounds_min) is list)):
                self.__config_error_invalid_value(
                    "bounds_min", "<Valid min bounds is a list>", 23)

            if (not (type(temp_input_bounds_max) is list)):
                self.__config_error_invalid_value(
                    "bounds_max", "<Valid max bounds is a list>", 24)

            # The bound min is less or equal bound max
            # Just check if there are elements
            if (len(temp_input_bounds_min) > 0):
                if (len(temp_input_bounds_min) != len(temp_input_bounds_max)):
                    self.__config_error_invalid_value(
                        "bounds_min & bounds_max",
                        "<Both bound list must have same size>", 25)
                else:
                    for index in range(0, len(temp_input_bounds_min)):
                        if (type(temp_input_bounds_min[index]) in [int, float] and type(temp_input_bounds_max[index]) in [int, float]):
                            if (temp_input_bounds_min[index] > temp_input_bounds_max[index]):
                                self.__config_error_invalid_value(
                                    "bounds_min & bounds_max",
                                    "bounds_max >= bounds_min", 26)
                        else:
                            self.__config_error_invalid_value(
                                "bounds_min & bounds_max",
                                "<The bound must be type numeric>", 27)

            if(self.methodology != "dynamic_ga"):
                if (not (temp_input_gen_method in ["none", "random", "cbmc"])):
                    self.__config_error_invalid_value(
                        "gen_method", "[none | random | cbmc]", 28)

            if(self.methodology != "dynamic_ga"):
                if (type(temp_input_n_test_cases) is int):
                    if (temp_input_n_test_cases < 1):
                        self.__config_error_invalid_value(
                            "n_test_cases", "x >= 1", 29)
                else:
                    self.__config_error_invalid_value(
                        "n_test_cases", "<Test cases number must be integer>", 30)

            self.user_project.set_inputs(temp_chosen_input,
                                         temp_input_types,
                                         temp_input_bounds_min,
                                         temp_input_bounds_max,
                                         temp_input_gen_method,
                                         temp_input_n_test_cases)

        # evt - Any methodology that use EVT
        if (self.methodology in ["wpevt", "dynamic_ga", "evt"]):
            try:
                temp_number_exec = self.config["evt"]["number_exec"]
                temp_pwcet_bounds = self.config["evt"]["pwcet_bounds"]
            except KeyError:
                self.__config_error_reading("evt")

            if (temp_number_exec == None):
                temp_number_exec = self.__config_warning_default_value(
                    "number_exec",
                    10000)
            elif (type(temp_number_exec) is int):
                if (temp_number_exec < 5000):
                    self.__config_error_invalid_value(
                        "number_exec", "x >= 5000", 31)
            else:
                self.__config_error_invalid_value(
                    "number_exec", "<Number of executions must be integer>", 32)

            if (temp_pwcet_bounds == None):
                temp_pwcet_bounds = self.__config_warning_default_value(
                    "pwcet_bounds", [1E-9, 1E-10, 1E-11, 1E-12])
            elif (type(temp_pwcet_bounds) is list):
                if (len(temp_pwcet_bounds) == 0):
                    temp_pwcet_bounds = self.__config_warning_default_value(
                        "pwcet_bounds", [1E-9, 1E-10, 1E-11, 1E-12])
                elif (len(temp_pwcet_bounds) > 5):
                    self.__config_error_invalid_value(
                        "pwcet_bounds",
                        "<pWCET bounds list must have maximum 5 elements>", 33)
                else:
                    for probability in temp_pwcet_bounds:
                        if (float(probability) > 1E-6):
                            self.__config_error_invalid_value(
                                "pwcet_bounds", "x <= 1E-6", 34)
            else:
                self.__config_error_invalid_value(
                    "pwcet_bounds", "<pWCET bounds must be list>", 35)

            self.user_project.set_evt(temp_number_exec, temp_pwcet_bounds)

        # ga - Any methodology that use GA
        if (self.methodology in ["wpevt", "dynamic_ga"]):
            try:
                temp_parent_selection_type = self.config["ga"][
                    "parent_selection_type"]
                temp_crossover_type = self.config["ga"]["crossover_type"]
                temp_mutation_type = self.config["ga"]["mutation_type"]
                temp_mutation_percent_genes = self.config["ga"][
                    "mutation_percent_genes"]
                temp_stop_criteria = self.config["ga"]["stop_criteria"]
            except KeyError:
                self.__config_error_reading("ga")

            if (temp_parent_selection_type == None):
                temp_parent_selection_type = self.__config_warning_default_value(
                    "parent_selection_type", "sss")
            elif (not (temp_parent_selection_type in ["sss", "random", "rank", "sus", "tournament", "rws"])):
                self.__config_error_invalid_value(
                    "parent_selection_type",
                    "[sss | random | rank | sus | tournament | rws]", 36)

            if (temp_crossover_type == None):
                temp_crossover_type = self.__config_warning_default_value(
                    "crossover_type",
                    "two_points")
            elif (not (temp_crossover_type in ["two_points", "scattered", "single_point", "uniform"])):
                self.__config_error_invalid_value(
                    "crossover_type",
                    "[two_points | scattered | single_point | uniform]", 37)

            if (temp_mutation_type == None):
                temp_mutation_type = self.__config_warning_default_value(
                    "mutation_type",
                    "adaptive")
            elif (not (temp_mutation_type in ["adaptive", "inversion", "random", "scramble", "swap"])):
                self.__config_error_invalid_value(
                    "mutation_type",
                    "[adaptive | inversion | random | scramble | swap]", 38)

            if (temp_mutation_percent_genes == None):
                temp_mutation_percent_genes = self.__config_warning_default_value(
                    "mutation_percent_genes", [70, 15])
            elif (type(temp_mutation_percent_genes) is list):
                if (len(temp_mutation_percent_genes) == 0):
                    self.__config_error_invalid_value(
                        "mutation_percent_genes",
                        "<Mutation percent genes list must have elements>", 39)
                elif (len(temp_mutation_percent_genes) > 2):
                    self.__config_error_invalid_value(
                        "mutation_percent_genes",
                        "<Mutation percent genes list must have maximum 2 elements>",
                        40)
                else:
                    for percentage in temp_mutation_percent_genes:
                        if (percentage < 1 or percentage > 99):
                            self.__config_error_invalid_value(
                                "mutation_percent_genes", "1 <= x <= 99", 41)
            else:
                self.__config_error_invalid_value(
                    "mutation_percent_genes",
                    "<Mutation percent genes must be a list>", 42)

            if (temp_stop_criteria == None):
                temp_stop_criteria = self.__config_warning_default_value(
                    "stop_criteria",
                    True)
            elif (not (type(temp_stop_criteria) is bool)):
                self.__config_error_invalid_value(
                    "stop_criteria", "[True | False]", 43)

            self.user_project.set_ga(
                temp_parent_selection_type, temp_crossover_type,
                temp_mutation_type, temp_mutation_percent_genes,
                temp_stop_criteria)


    def create_output_folder(self):
        '''
        Create a new output folder for this execution, so it's possible prevent files from being overwritten


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # Use the time stamp to prevent two folders with the same name
        time_stamp = datetime.now().strftime("%Y_%m_%d-%Hh_%Mm_%Ss")

        # Create the output base folder concatenating the output directory created by user and the program name
        # Example: C:\Users\Peter\Desktop\output\myprogram
        temp_output_base_folder = os.path.join(
            os.path.realpath(self.config["metadata"]["project_output"]),
            self.config["metadata"]["project_name"])

        # Create one specific folder to this execution concatenating that base directory and the time stamp
        # Example: C:\Users\Peter\Desktop\output\myprogram\2023_12_12-00h_00m_00s_static_ipet
        output_directory = os.path.join(
            temp_output_base_folder,
            f"{time_stamp}_{self.methodology}")
        # Create the folder in file system
        pathlib.Path(output_directory).mkdir(parents=True, exist_ok=True)

        # Update the new output folder in DTO UserProject
        self.user_project.set_output_directory(output_directory)


    def __config_error_reading(self, field: str) -> None:
        '''
        Raise error because the field don't exist in the config.yaml


        Parameters
        ----------
        message : str
            The name of field


        Returns
        -------
            None
        '''
        print(
            "\n\33[41mError! The field of block " + field +
            " doesn't exist.\33[0m")
        print("Please, fix the config.yaml as the template.")
        print("Directory of config.yaml with error: " + self.__path_yaml)
        exit(1)


    def __config_error_invalid_value(
            self, field: str, valid_options: any, error_id: int) -> None:
        '''
        Raise error because the value is invalid


        Parameters
        ----------
        message : str
            The name of field

        valid_options : any
            The valid options for this field. This may be values range, options set, small text, and so on.

        error_id : int
            ID of this specific error. Useful for debugging or test

        Returns
        -------
            None
        '''
        print("\n\33[41mError! The field " + field +
              " is with invalid value.\33[0m")
        print("The valid options are: " + str(valid_options))
        print("Directory of config.yaml with error: " + self.__path_yaml)
        exit(error_id)


    def __config_warning_default_value(
            self, field: str, default_value: any) -> any:
        '''
        The value don't exist in the config.yaml, so FioWAT use default value


        Parameters
        ----------
        message : str
            The name of field

        default_value : any
            Default value of this field


        Returns
        -------
        default_value : any
            Default value of this field
        '''
        print("\n\33[43mWarning! The field " + field + " don't have value.\33[0m")
        print("The tool will use default value: " + str(default_value))
        return default_value
