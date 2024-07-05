from setup_test import *

from src.cfg.graph_weight import define_instructions_weight, update_basic_block_weight_statically, update_weight_by_measurements
from src.utils.user_project import UserProject
from src.cfg.timeMeter import TimeMeter


class Test_define_instructions_weight(unittest.TestCase):

    # VC-149
    def test_01_avr(self):
        project = Mock()
        project.get_architecture.return_value = 'avr'

        result = {'call llvm.dbg.declare': 0, 'llvm.dbg.value': 0, 'call llvm.dbg.assign': 0, 'asm': 1,
                  'add': 14, 'alloca': 55, 'and': 10, 'ashr': 8, 'bitcast': 8, 'br': 23,
                  'call': 6, 'extractelement': 47, 'extractvalue': 39, 'fadd': 1085,
                  'fcmp': 16, 'fdiv': 819, 'fmul': 917, 'fpext': 18, 'fptosi': 417,
                  'fptoui': 1512, 'fptrunc': 18, 'frem': 823, 'fsub': 1123, 'getelementptr': 8,
                  'icmp': 24, 'indirectbr': 0, 'insertelement': 118, 'insertvalue': 93,
                  'inttoptr': 8, 'invoke': 0, 'load': 20, 'lshr': 8, 'mul': 25, 'or': 9,
                  'phi': 0, 'ptrtoint': 8, 'ret': 8, 'sdiv': 75, 'select': 8, 'sext': 8,
                  'shl': 8, 'shufflevector': 0, 'sitofp': 616, 'srem': 78, 'store': 18,
                  'sub': 14, 'switch': 75, 'trunc': 8, 'udiv': 46, 'uitofp': 652, 'unreachable': 0,
                  'unwind': 0, 'urem': 41, 'va_arg': 0, 'xor': 12, 'zext': 8}

        self.assertDictEqual(define_instructions_weight(project), result)

    # VC-150
    def test_02_weight_obtained_by_measurements(self):
        project = Mock()
        project.get_architecture.return_value = "my_invented_processor"

        self.assertEqual(define_instructions_weight(project), {})

    # def test_03_x86_64(self):
    #     project = Mock()
    #     project.get_architecture.return_value = 'x86_64'

    #     result = {'call llvm.dbg.declare': 0, 'llvm.dbg.value': 0, 'call llvm.dbg.assign': 0, 'asm': 1,
    #             'add': , 'alloca': , 'and': , 'ashr': , 'bitcast': , 'br': ,
    #             'call': , 'extractelement': , 'extractvalue': , 'fadd': ,
    #             'fcmp': , 'fdiv': , 'fmul': , 'fpext': , 'fptosi': ,
    #             'fptoui': , 'fptrunc': , 'frem': , 'fsub': , 'getelementptr': ,
    #             'icmp': , 'indirectbr': , 'insertelement': , 'insertvalue': ,
    #             'inttoptr': , 'invoke': , 'load': , 'lshr': , 'mul': , 'or': ,
    #             'phi': 0, 'ptrtoint': , 'ret': , 'sdiv': , 'select': , 'sext': ,
    #             'shl': , 'shufflevector': , 'sitofp': , 'srem': , 'store': ,
    #             'sub': , 'switch': , 'trunc': , 'udiv': , 'uitofp': , 'unreachable': ,
    #             'unwind': , 'urem': , 'va_arg': , 'xor': , 'zext': }

    #     self.assertDictEqual(define_instructions_weight(project), result)


STANDARD_WEIGHT = {
    'call llvm.dbg.declare': 0, 'llvm.dbg.value': 0, 'call llvm.dbg.assign': 0,
    'add': 14, 'alloca': 55, 'and': 10, 'ashr': 8, 'bitcast': 8, 'br': 23,
    'call': 6, 'extractelement': 47, 'extractvalue': 39, 'fadd': 1085, 'fcmp':
    16, 'fdiv': 819, 'fmul': 917, 'fpext': 18, 'fptosi': 417, 'fptoui': 1512,
    'fptrunc': 18, 'frem': 823, 'fsub': 1123, 'getelementptr': 8, 'icmp': 24,
    'indirectbr': 0, 'insertelement': 118, 'insertvalue': 93, 'inttoptr': 8,
    'invoke': 0, 'load': 20, 'lshr': 8, 'mul': 25, 'or': 9, 'phi': 0,
    'ptrtoint': 8, 'ret': 8, 'sdiv': 75, 'select': 8, 'sext': 8, 'shl': 8,
    'shufflevector': 0, 'sitofp': 616, 'srem': 78, 'store': 18, 'sub': 14,
    'switch': 75, 'trunc': 8, 'udiv': 46, 'uitofp': 652, 'unreachable': 0,
    'unwind': 0, 'urem': 41, 'va_arg': 0, 'xor': 12, 'zext': 8}


