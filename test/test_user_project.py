from setup_test import *

from src.utils.user_project import UserProject


class Test_UserProject(unittest.TestCase):

    #VC-224
    def test_01_constructor_default_parameters(self):
        user_project = UserProject(
                                    "program",
                                    CURRENT_DIRECTORY + "input",
                                    CURRENT_DIRECTORY + "output",
                                    "avr",
                                    "atmel",
                                    "none",
                                    "atmega328")
        
        self.assertEqual(user_project.get_main_file_name(), "program")
        self.assertEqual(user_project.get_input_directory(), join(CURRENT_DIRECTORY + "input", ''))
        self.assertEqual(user_project.get_output_directory(), join(CURRENT_DIRECTORY + "output", ''))
        self.assertEqual(user_project.get_architecture(), "avr")
        self.assertEqual(user_project.get_vendor(), "atmel")
        self.assertEqual(user_project.get_operational_system(), "none")
        self.assertEqual(user_project.get_microcontroller_unit(), "atmega328")
        self.assertEqual(user_project.get_function_target(), "main")
        self.assertEqual(user_project.get_report_format(), ["pdf"])
        self.assertEqual(user_project.get_deadline(), 0.0)
        self.assertEqual(user_project.get_llvm_path(), "")
        self.assertEqual(user_project.get_cbmc_path(), "")
        self.assertEqual(user_project.get_board(), None)
        self.assertEqual(user_project.get_serial_port(), "")
        self.assertEqual(user_project.get_flash_board(), False)
        self.assertEqual(user_project.get_chosen_input(), [])
        self.assertEqual(user_project.get_input_types(), [])
        self.assertEqual(user_project.get_input_bounds_min(), [])
        self.assertEqual(user_project.get_input_bounds_max(), [])
        self.assertEqual(user_project.get_input_gen_method(), "")
        self.assertEqual(user_project.get_input_n_test_cases(), 0)
        self.assertEqual(user_project.get_number_exec(), 10000)
        self.assertEqual(user_project.get_pwcet_bounds(), [1E-9, 1E-10, 1E-11, 1E-12])
        self.assertEqual(user_project.get_parent_selection_type(), "sss")
        self.assertEqual(user_project.get_crossover_type(), "two_points")
        self.assertEqual(user_project.get_mutation_type(), "adaptive")
        self.assertEqual(user_project.get_mutation_percent_genes(), [70,15])
        self.assertEqual(user_project.get_stop_criteria(), True)


    #VC-225
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_02_str_function(self, mock_stdout):
        user_project = UserProject(
                            "program",
                            CURRENT_DIRECTORY + "input",
                            CURRENT_DIRECTORY + "output",
                            "avr",
                            "atmel",
                            "none",
                            "atmega328",
                            "fatorial",
                            ["pdf"],
                            500.0)
        
        print(user_project)
        self.assertEqual(mock_stdout.getvalue(),
                         "*** Project informations ***\nMain file name: program" + \
                         "\nFunction target: fatorial" + \
                         "\nDirectory of project: " + join(CURRENT_DIRECTORY + "input",'') + \
                         "\nDirectory of output: " + join(CURRENT_DIRECTORY + "output",'') + \
                         "\nDeadline: 500.0" + \
                         "\n\n*** Target informations ***\nArchitecture: avr" + \
                         "\nVendor: atmel" + \
                         "\nOperational system: none" + \
                         "\nMicrocontroller unit: atmega328\n")

    #VC-226
    def test_03_board_true(self):
        user_project = UserProject("","","","","","","")
        user_project.set_target(True, "", False)
        self.assertEqual(user_project.get_env_name(), "board")
    
    #VC-227
    def test_04_board_false(self):
        user_project = UserProject("","","","","","","")
        user_project.set_target(False, "", False)
        self.assertEqual(user_project.get_env_name(), "simul")

    #VC-228
    def test_05_constructor_setup_all_arguments(self):
        user_project = UserProject(
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "fatorial",
                                    ["html"],
                                    150)
        user_project.set_input_directory(CURRENT_DIRECTORY + "input")
        user_project.set_output_directory(CURRENT_DIRECTORY + "output")
        user_project.set_external_libs(CURRENT_DIRECTORY + "llvm", CURRENT_DIRECTORY + "cbmc")
        user_project.set_target(True, "COM2", True)
        user_project.set_inputs([2, 3], [int, float], [0], [10], "random", 33)
        user_project.set_evt(50000, [1E-27])
        user_project.set_ga("sus", "scattered", "inversion", [30], False)
        
        self.assertEqual(user_project.get_main_file_name(), "")
        self.assertEqual(user_project.get_input_directory(), join(CURRENT_DIRECTORY + "input", ''))
        self.assertEqual(user_project.get_output_directory(), join(CURRENT_DIRECTORY + "output", ''))
        self.assertEqual(user_project.get_architecture(), "")
        self.assertEqual(user_project.get_vendor(), "")
        self.assertEqual(user_project.get_operational_system(), "")
        self.assertEqual(user_project.get_microcontroller_unit(), "")
        self.assertEqual(user_project.get_function_target(), "fatorial")
        self.assertEqual(user_project.get_report_format(), ["html"])
        self.assertEqual(user_project.get_deadline(), 150)
        self.assertEqual(user_project.get_llvm_path(), join(CURRENT_DIRECTORY + "llvm", ''))
        self.assertEqual(user_project.get_cbmc_path(), join(CURRENT_DIRECTORY + "cbmc", ''))
        self.assertEqual(user_project.get_board(), True)
        self.assertEqual(user_project.get_serial_port(), "COM2")
        self.assertEqual(user_project.get_flash_board(), True)
        self.assertEqual(user_project.get_chosen_input(), [2, 3])
        self.assertEqual(user_project.get_input_types(), [int, float])
        self.assertEqual(user_project.get_input_bounds_min(), [0])
        self.assertEqual(user_project.get_input_bounds_max(), [10])
        self.assertEqual(user_project.get_input_gen_method(), "random")
        self.assertEqual(user_project.get_input_n_test_cases(), 33)
        self.assertEqual(user_project.get_number_exec(), 50000)
        self.assertEqual(user_project.get_pwcet_bounds(), [1E-27])
        self.assertEqual(user_project.get_parent_selection_type(), "sus")
        self.assertEqual(user_project.get_crossover_type(), "scattered")
        self.assertEqual(user_project.get_mutation_type(), "inversion")
        self.assertEqual(user_project.get_mutation_percent_genes(), [30])
        self.assertEqual(user_project.get_stop_criteria(), False)
    

    def test_06_filename_with_extension(self):
        user_project = UserProject("mergesort.c", "", "", "", "", "", "")
        self.assertEqual(user_project.get_main_file_name(), "mergesort")
    

    def test_07_filename_with_dot(self):
        user_project = UserProject("dot_product.release.c", "", "", "", "", "", "")
        self.assertEqual(user_project.get_main_file_name(), "dot_product")
    

    def test_08_directory_without_end_bar(self):
        if 'win' in sys.platform:
            user_project = UserProject("", "C:\\Users\\1Peter\\Desktop", "C:\\Users\\2Peter\\Desktop", "", "", "", "")
            self.assertEqual(user_project.get_input_directory(), "C:\\Users\\1Peter\\Desktop\\")
            self.assertEqual(user_project.get_output_directory(), "C:\\Users\\2Peter\\Desktop\\")
        else:
            user_project = UserProject("", "/home/1maria/Documents", "/home/2maria/Documents", "", "", "", "")
            self.assertEqual(user_project.get_input_directory(), "/home/1maria/Documents/")
            self.assertEqual(user_project.get_output_directory(), "/home/2maria/Documents/")
    

    def test_09_directory_with_space(self):
        if 'win' in sys.platform:
            user_project = UserProject("", "C:\\Users\\1Peter Truman\\Desktop", "C:\\Users\\2Peter Truman\\Desktop", "", "", "", "")
            self.assertEqual(user_project.get_input_directory(), "C:\\Users\\1Peter Truman\\Desktop\\")
            self.assertEqual(user_project.get_output_directory(), "C:\\Users\\2Peter Truman\\Desktop\\")
        else:
            user_project = UserProject("", "/home/1maria flower/Documents", "/home/2maria flower/Documents", "", "", "", "")
            self.assertEqual(user_project.get_input_directory(), "/home/1maria flower/Documents/")
            self.assertEqual(user_project.get_output_directory(), "/home/2maria flower/Documents/")
    

    def test_10_none_external_libs(self):
        user_project = UserProject("", "", "", "", "", "", "")
        user_project.set_external_libs(None, None)
        self.assertEqual(user_project.get_llvm_path(), "")
        self.assertEqual(user_project.get_cbmc_path(), "")


    def test_11_external_libs_without_end_bar(self):
        if 'win' in sys.platform:
            user_project = UserProject("", "", "", "", "", "", "")
            user_project.set_external_libs("C:\\Users\\Documents", "C:\\Users\\Desktop")
            self.assertEqual(user_project.get_llvm_path(), "C:\\Users\\Documents\\")
            self.assertEqual(user_project.get_cbmc_path(), "C:\\Users\\Desktop\\")
        else:
            user_project = UserProject("", "", "", "", "", "", "")
            user_project.set_external_libs("/usr/lib/llvm-16", "/usr/bin")
            self.assertEqual(user_project.get_llvm_path(), "/usr/lib/llvm-16/")
            self.assertEqual(user_project.get_cbmc_path(), "/usr/bin/")
    

    def test_12_triple_target(self):
        user_project = UserProject("", "", "", "avr", "atmel", "none", "")
        self.assertEqual(user_project.get_triple_target(), "avr-atmel-none")

        
    


if __name__ == '__main__':
    unittest.main()