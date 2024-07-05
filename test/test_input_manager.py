from setup_test import *

from inputs.input_manager import *
from inputs.generators import *


class TestRandomInputGenerator(unittest.TestCase):
    def setUp(self):
        self.project = Mock()
        self.inter_values = Mock()
        self.project.input_types = ["int", "float", "int(10)"]
        self.project.input_bounds_min = [1, 0.0, -1]
        self.project.input_bounds_max = [10, 1.0, 100]
        self.project.input_n_test_cases = 5

    # LLR-93
    # VC-375
    def test_01_init(self):
        manager = InputManager(self.project, self.inter_values)

        variables = manager.get_variables()

        for var in variables:
            self.assertIsInstance(var, Variable)

        self.assertEqual(variables[0].type, 'int')
        self.assertEqual(variables[1].type, 'float')
        self.assertEqual(variables[2].type, 'int')

        self.assertEqual(variables[0].size,  1)
        self.assertEqual(variables[1].size, 1)
        self.assertEqual(variables[2].size, 10)

        self.assertEqual(variables[0].min_value,  1)
        self.assertEqual(variables[1].min_value, 0.0)
        self.assertEqual(variables[2].min_value, -1)

        self.assertEqual(variables[0].max_value,  10)
        self.assertEqual(variables[1].max_value, 1.0)
        self.assertEqual(variables[2].max_value, 100)

    # LLR-94
    # VC-376
    def test_02_generator(self):
        self.project.input_gen_method = "random"
        manager = InputManager(self.project, self.inter_values)

        self.assertIsInstance(manager.generator, RandomInputGenerator)

    # LLR-94
    # VC-377
    def test_03_generator(self):
        self.project.input_gen_method = "cbmc"
        self.project.input_directory = "inputs"
        self.project.main_file_name = "test"
        manager = InputManager(self.project, self.inter_values)

        self.assertIsInstance(manager.generator, CBMCInputGenerator)

    # LLR-94
    #VC-378
    def test_04_generator(self):
        self.project.input_gen_method = "none"
        manager = InputManager(self.project, self.inter_values)

        self.assertEqual(manager.generator, False)

    # LLR-95
    #VC-379
    def test_05_generate_inputs(self):
        manager = InputManager(self.project, self.inter_values)

        manager.generator = Mock()
        manager.generator.run.return_value = [[1, 2, 3], [5, 4, 3]]

        result = manager.generate_inputs()

        self.assertEqual(result,
                         [[1, 2, 3], [5, 4, 3]])

    # LLR-97
    # VC-380
    def test_06_random_input_init(self):
        manager = InputManager(self.project, self.inter_values)

        generator = RandomInputGenerator(
            manager.variables, self.project.input_n_test_cases)

        self.assertIsInstance(generator.rng, np.random.Generator)

    # LLR-98
    # VC-381
    def test_07_generate_random_type_int(self):
        manager = InputManager(self.project, self.inter_values)

        generator = RandomInputGenerator(
            manager.variables, self.project.input_n_test_cases)

        random_value = generator.generate_random_type("int", 1, 10, 1)
        self.assertIsInstance(random_value, list)
        self.assertTrue(len(random_value) == 1)
        self.assertTrue(1 <= random_value[0] <= 10)

    # LLR-98
    # VC-382
    def test_08_generate_random_type_float(self):
        manager = InputManager(self.project, self.inter_values)

        generator = RandomInputGenerator(
            manager.variables, self.project.input_n_test_cases)
        random_value = generator.generate_random_type("float", 0.0, 1.0, 1)
        self.assertIsInstance(random_value, list)
        self.assertTrue(len(random_value) == 1)
        self.assertTrue(0.0 <= random_value[0] <= 1.0)

    # LLR-98
    # VC-383
    def test_09_generate_random_type_int_array(self):
        manager = InputManager(self.project, self.inter_values)

        generator = RandomInputGenerator(
            manager.variables, self.project.input_n_test_cases)
        random_value = generator.generate_random_type("int", -1, 100, 10)
        self.assertIsInstance(random_value, list)
        self.assertTrue(len(random_value) == 10)
        for elem in random_value:
            self.assertTrue(-1 <= elem <= 100)

    # def test_variable_set_type_array(self):
    #     var = Variable("int array[10]")
    #     self.assertTrue(var.array)
    #     self.assertEqual(var.type, "int")
    #     self.assertEqual(var.size, 10)

    # def test_variable_set_bounds(self):
    #     var = Variable("int")
    #     var.set_bounds(1, 10)
    #     self.assertEqual(var.min_value, 1)
    #     self.assertEqual(var.max_value, 10)
    #     self.assertFalse(var.array)

    # def test_variable_expand_bounds(self):
    #     var = Variable("int array[5]")
    #     var.set_bounds([1], [10])
    #     self.assertEqual(var.min_value, [1, 1, 1, 1, 1])
    #     self.assertEqual(var.max_value, [10, 10, 10, 10, 10])

    # def test_variable_check_bounds(self):
    #     var = Variable("int array[5]")
    #     with self.assertRaises(SystemExit):
    #         var.set_bounds(1, 10)

    # def test_variable_check_bounds(self):
    #     var = Variable("int")
    #     with self.assertRaises(SystemExit):
    #         var.set_bounds([1], [10])

    # def test_variable_check_bounds(self):
    #     var = Variable("int")
    #     with self.assertRaises(SystemExit):
    #         var.set_bounds(1.1, 2)

    # def test_variable_check_type_int(self):
    #     var = Variable("int")
    #     self.assertTrue(var.check_type())

    # def test_variable_check_type_float(self):
    #     var = Variable("float")
    #     self.assertTrue(var.check_type())

    # def test_variable_check_type_unk(self):
    #     var = Variable("unk")
    #     with self.assertRaises(SystemExit):
    #         self.assertTrue(var.check_type())


if __name__ == '__main__':
    unittest.main()