class Test_update_basic_block_weight_statically(unittest.TestCase):

    # VC-151
    def test_01_one_instruction(self):
        function = [create_bb(472, '', 0, 1, ['ret'], [])]
        result = [8]

        update_basic_block_weight_statically(function, STANDARD_WEIGHT)

        for index, basic_block in enumerate(function):
            with self.subTest(msg="Error in Basic block: " + str(index)):
                self.assertEqual(basic_block.get_weight(), result[index])

    # VC-152
    def test_02_zero_instructions(self):
        function = [create_bb(472, '', 0, 1, [], [])]
        result = [0]

        update_basic_block_weight_statically(function, STANDARD_WEIGHT)

        for index, basic_block in enumerate(function):
            with self.subTest(msg="Error in Basic block: " + str(index)):
                self.assertEqual(basic_block.get_weight(), result[index])

    # VC-153
    def test_03_one_block_multiple_instructions(self):
        function = [create_bb(119, '', 0, 1, [
                    'alloca', 'call', 'getelementptr', 'call',
                    'getelementptr', 'load', 'sext', 'sdiv', 'ret'], [])]
        result = [194]

        update_basic_block_weight_statically(function, STANDARD_WEIGHT)

        for index, basic_block in enumerate(function):
            with self.subTest(msg="Error in Basic block: " + str(index)):
                self.assertEqual(basic_block.get_weight(), result[index])

    # VC-154
    def test_04_multiple_blocks_multiple_instructions(self):
        function = [
            create_bb(208, '12', 0, 0, ['store', 'br'],
                      [2]),
            create_bb(
                212, '13', 0, 0,
                ['store', 'store', 'load', 'load', 'icmp', 'br'],
                [3, 7]),
            create_bb(220, '17', 0, 0, ['br'],
                      [4]),
            create_bb(
                223, '18', 0, 0,
                ['load', 'load', 'sext', 'getelementptr', 'load', 'load', 'add',
                 'store', 'load', 'add', 'store', 'br'],
                [5]),
            create_bb(
                237, '28', 0, 50, ['load', 'load', 'icmp', 'br'],
                [4, 6])]
        result = [41, 123, 23, 203, 87]

        update_basic_block_weight_statically(function, STANDARD_WEIGHT)

        for index, basic_block in enumerate(function):
            with self.subTest(msg="Error in Basic block: " + str(index)):
                self.assertEqual(basic_block.get_weight(), result[index])

    # VC-155
    def test_05_sum_all_null_instructions(self):
        function = [
            create_bb(
                1, '', 1, 1,
                ['call llvm.dbg.declare', 'llvm.dbg.value',
                 'call llvm.dbg.assign', 'phi'],
                [1])]
        architectures = ['avr', 'x86_64']
        project = Mock()

        for architecture in architectures:

            # It's possible change the return value dynamically
            project.get_architecture.return_value = architecture

            # Test the same instrunctions for each architecture
            with self.subTest(msg="Error in architecture: " + architecture):
                update_basic_block_weight_statically(
                    function, define_instructions_weight(project))
                self.assertEqual(function[0].get_weight(), 0)


