from setup_test import *
import random
import pathlib

from src.pipeline.config_parser import ConfigParser
from src.utils.user_project import UserProject


class Test_open_yaml_file(unittest.TestCase):

    # VC-236
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.pipeline.config_parser.open')
    @patch('src.pipeline.config_parser.yaml')
    def test_01_normal_situation(self, mock_yaml, mock_open, mock_stdout):
        mock_yaml = Mock()
        mock_yaml.load.return_value = {'metadata': "program.c"}

        config = ConfigParser("Desktop")
        config.open_yaml_file()
        self.assertEqual(mock_stdout.getvalue(), "")


# Default value for all tests. Each test update specific fields of test
TEMPLATE_YAML_FILE = {
    "run": {
        "methods": "wpevt",
        "function_target": "dotproduct",
        "report": ["json"],
        "deadline": 100},
    "metadata": {
        "project_name": "program",
        "c_program_path": CURRENT_DIRECTORY,
        "project_output": CURRENT_DIRECTORY,
        "architecture": "avr",
        "vendor": "atmel",
        "operational_system": "none",
        "microcontroller_unit": "atmega328"},
    "external_libs": {
        "llvm_path": CURRENT_DIRECTORY,
        "cbmc_path": CURRENT_DIRECTORY},
    "target": {
        "board": False,
        "usb_port": "COM1",
        "flash_board": False},
    "inputs": {
        "chosen_input": [10, -1, 0, 3],
        "types": [int(2), float, int],
        "bounds_min": [0, -10, -3, 755],
        "bounds_max": [0, 5, -1, 964],
        "gen_method": "cbmc",
        "n_test_cases": 8},
    "evt": {
        "number_exec": 14000,
        "pwcet_bounds": [1E-20, 1E-21]},
    "ga": {
        "parent_selection_type": "rank",
        "crossover_type": "single_point",
        "mutation_type": "swap",
        "mutation_percent_genes": [50, 10],
        "stop_criteria": False}}


