from setup_test import *

from src.constraint_solver.worst_path import worst_path_match

class Test_worst_path_match(unittest.TestCase):

    #VC-463
    def test_01_first_program(self):
        intermediate_values = Mock()
        intermediate_values.get_number_executions_worst_path.return_value = 419.0
        intermediate_values.get_all_worst_path_basic_block.return_value = {'BubbleSort': [('block0', 1),
                                                                                          ('block1', 11),
                                                                                          ('block2', 11),
                                                                                          ('block3', 66),
                                                                                          ('block4', 66),
                                                                                          ('block5', 11),
                                                                                          ('block6', 55),
                                                                                          ('block7', 55),
                                                                                          ('block8', 55),
                                                                                          ('block9', 55),
                                                                                          ('block10', 11),
                                                                                          ('block11', 1),
                                                                                          ('block12', 10),
                                                                                          ('block13', 10),
                                                                                          ('block14', 1)]}

        coverage_code = {'BubbleSort': {'block0': 1,
                                        'block1': 7,
                                        'block2': 7,
                                        'block3': 49,
                                        'block4': 49,
                                        'block6': 42,
                                        'block8': 42,
                                        'block9': 42,
                                        'block7': 23,
                                        'block5': 7,
                                        'block10': 7,
                                        'block12': 6,
                                        'block13': 6,
                                        'block11': 1,
                                        'block14': 1}}

        self.assertAlmostEqual(worst_path_match(intermediate_values, coverage_code), 0.6921241)

    #VC-464
    def test_02_null_executions(self):
        intermediate_values = Mock()
        intermediate_values.get_number_executions_worst_path.return_value = 419.0
        intermediate_values.get_all_worst_path_basic_block.return_value = {'BubbleSort': [('block0', 1),
                                                                                          ('block1', 11),
                                                                                          ('block2', 11),
                                                                                          ('block3', 66),
                                                                                          ('block4', 66),
                                                                                          ('block5', 11),
                                                                                          ('block6', 55),
                                                                                          ('block7', 55),
                                                                                          ('block8', 55),
                                                                                          ('block9', 55),
                                                                                          ('block10', 11),
                                                                                          ('block11', 1),
                                                                                          ('block12', 10),
                                                                                          ('block13', 10),
                                                                                          ('block14', 1)]}

        coverage_code = {'BubbleSort': {}}

        self.assertAlmostEqual(worst_path_match(intermediate_values, coverage_code), 0.0)

    #VC-465
    def test_03_all_match(self):
        intermediate_values = Mock()
        intermediate_values.get_number_executions_worst_path.return_value = 419.0
        intermediate_values.get_all_worst_path_basic_block.return_value = {'BubbleSort': [('block0', 1),
                                                                                          ('block1', 11),
                                                                                          ('block2', 11),
                                                                                          ('block3', 66),
                                                                                          ('block4', 66),
                                                                                          ('block5', 11),
                                                                                          ('block6', 55),
                                                                                          ('block7', 55),
                                                                                          ('block8', 55),
                                                                                          ('block9', 55),
                                                                                          ('block10', 11),
                                                                                          ('block11', 1),
                                                                                          ('block12', 10),
                                                                                          ('block13', 10),
                                                                                          ('block14', 1)]}

        coverage_code = {'BubbleSort': {'block0': 1,
                                        'block1': 11,
                                        'block2': 11,
                                        'block3': 66,
                                        'block4': 66,
                                        'block6': 55,
                                        'block8': 55,
                                        'block9': 55,
                                        'block7': 55,
                                        'block5': 11,
                                        'block10': 11,
                                        'block12': 10,
                                        'block13': 10,
                                        'block11': 1,
                                        'block14': 1}}

        self.assertAlmostEqual(worst_path_match(intermediate_values, coverage_code), 1.0)

    #VC-466
    def test_04_more_than_100_percent(self):
        intermediate_values = Mock()
        intermediate_values.get_number_executions_worst_path.return_value = 419.0
        intermediate_values.get_all_worst_path_basic_block.return_value = {'BubbleSort': [('block0', 1),
                                                                                          ('block1', 11),
                                                                                          ('block2', 11),
                                                                                          ('block3', 66),
                                                                                          ('block4', 66),
                                                                                          ('block5', 11),
                                                                                          ('block6', 55),
                                                                                          ('block7', 55),
                                                                                          ('block8', 55),
                                                                                          ('block9', 55),
                                                                                          ('block10', 11),
                                                                                          ('block11', 1),
                                                                                          ('block12', 10),
                                                                                          ('block13', 10),
                                                                                          ('block14', 1)]}

        coverage_code = {'BubbleSort': {'block0': 1,
                                        'block1': 11,
                                        'block2': 11,
                                        'block3': 66,
                                        'block4': 66,
                                        'block6': 60,
                                        'block8': 60,
                                        'block9': 60,
                                        'block7': 60,
                                        'block5': 11,
                                        'block10': 11,
                                        'block12': 10,
                                        'block13': 10,
                                        'block11': 1,
                                        'block14': 1}}

        self.assertAlmostEqual(worst_path_match(intermediate_values, coverage_code), 1.047732696)




if __name__ == '__main__':
    unittest.main()