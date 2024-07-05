from setup_test import *

from src.inputs.input_manager import *
from src.inputs.generators import *


class Test_RandomInputGenerator(unittest.TestCase):
    def setUp(self):
        self.project = Mock()
        self.project.input_types = ["int", "float", "int(10)"]
        self.project.input_bounds_min = [1, 0.0, -1]
        self.project.input_bounds_max = [10, 1.0, 100]
        self.project.input_n_test_cases = 5
        self.inter_values = Mock()
        self.manager = InputManager(self.project, self.inter_values)

    #VC-452
    def test_01_run(self):
        generator = RandomInputGenerator(
            self.manager.variables, self.manager.test_cases)
        test_cases_list = generator.run()
        self.assertEqual(len(test_cases_list), 5)
        for elem in test_cases_list:
            self.assertIsInstance(elem, list)
            self.assertEqual(len(elem), 3)
            self.assertIsInstance(elem[0], int)
            self.assertIsInstance(elem[1], float)
            self.assertIsInstance(elem[2], list)
            self.assertEqual(len(elem[2]), 10)
            for item in elem[2]:
                self.assertIsInstance(item, int)
                self.assertTrue(-1 <= item <= 100)

    #VC-453
    def test_02_generate_random_type_int(self):
        generator = RandomInputGenerator(
            self.manager.variables, self.manager.test_cases)
        random_value = generator.generate_random_type("int", 1, 10, 1)
        self.assertIsInstance(random_value, list)
        self.assertTrue(len(random_value) == 1)
        self.assertTrue(1 <= random_value[0] <= 10)

    #VC-454
    def test_03_generate_random_type_float(self):
        generator = RandomInputGenerator(
            self.manager.variables, self.manager.test_cases)
        random_value = generator.generate_random_type("float", 0.0, 1.0, 1)
        self.assertIsInstance(random_value, list)
        self.assertTrue(len(random_value) == 1)
        self.assertTrue(0.0 <= random_value[0] <= 1.0)

    #VC-455
    def test_04_generate_random_type_int_array(self):
        generator = RandomInputGenerator(
            self.manager.variables, self.manager.test_cases)
        random_value = generator.generate_random_type("int", -1, 100, 10)
        self.assertIsInstance(random_value, list)
        self.assertTrue(len(random_value) == 10)
        for elem in random_value:
            self.assertTrue(-1 <= elem <= 100)



class Test_CBMCInputGenerator(unittest.TestCase):
    def setUp(self):
        self.project = Mock()
        self.project.input_directory = "/home/maria/documents/"
        self.project.main_file_name = "program"
        self.project.cbmc_path = "/usr/bin/"
        self.project.input_n_test_cases = 5
        self.inter_values = Mock()
        self.manager = InputManager(self.project, self.inter_values)

    #VC-456
    def test_01_constructor(self, mock_process):
        generator = CBMCInputGenerator(self.project)
        self.assertEqual(generator.file, "/home/maria/documents/program_cbmc.c")
        self.assertEqual(generator.cbmc_path, "/usr/bin/")
        
    #VC-457
    @patch('src.inputs.generators.subprocess')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_02_run(self, mock_stdout, mock_process):
        generator = CBMCInputGenerator(self.project)
        mock_process = Mock()
        mock_process.returncode.return_value = 0
        test_cases_list = generator.run()
        self.assertEqual(mock_stdout.getvalue(),
                         "Running /usr/bin/cbmc /home/maria/documents/program_cbmc.c --cover location --show-test-suite --unwind 10 --json-ui\n")
        





class Test_Variable(unittest.TestCase):

    #VC-458
    def test_01_variable_set_type_array(self):
        var = Variable("int(10)")
        self.assertTrue(var.array)
        self.assertEqual(var.type, "int")
        self.assertEqual(var.size, 10)

    #VC-459
    def test_02_variable_set_bounds(self):
        var = Variable("int")
        var.set_bounds(1, 10)
        self.assertEqual(var.min_value, 1)
        self.assertEqual(var.max_value, 10)
        self.assertFalse(var.array)

    #VC-460
    def test_03_variable_set_bounds(self):
        var = Variable("int")
        with self.assertRaises(SystemExit):
            var.set_bounds([1], [10])

    #VC-461
    def test_04_variable_set_bounds(self):
        var = Variable("int")
        with self.assertRaises(SystemExit):
            var.set_bounds(1.1, 2)

    #VC-462
    def test_08_variable_check_type_unk(self):
        var = Variable("unk")
        with self.assertRaises(SystemExit):
            self.assertTrue(var.check_type())









if __name__ == '__main__':
    unittest.main()