class Test_filter_and_create_user_project(unittest.TestCase):

    # VC-237
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_01_normal_situation(self, mock_stdout):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.filter_and_create_user_project()

        self.assertEqual(config.methodology, "wpevt")
        self.assertEqual(config.user_project.get_main_file_name(), "program")
        self.assertEqual(
            config.user_project.get_input_directory(),
            join(CURRENT_DIRECTORY, ''))
        self.assertEqual(config.user_project.get_output_directory(), "")
        self.assertEqual(config.user_project.get_architecture(), "avr")
        self.assertEqual(config.user_project.get_vendor(), "atmel")
        self.assertEqual(config.user_project.get_operational_system(), "none")
        self.assertEqual(
            config.user_project.get_microcontroller_unit(),
            "atmega328")
        self.assertEqual(
            config.user_project.get_function_target(),
            "dotproduct")
        self.assertEqual(config.user_project.get_report_format(), ["json"])
        self.assertEqual(config.user_project.get_deadline(), 100)
        self.assertEqual(mock_stdout.getvalue(), "")

    # VC-238
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_02_invalid_key(self, mock_stdout):
        config = ConfigParser("")
        config.config = {"run": {"methods": "static_ipet"}}

        result = "\n\33[41mError! The field of block methods | run doesn't exist.\33[0m\n" + \
                 "Please, fix the config.yaml as the template.\n" + \
                 "Directory of config.yaml with error: \n"

        with self.assertRaises(SystemExit):
            config.filter_and_create_user_project()
        self.assertEqual(mock_stdout.getvalue(), result)

    # VC-239
    def test_03_default_values(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["function_target"] = None
        config.config["run"]["report"] = None
        config.config["run"]["deadline"] = None
        config.filter_and_create_user_project()

        self.assertEqual(config.user_project.get_function_target(), "main")
        self.assertEqual(config.user_project.get_report_format(), ["pdf"])
        self.assertEqual(config.user_project.get_deadline(), 0)

        # Test the second default value
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["deadline"] = -5
        config.config["run"]["report"] = []
        config.filter_and_create_user_project()
        self.assertEqual(config.user_project.get_deadline(), 0)
        self.assertEqual(config.user_project.get_report_format(), ["pdf"])

        # Test the third default value
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["report"] = ["yaml", "pdf", "json"]
        self.assertEqual(config.user_project.get_report_format(), ["pdf"])

    # VC-240
    def test_04_methodology(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["methods"] = "fake_methodology"

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 2)

    # VC-241
    def test_05_filename(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["metadata"]["project_name"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 3)

    # VC-242
    def test_06_input_directory_null(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["metadata"]["c_program_path"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 4)

    # VC-243
    def test_07_input_directory_relative_directory(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)

        if 'win' in sys.platform:
            config.config["metadata"]["c_program_path"] = "Users\\John\\Downloads"
        else:
            config.config["metadata"]["c_program_path"] = "carla/Documents"

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 5)

    # VC-244
    def test_08_input_directory_exist_directory(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["metadata"]["c_program_path"] = CURRENT_DIRECTORY + \
            "nonexistfolder" + str(random.randint(0, 10000))

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 6)

    # VC-245
    def test_09_output_directory_null(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["metadata"]["project_output"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 7)

    # VC-246
    def test_10_output_directory_relative_directory(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)

        if 'win' in sys.platform:
            config.config["metadata"]["project_output"] = "Users\\John\\Downloads"
        else:
            config.config["metadata"]["project_output"] = "carla/Documents"

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 8)

    # VC-247
    def test_11_output_directory_exist_directory(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["metadata"]["project_output"] = CURRENT_DIRECTORY + \
            "nonexistfolder" + str(random.randint(0, 10000))

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 9)

    # VC-248
    def test_12_static_ipet_avr(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["methods"] = "static_ipet"

        config.filter_and_create_user_project()
        self.assertEqual(config.methodology, "static_ipet")

    # VC-249
    def test_12_static_ipet_invalid_architecture(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["methods"] = "static_ipet"
        config.config["metadata"]["architecture"] = "nonexistingarchitecture"

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 10)

    # VC-250
    def test_13_instrumentation_invalid_architecture(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["methods"] = "hybrid_ipet"
        config.config["metadata"]["architecture"] = "nonexistingarchitecture"

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 11)

    # VC-251
    def test_15_null_architecture(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["methods"] = "evt"
        config.config["metadata"]["architecture"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 12)

    # VC-252
    def test_16_null_vendor(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["metadata"]["vendor"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 13)

    # VC-253
    def test_17_null_operational_system(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["metadata"]["operational_system"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 14)

    # VC-254
    def test_18_null_microcontroller_unit(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["metadata"]["microcontroller_unit"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_and_create_user_project()
        self.assertEqual(code.exception.code, 15)

    # VC-255
    def test_19_methodology_static_ipet(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["methods"] = "static_ipet"

        config.filter_and_create_user_project()
        self.assertEqual(config.methodology, "static_ipet")

    # VC-256
    def test_20_methodology_hybrid_ipet(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["methods"] = "hybrid_ipet"

        config.filter_and_create_user_project()
        self.assertEqual(config.methodology, "hybrid_ipet")

    # VC-257
    def test_21_methodology_wpevt(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["methods"] = "wpevt"

        config.filter_and_create_user_project()
        self.assertEqual(config.methodology, "wpevt")

    # VC-258
    def test_22_methodology_dynamic_ga(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["methods"] = "dynamic_ga"

        config.filter_and_create_user_project()
        self.assertEqual(config.methodology, "dynamic_ga")

    # VC-259
    def test_23_methodology_evt(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["run"]["methods"] = "evt"

        config.filter_and_create_user_project()
        self.assertEqual(config.methodology, "evt")


TEMPLATE_USER_PROJECT = UserProject("program",
                                    CURRENT_DIRECTORY,
                                    "",
                                    "avr",
                                    "atmel",
                                    "none",
                                    "atmega328",
                                    "dotproduct",
                                    ["json"],
                                    100)


class Test_filter_values_of_one_methodology(unittest.TestCase):

    # VC-260
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_01_normal_situation(self, mock_stdout):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.filter_values_of_one_methodology()

        self.assertEqual(
            config.user_project.get_llvm_path(),
            join(CURRENT_DIRECTORY, ''))
        self.assertEqual(
            config.user_project.get_cbmc_path(),
            join(CURRENT_DIRECTORY, ''))
        self.assertEqual(config.user_project.get_board(), False)
        self.assertEqual(config.user_project.get_serial_port(), "COM1")
        self.assertEqual(config.user_project.get_chosen_input(), [10, -1, 0, 3])
        self.assertEqual(config.user_project.get_input_types(),
                         [int(2), float, int])
        self.assertEqual(
            config.user_project.get_input_bounds_min(),
            [0, -10, -3, 755])
        self.assertEqual(
            config.user_project.get_input_bounds_max(),
            [0, 5, -1, 964])
        self.assertEqual(config.user_project.get_input_gen_method(), "cbmc")
        self.assertEqual(config.user_project.get_input_n_test_cases(), 8)
        self.assertEqual(config.user_project.get_number_exec(), 14000)
        self.assertEqual(config.user_project.get_pwcet_bounds(), [1E-20, 1E-21])
        self.assertEqual(
            config.user_project.get_parent_selection_type(),
            "rank")
        self.assertEqual(
            config.user_project.get_crossover_type(),
            "single_point")
        self.assertEqual(config.user_project.get_mutation_type(), "swap")
        self.assertEqual(
            config.user_project.get_mutation_percent_genes(),
            [50, 10])
        self.assertEqual(config.user_project.get_stop_criteria(), False)
        self.assertEqual(mock_stdout.getvalue(), "")

    # VC-261
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_02_invalid_key_external_libs(self, mock_stdout):
        config = ConfigParser("")
        config.config = {}
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"

        result = "\n\33[41mError! The field of block external_libs doesn't exist.\33[0m\n" + \
                 "Please, fix the config.yaml as the template.\n" + \
                 "Directory of config.yaml with error: \n"

        with self.assertRaises(SystemExit):
            config.filter_values_of_one_methodology()
        self.assertEqual(mock_stdout.getvalue(), result)

    # VC-262
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_03_invalid_key_target(self, mock_stdout):
        config = ConfigParser("")
        config.config = {"external_libs": {
            "llvm_path": CURRENT_DIRECTORY,
            "cbmc_path": CURRENT_DIRECTORY}}
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"

        result = "\n\33[41mError! The field of block target doesn't exist.\33[0m\n" + \
                 "Please, fix the config.yaml as the template.\n" + \
                 "Directory of config.yaml with error: \n"

        with self.assertRaises(SystemExit):
            config.filter_values_of_one_methodology()
        self.assertEqual(mock_stdout.getvalue(), result)

    # VC-263
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_04_invalid_key_inputs(self, mock_stdout):
        config = ConfigParser("")
        config.config = {"external_libs": {
            "llvm_path": CURRENT_DIRECTORY,
            "cbmc_path": CURRENT_DIRECTORY},
            "target": {
            "board": False,
            "usb_port": "COM1",
            "flash_board": True}}
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"

        result = "\n\33[41mError! The field of block inputs doesn't exist.\33[0m\n" + \
                 "Please, fix the config.yaml as the template.\n" + \
                 "Directory of config.yaml with error: \n"

        with self.assertRaises(SystemExit):
            config.filter_values_of_one_methodology()
        self.assertEqual(mock_stdout.getvalue(), result)

    # VC-264
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_05_invalid_key_evt(self, mock_stdout):
        config = ConfigParser("")
        config.config = {"external_libs": {
            "llvm_path": CURRENT_DIRECTORY,
            "cbmc_path": CURRENT_DIRECTORY},
            "target": {
            "board": False,
            "usb_port": "COM1",
            "flash_board": True},
            "inputs": {
            "chosen_input": [10, -1, 0, 3],
            "types": [int(2), float, int],
            "bounds_min": [0, -10, -3, 755],
            "bounds_max": [0, 5, -1, 964],
            "gen_method": "cbmc",
            "n_test_cases": 8}}
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"

        result = "\n\33[41mError! The field of block evt doesn't exist.\33[0m\n" + \
                 "Please, fix the config.yaml as the template.\n" + \
                 "Directory of config.yaml with error: \n"

        with self.assertRaises(SystemExit):
            config.filter_values_of_one_methodology()
        self.assertEqual(mock_stdout.getvalue(), result)

    # VC-265
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_06_invalid_key_ga(self, mock_stdout):
        config = ConfigParser("")
        config.config = {"external_libs": {
            "llvm_path": CURRENT_DIRECTORY,
            "cbmc_path": CURRENT_DIRECTORY},
            "target": {
            "board": False,
            "usb_port": "COM1",
            "flash_board": True},
            "inputs": {
            "chosen_input": [10, -1, 0, 3],
            "types": [int(2), float, int],
            "bounds_min": [0, -10, -3, 755],
            "bounds_max": [0, 5, -1, 964],
            "gen_method": "cbmc",
            "n_test_cases": 8},
            "evt": {
            "number_exec": 14000,
            "pwcet_bounds": [1E-20, 1E-21]}}
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"

        result = "\n\33[41mError! The field of block ga doesn't exist.\33[0m\n" + \
                 "Please, fix the config.yaml as the template.\n" + \
                 "Directory of config.yaml with error: \n"

        with self.assertRaises(SystemExit):
            config.filter_values_of_one_methodology()
        self.assertEqual(mock_stdout.getvalue(), result)

    # VC-266
    def test_07_default_values(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["target"]["board"] = None
        config.config["target"]["flash_board"] = None
        config.config["evt"]["number_exec"] = None
        config.config["evt"]["pwcet_bounds"] = None
        config.config["ga"]["parent_selection_type"] = None
        config.config["ga"]["crossover_type"] = None
        config.config["ga"]["mutation_type"] = None
        config.config["ga"]["mutation_percent_genes"] = None
        config.config["ga"]["stop_criteria"] = None
        config.filter_values_of_one_methodology()

        self.assertEqual(config.user_project.get_board(), True)
        self.assertEqual(config.user_project.get_flash_board(), False)
        self.assertEqual(config.user_project.get_number_exec(), 10000)
        self.assertEqual(
            config.user_project.get_pwcet_bounds(),
            [1E-9, 1E-10, 1E-11, 1E-12])
        self.assertEqual(config.user_project.get_parent_selection_type(), "sss")
        self.assertEqual(config.user_project.get_crossover_type(), "two_points")
        self.assertEqual(config.user_project.get_mutation_type(), "adaptive")
        self.assertEqual(
            config.user_project.get_mutation_percent_genes(),
            [70, 15])
        self.assertEqual(config.user_project.get_stop_criteria(), True)

        # Test the second situation of default value
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.config["evt"]["pwcet_bounds"] = []
        config.filter_values_of_one_methodology()

        self.assertEqual(
            config.user_project.get_pwcet_bounds(),
            [1E-9, 1E-10, 1E-11, 1E-12])

    # VC-267
    def test_08_llvm_path_null(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["external_libs"]["llvm_path"] = None

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_llvm_path(), "")

    # VC-268
    def test_09_llvm_path_relative_directory(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"

        if 'win' in sys.platform:
            config.config["external_libs"]["llvm_path"] = "Users\\LLVM\\Downloads"
        else:
            config.config["external_libs"]["llvm_path"] = "carla/llvm"

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 16)

    # VC-269
    def test_10_cbmc_path_null(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["external_libs"]["cbmc_path"] = None

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_cbmc_path(), "")

    # VC-270
    def test_11_cbmc_path_relative_directory(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"

        if 'win' in sys.platform:
            config.config["external_libs"]["cbmc_path"] = "Users\\CBMC\\Downloads"
        else:
            config.config["external_libs"]["cbmc_path"] = "carla/cbmc"

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 17)

    # VC-271
    def test_12_board(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["target"]["board"] = 2

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 18)

    # VC-272
    def test_13_serial_port(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["target"]["usb_port"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 19)

    # VC-273
    def test_14_serial_port(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["target"]["usb_port"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 19)

    # VC-274
    def test_15_null_chosen_input(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["chosen_input"] = None
        config.config["inputs"]["gen_method"] = "none"

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 20)

    # VC-275
    def test_16_null_types(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["types"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 22)

    # VC-276
    def test_17_types_zero_size(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["types"] = []

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 21)

    # VC-277
    def test_18_null_bounds_min(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 23)

    # VC-278
    def test_19_null_bounds_max(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_max"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 24)

    # VC-279
    def test_20_bounds_different_size_1(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [2]
        config.config["inputs"]["bounds_max"] = []

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 25)

    # VC-280
    def test_21_bounds_different_size_2(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [2]
        config.config["inputs"]["bounds_max"] = [0, 0]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 25)

    # VC-281
    def test_22_bounds_non_numeric_elements_1(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [1]
        config.config["inputs"]["bounds_max"] = [None]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 27)

    # VC-282
    def test_23_bounds_non_numeric_elements_2(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [None]
        config.config["inputs"]["bounds_max"] = [None]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 27)

    # VC-283
    def test_24_bounds_non_numeric_elements_3(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [None]
        config.config["inputs"]["bounds_max"] = [1]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 27)

    # VC-284
    def test_25_bounds_non_numeric_elements_4(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [1, 1, -3, 0, "string", 5]
        config.config["inputs"]["bounds_max"] = [7, 7, 7, 7, 7, 7]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 27)

    # VC-285
    def test_26_bounds_non_numeric_elements_5(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [1, 1, -3, 0, 2, 5]
        config.config["inputs"]["bounds_max"] = [7, 7, [7, 7], 7, 7, 7]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 27)

    # VC-286
    def test_27_bounds_with_float(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [0, -8.75, 3.14159, 0.0]
        config.config["inputs"]["bounds_max"] = [1, 100, 7456.203460, 0]

        config.filter_values_of_one_methodology()
        self.assertEqual(
            config.user_project.get_input_bounds_min(),
            [0, -8.75, 3.14159, 0.0])
        self.assertEqual(
            config.user_project.get_input_bounds_max(),
            [1, 100, 7456.203460, 0])

    # VC-287
    def test_28_bounds_min_equal_bound_max(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [-5, 100, 20.3, 0, 1]
        config.config["inputs"]["bounds_max"] = [-5, 100, 20.3, 0, 1]

        config.filter_values_of_one_methodology()
        self.assertEqual(
            config.user_project.get_input_bounds_min(),
            [-5, 100, 20.3, 0, 1])
        self.assertEqual(
            config.user_project.get_input_bounds_max(),
            [-5, 100, 20.3, 0, 1])

    # VC-288
    def test_29_bounds_min_greater_than_bound_max_1(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [0]
        config.config["inputs"]["bounds_max"] = [-1]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 26)

    # VC-289
    def test_30_bounds_min_greater_than_bound_max_2(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [-5]
        config.config["inputs"]["bounds_max"] = [-5.00001]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 26)

    # VC-290
    def test_31_bounds_min_greater_than_bound_max_3(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["bounds_min"] = [10.0001]
        config.config["inputs"]["bounds_max"] = [10]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 26)

    # VC-291
    def test_32_null_gen_method(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["gen_method"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 28)

    # VC-292
    def test_33_gen_method_none(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["gen_method"] = "none"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_input_gen_method(), "none")

    # VC-293
    def test_34_gen_method_random(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["gen_method"] = "random"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_input_gen_method(), "random")

    # VC-294
    def test_35_gen_method_cbmc(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["gen_method"] = "cbmc"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_input_gen_method(), "cbmc")

    # VC-295
    def test_36_null_n_test_cases(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["n_test_cases"] = None

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 30)

    # VC-296
    def test_37_zero_n_test_cases(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["n_test_cases"] = 0

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 29)

    # VC-297
    def test_38_float_n_test_cases(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["n_test_cases"] = 10.5

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 30)

    # VC-298
    def test_39_negative_n_test_cases(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["n_test_cases"] = -100

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 29)

    # VC-299
    def test_40_one_n_test_cases(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["n_test_cases"] = 1

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_input_n_test_cases(), 1)

    # VC-300
    def test_41_5000_number_exec(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["evt"]["number_exec"] = 5000

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_number_exec(), 5000)

    # VC-301
    def test_42_4999_number_exec(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["evt"]["number_exec"] = 4999

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 31)

    # VC-302
    def test_43_float_number_exec(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["evt"]["number_exec"] = 10000.5

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 32)

    # VC-303
    def test_44_pwcet_bounds_non_list(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["evt"]["pwcet_bounds"] = 1E-9

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 35)

    # VC-304
    def test_45_pwcet_bounds_6_elements(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["evt"]["pwcet_bounds"] = [
            1E-9, 1E-10, 1E-11, 1E-12, 1E-13, 1E-14]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 33)

    # VC-305
    def test_46_pwcet_bounds_E_5(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["evt"]["pwcet_bounds"] = [1E-5]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 34)

    # VC-306
    def test_47_pwcet_bounds_E_6(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["evt"]["pwcet_bounds"] = [1E-6]

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_pwcet_bounds(), [1E-6])
        

    # VC-307
    def test_48_parent_selection_type_invalid(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["parent_selection_type"] = "non_existing_type"

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 36)

    # VC-308
    def test_49_parent_selection_type_sss(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["parent_selection_type"] = "sss"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_parent_selection_type(), "sss")

    # VC-309
    def test_50_parent_selection_type_random(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["parent_selection_type"] = "random"

        config.filter_values_of_one_methodology()
        self.assertEqual(
            config.user_project.get_parent_selection_type(),
            "random")

    # VC-310
    def test_51_parent_selection_type_rank(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["parent_selection_type"] = "rank"

        config.filter_values_of_one_methodology()
        self.assertEqual(
            config.user_project.get_parent_selection_type(),
            "rank")

    # VC-311
    def test_52_parent_selection_type_sus(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["parent_selection_type"] = "sus"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_parent_selection_type(), "sus")

    # VC-312
    def test_53_parent_selection_type_tournament(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["parent_selection_type"] = "tournament"

        config.filter_values_of_one_methodology()
        self.assertEqual(
            config.user_project.get_parent_selection_type(),
            "tournament")

    # VC-313
    def test_54_parent_selection_type_rws(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["parent_selection_type"] = "rws"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_parent_selection_type(), "rws")

    # VC-314
    def test_55_crossover_type_invalid(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["crossover_type"] = "non_existing_type"

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 37)

    # VC-315
    def test_56_crossover_type_two_points(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["crossover_type"] = "two_points"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_crossover_type(), "two_points")

    # VC-316
    def test_57_crossover_type_scattered(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["crossover_type"] = "scattered"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_crossover_type(), "scattered")

    # VC-317
    def test_58_crossover_type_single_point(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["crossover_type"] = "single_point"

        config.filter_values_of_one_methodology()
        self.assertEqual(
            config.user_project.get_crossover_type(),
            "single_point")

    # VC-318
    def test_59_crossover_type_uniform(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["crossover_type"] = "uniform"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_crossover_type(), "uniform")

    # VC-319
    def test_60_mutation_type_invalid(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_type"] = "non_existing_type"

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 38)

    # VC-320
    def test_61_mutation_type_inversion(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_type"] = "inversion"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_mutation_type(), "inversion")

    # VC-321
    def test_62_mutation_type_adaptive(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_type"] = "adaptive"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_mutation_type(), "adaptive")

    # VC-322
    def test_63_mutation_type_random(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_type"] = "random"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_mutation_type(), "random")

    # VC-323
    def test_64_mutation_type_scramble(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_type"] = "scramble"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_mutation_type(), "scramble")

    # VC-324
    def test_65_mutation_type_swap(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_type"] = "swap"

        config.filter_values_of_one_methodology()
        self.assertEqual(config.user_project.get_mutation_type(), "swap")

    # VC-325
    def test_66_mutation_percent_genes_non_list(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_percent_genes"] = 70

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 42)

    # VC-326
    def test_66_mutation_percent_genes_non_list(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_percent_genes"] = 70

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 42)

    # VC-327
    def test_67_mutation_percent_genes_0_elements(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_percent_genes"] = []

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 39)

    # VC-328
    def test_68_mutation_percent_genes_3_elements(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_percent_genes"] = [10, 20, 30]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 40)

    # VC-329
    def test_69_mutation_percent_genes_elements_less_than_1(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_percent_genes"] = [0, 50]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 41)

    # VC-330
    def test_70_mutation_percent_genes_elements_greater_than_1(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_percent_genes"] = [50, 100]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 41)

    # VC-331
    def test_71_mutation_percent_genes_elements_one_element_100(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["mutation_percent_genes"] = [100]

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 41)

    # VC-332
    def test_72_stop_criteria_non_bool(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["ga"]["stop_criteria"] = 2

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 43)

    #VC-363
    def test_73_flash_board_invalid(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["target"]["flash_board"] = 2

        with self.assertRaises(SystemExit) as code:
            config.filter_values_of_one_methodology()
        self.assertEqual(code.exception.code, 44)

    #VC-364
    def test_74_null_input_and_generation_method(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "wpevt"
        config.config["inputs"]["chosen_input"] = None
        config.config["inputs"]["gen_method"] = "cbmc"

        config.filter_values_of_one_methodology()

        self.assertEqual(config.user_project.get_input_gen_method(), "cbmc")
        self.assertEqual(config.user_project.get_chosen_input(), None)

    #VC-365
    def test_75_dynamic_ga_non_use_input_invalid_value(self):
        config = ConfigParser("")
        config.config = copy.deepcopy(TEMPLATE_YAML_FILE)
        config.user_project = copy.deepcopy(TEMPLATE_USER_PROJECT)
        config.methodology = "dynamic_ga"
        config.config["inputs"]["chosen_input"] = None
        config.config["inputs"]["gen_method"] = "nonexistingmethod"
        config.config["inputs"]["n_test_cases"] = 0

        config.filter_values_of_one_methodology()

        self.assertEqual(config.user_project.get_chosen_input(), None)
        self.assertEqual(config.user_project.get_input_gen_method(), "nonexistingmethod")
        self.assertEqual(config.user_project.get_input_n_test_cases(), 0)
        



class Test_create_output_folder(unittest.TestCase):

    # VC-333
    @patch('src.pipeline.config_parser.os.mkdir')
    @patch('src.pipeline.config_parser.pathlib')
    @patch('src.pipeline.config_parser.datetime')
    def test_01_normal_situation(self, mock_datetime, mock_path, mock_mkdir):
        result = os.path.join(
            os.path.join(CURRENT_DIRECTORY, "program"),
            "2020_02_10-00h_00m_00s_dynamic_ga")

        config = ConfigParser("")
        config.config = {"metadata": {
            "project_output": CURRENT_DIRECTORY, "project_name": "program"}}
        config.methodology = "dynamic_ga"
        config.user_project = Mock()

        mock_datetime.now = Mock(return_value=date(2020, 2, 10))
        mock_path.Path = Mock(return_value=pathlib.Path(""))
        mock_mkdir.mkdir = Mock(return_value=None)

        config.create_output_folder()

        config.user_project.set_output_directory.assert_called_once_with(result)


if __name__ == '__main__':
    unittest.main()