class Test_update_weight_by_measurements(unittest.TestCase):

    # VC-156
    def test_01_one_block(self):
        graph = {}
        graph["fat"] = [create_bb(5, '#;fat;block0', 0, 1, ['ret'], [])]

        timer = Mock()
        timer.final_times = {'fat': {"block0": 50}}
        update_weight_by_measurements(graph, timer)

        self.assertEqual(graph["fat"][0].get_weight(), 50)

    # VC-157
    def test_02_without_hash(self):
        graph = {}
        graph["fat"] = [create_bb(5, ';fat;block0', 0, 1, ['ret'], [])]

        timer = Mock()
        timer.final_times = {'fat': {"block0": 50}}
        update_weight_by_measurements(graph, timer)

        self.assertEqual(graph["fat"][0].get_weight(), 0)

    # VC-158
    def test_03_without_semicolon(self):
        graph = {}
        graph["fat"] = [create_bb(5, '#fatblock0', 0, 1, ['ret'], [])]

        timer = Mock()
        timer.final_times = {'fat': {"block0": 70}}

        with self.assertRaises(ValueError):
            update_weight_by_measurements(graph, timer)

    # VC-159
    def test_04_two_blocks(self):
        graph = {}
        graph["fat"] = [create_bb(5, '#;fat;block0', 0, 0, ['and', 'br'], [
                                  1]), create_bb(7, '#;fat;block1', 0, 1, ['ret'], [])]

        timer = Mock()
        timer.final_times = {'fat': {"block0": 30, "block1": 80}}
        update_weight_by_measurements(graph, timer)

        self.assertEqual(graph["fat"][0].get_weight(), 30)
        self.assertEqual(graph["fat"][1].get_weight(), 80)

    # VC-160
    def test_05_two_functions(self):
        graph = {}
        graph["fat"] = [create_bb(1, '#;fat;block0', 0, 1, ['ret'], [])]
        graph["dot"] = [create_bb(5, '#;dot;block0', 0, 1, [
                                  'call fat', 'ret'], [])]

        timer = Mock()
        timer.final_times = {'fat': {"block0": 30}, 'dot': {"block0": 40}}
        update_weight_by_measurements(graph, timer)

        self.assertEqual(graph["fat"][0].get_weight(), 30)
        self.assertEqual(graph["dot"][0].get_weight(), 40)

    # VC-161
    def test_06_main_function_default_argument(self):
        graph = {}
        graph["main"] = [create_bb(5, '#;main;block0', 0, 1, ['ret'], [])]

        timer = Mock()
        timer.final_times = {'main': {"block0": 110}}
        update_weight_by_measurements(graph, timer)

        self.assertEqual(graph["main"][0].get_weight(), 110)

    # VC-162
    def test_07_main_function_true_argument(self):
        graph = {}
        graph["main"] = [create_bb(5, '#;main;block0', 0, 1, ['ret'], [])]

        timer = Mock()
        timer.final_times = {'main': {"block0": 110}}
        update_weight_by_measurements(graph, timer, True)

        self.assertEqual(graph["main"][0].get_weight(), 110)

    # VC-163
    def test_08_main_function_false_argument(self):
        graph = {}
        graph["main"] = [create_bb(5, '#;main;block0', 0, 1, ['ret'], [])]

        timer = Mock()
        timer.final_times = {'main': {"block0": 110}}
        update_weight_by_measurements(graph, timer, False)

        self.assertEqual(graph["main"][0].get_weight(), 0)

    # VC-164
    def test_09_main_function_and_other_functions(self):
        graph = {}
        graph["first"] = [create_bb(1, '#;first;block0', 0, 1, ['ret'], [])]
        graph["main"] = [create_bb(2, '#;main;block0', 0, 1, [
                                   'call first', 'ret'], [])]
        graph["second"] = [create_bb(3, '#;second;block0', 0, 1, [
                                     'call main', 'ret'], [])]

        timer = Mock()
        timer.final_times = {
            'main': {"block0": 20},
            'first': {"block0": 10},
            'second': {"block0": 30}}
        update_weight_by_measurements(graph, timer, False)

        self.assertEqual(graph["first"][0].get_weight(), 10)
        self.assertEqual(graph["main"][0].get_weight(), 0)
        self.assertEqual(graph["second"][0].get_weight(), 30)

    # VC-366
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_10_coverage_warning(self, mock_stdout):
        graph = {}
        graph["first"] = [create_bb(1, '#;first;block0', 0, 1, ['ret'], []), create_bb(
            1, '#;first;block1', 0, 1, ['ret'], []), create_bb(1, '#;first;block2', 0, 1, ['ret'], [])]
        graph["main"] = [create_bb(2, '#;main;block0', 0, 1, [
                                   'call first', 'ret'], [])]

        timer = Mock()
        timer.final_times = {
            'main': {"block0": 20},
            'first': {"block0": 10, "block1": 20}}
        cov = 2/3
        update_weight_by_measurements(graph, timer, False)

        self.assertEqual(mock_stdout.getvalue(), "\n\33[43mWarning! Block coverage achieved by the test cases was {:.2f}\33[0m\n".format(
            100*cov))

    # VC-368
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_11_coverage_warning(self, mock_stdout):
        graph = {}
        graph["first"] = [create_bb(1, '#;first;block0', 0, 1, ['ret'], []), create_bb(
            1, '#;first;block1', 0, 1, ['ret'], []), create_bb(1, '#;first;block2', 0, 1, ['ret'], [])]
        graph["main"] = [create_bb(2, '#;main;block0', 0, 1, [
                                   'call first', 'ret'], [])]

        timer = Mock()
        timer.final_times = {
            'main': {"block0": 20},
            'first': {"block0": 10, "block1": 20}}
        cov = 3/4
        update_weight_by_measurements(graph, timer)

        self.assertEqual(mock_stdout.getvalue(), "\n\33[43mWarning! Block coverage achieved by the test cases was {:.2f}\33[0m\n".format(
            100*cov))


if __name__ == '__main__':
    unittest.main()
