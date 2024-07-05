from os.path import join


class UserProject:
    """
    DTO of user configurations, extracted from config.yaml file.


    Parameters
    ----------
        The same of attributes


    Attributes
    ----------
    main_file_name : str
        Name of main file of user project without extension. Example: quantum or dot_product

    input_directory : str
        Directory where main file is located

    output_directory : str
        Directory where report will be generated

    architecture : str
        Architeture of target. Example: avr, x86_64

    vendor : str
        Vendor of target. Example: pc, atmel

    operational_system : str
        Operational system of target. Example: windows, none

    microcontroller_unit : str
        Microcontroller of target. Example: atmega328, unknown

    function_target : str, default = main
        Function name that user wants calculate WCET

    report_format : list, default = ["pdf"]
        Which format the user wants to the report, each format generates another report. Options: pdf | json

    deadline : float, default = 0.0
        Deadline in cycles of program. If the value is 0, this means undefined/irrelevant deadline.

    llvm_path : str
        Directory where LLVM 16 is installed

    cbmc_path : str
        Directory where CBMC is installed

    board : bool
        Flag that select if the target is a board

    serial_port : str
        Specific the serial port where the comunication with board will occurs

    flash_board : bool, default = False
        If the board already has the program loaded

    input_types : list
        List of input variables types in the same sequence of input values.

        Example: [int(15), float, int]

    chosen_input : list
        User selected input. Example: [4, 3, 10, -5]       

    input_bounds_min : list
        List of input variables bounds min (ordered). If simple variable, pass single number. If array pass list. The range of minimum values is closedd.

        Example: [-1, 0, 70]

    input_bounds_max : list
        List of input variables bounds max (ordered). If simple variable, pass single number. If array pass list. The range of maximum values is opend.

        Example: [5, 100, -3]

    input_gen_method : str
        Select the method to generate input for instructions coverage.

        Example: cbmc

    input_n_test_cases : int
        Choose how many input values will be generated using input generation component

    number_exec : int, default = 10000
        Executions number of program using the same input

    pwcet_bounds : list, default = [1E-9, 1E-10, 1E-11, 1E-12]
        Desired probability of exceedance

    parent_selection_type : str, default = sss
        Technique to choose the parents. Example: tournament

    crossover_type : str, default = two_points
        Technique to choose crossover between two individuals

    mutation_type : str, default = adaptive
        Technique to insert variability in individuals

    mutation_percent_genes : list, default = [70,15]
        Only adaptive option requires list, for other options set one value only

        Example: [30]

    stop_criteria : bool, default = True
        Stop the evolution using the square of genes number or the cubic of genes number
    """

    def __init__(self,
                 main_file_name: str,
                 input_directory: str,
                 output_directory: str,
                 architecture: str,
                 vendor: str,
                 operational_system: str,
                 microcontroller_unit: str,
                 function_target: str = "main",
                 report_format: list = ["pdf"],
                 deadline: float = 0.0
                 ) -> None:

        # Remove the extension of filename
        main_file_name_without_extension = ""
        position = main_file_name.find(".")
        if (position != -1):
            position = 0
            while (main_file_name[position] != "."):
                main_file_name_without_extension += main_file_name[position]
                position += 1
        else:
            main_file_name_without_extension = main_file_name

        # Common values for all methodologies
        self.main_file_name = main_file_name_without_extension
        self.input_directory = join(input_directory, '')
        self.output_directory = join(output_directory, '')
        self.architecture = architecture
        self.vendor = vendor
        self.operational_system = operational_system
        self.microcontroller_unit = microcontroller_unit
        self.function_target = function_target

        # Others
        self.report_format = report_format
        self.deadline = deadline

        # External libs
        self.llvm_path = ""
        self.cbmc_path = ""

        # Target
        self.board = None
        self.serial_port = ""
        self.flash_board = False

        # Input values
        self.chosen_input = []
        self.input_types = []
        self.input_bounds_min = []
        self.input_bounds_max = []
        self.input_gen_method = ""
        self.input_n_test_cases = 0

        # EVT
        self.number_exec = 10000
        self.pwcet_bounds = [1E-9, 1E-10, 1E-11, 1E-12]

        # GA
        self.ga_pst = "sss"
        self.ga_csst = "two_points"
        self.ga_mtt = "adaptive"
        self.ga_mtpg = [70, 15]
        self.ga_stop_criteria = True

    def __str__(self) -> str:
        return "*** Project informations ***\nMain file name: " + self.main_file_name + \
            "\nFunction target: " + self.function_target + \
            "\nDirectory of project: " + self.input_directory + \
            "\nDirectory of output: " + self.output_directory + \
            "\nDeadline: " + str(self.deadline) + \
            "\n\n*** Target informations ***\nArchitecture: " + self.architecture + \
            "\nVendor: " + self.vendor + \
            "\nOperational system: " + self.operational_system + \
            "\nMicrocontroller unit: " + self.microcontroller_unit

    # SETTERS
    def set_input_directory(self, input_directory: str) -> None:
        self.input_directory = join(input_directory, '')

    def set_output_directory(self, output_directory: str) -> None:
        self.output_directory = join(output_directory, '')

    def set_external_libs(self, llvm_path: str, cbmc_path: str) -> None:
        if (llvm_path == None):
            self.llvm_path = ""
        else:
            self.llvm_path = join(llvm_path, '')
        if (cbmc_path == None):
            self.cbmc_path = ""
        else:
            self.cbmc_path = join(cbmc_path, '')

    def set_target(self, board: bool, serial_port: str, flash_board: bool) -> None:
        self.board = board
        self.serial_port = serial_port
        self.flash_board = flash_board

    def set_inputs(self, chosen_input: list, input_types: list, input_bounds_min: list, input_bounds_max: list, input_gen_method: str, input_n_test_cases: int) -> None:
        self.chosen_input = chosen_input
        self.input_types = input_types
        self.input_bounds_min = input_bounds_min
        self.input_bounds_max = input_bounds_max
        self.input_gen_method = input_gen_method
        self.input_n_test_cases = input_n_test_cases

    def set_evt(self, number_exec: int, pwcet_bounds: list) -> None:
        self.number_exec = number_exec
        self.pwcet_bounds = pwcet_bounds

    def set_ga(self, parent_selection_type: str, crossover_type: str, mutation_type: str, mutation_percent_genes: list, stop_criteria: bool) -> None:
        self.ga_pst = parent_selection_type
        self.ga_csst = crossover_type
        self.ga_mtt = mutation_type
        self.ga_mtpg = mutation_percent_genes
        self.ga_stop_criteria = stop_criteria

    # GETTERS

    def get_triple_target(self) -> str:
        return self.architecture + "-" + self.vendor + "-" + self.operational_system

    def get_env_name(self) -> str:
        if self.board:
            return "board"
        else:
            return "simul"

    def get_main_file_name(self) -> str:
        return self.main_file_name

    def get_input_directory(self) -> str:
        return self.input_directory

    def get_output_directory(self) -> str:
        return self.output_directory

    def get_architecture(self) -> str:
        return self.architecture

    def get_vendor(self) -> str:
        return self.vendor

    def get_operational_system(self) -> str:
        return self.operational_system

    def get_microcontroller_unit(self) -> str:
        return self.microcontroller_unit

    def get_function_target(self) -> str:
        return self.function_target

    def get_report_format(self) -> list:
        return self.report_format

    def get_deadline(self) -> float:
        return self.deadline

    def get_llvm_path(self) -> str:
        return self.llvm_path

    def get_cbmc_path(self) -> str:
        return self.cbmc_path

    def get_board(self) -> bool:
        return self.board

    def get_serial_port(self) -> str:
        return self.serial_port

    def get_flash_board(self) -> bool:
        return self.flash_board

    def get_chosen_input(self) -> list:
        return self.chosen_input

    def get_input_types(self) -> list:
        return self.input_types

    def get_input_bounds_min(self) -> list:
        return self.input_bounds_min

    def get_input_bounds_max(self) -> list:
        return self.input_bounds_max

    def get_input_gen_method(self) -> str:
        return self.input_gen_method

    def get_input_n_test_cases(self) -> int:
        return self.input_n_test_cases

    def get_number_exec(self) -> int:
        return self.number_exec

    def get_pwcet_bounds(self) -> list:
        return self.pwcet_bounds

    def get_parent_selection_type(self) -> str:
        return self.ga_pst

    def get_crossover_type(self) -> str:
        return self.ga_csst

    def get_mutation_type(self) -> str:
        return self.ga_mtt

    def get_mutation_percent_genes(self) -> list:
        return self.ga_mtpg

    def get_stop_criteria(self) -> bool:
        return self.ga_stop_criteria
