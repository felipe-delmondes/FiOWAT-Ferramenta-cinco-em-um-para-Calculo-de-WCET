from setup_test import *
from src.ipet.ipet import Ipet
from src.cfg.graph_generator import BasicBlock
from src.utils.intermediate_values import IntermediateValues


# Create class to test, its name is arbitrary. However, the parameter is always "unittest.TestCase"
class Test_run_ipet_static(unittest.TestCase):

    #VC-119
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_01_first_program(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["llvm.va_end"] = []
        graph["__stdio_common_vfscanf"] = []
        graph["__local_stdio_scanf_options"] = [
            create_bb(472, '', 0, 1, ['ret'], [])]
        graph["_vfscanf_l"] = [create_bb(450, '', 0, 1, ['alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'store',
                                         'load', 'load', 'load', 'load', 'call __local_stdio_scanf_options', 'load', 'call __stdio_common_vfscanf', 'ret'], [])]
        graph["__acrt_iob_func"] = []
        graph["llvm.va_start"] = []
        graph["scanf"] = [create_bb(149, '', 0, 1, ['alloca', 'alloca', 'alloca', 'store', 'call llvm.va_start',
                                    'load', 'load', 'call __acrt_iob_func', 'call _vfscanf_l', 'store', 'call llvm.va_end', 'load', 'ret'], [])]
        graph["__stdio_common_vfprintf"] = []
        graph["__local_stdio_printf_options"] = [
            create_bb(421, '', 0, 1, ['ret'], [])]
        graph["_vfprintf_l"] = [create_bb(426, '', 0, 1, ['alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'store',
                                          'load', 'load', 'load', 'load', 'call __local_stdio_printf_options', 'load', 'call __stdio_common_vfprintf', 'ret'], [])]
        graph["printf"] = [create_bb(132, '', 0, 1, ['alloca', 'alloca', 'alloca', 'store', 'call llvm.va_start',
                                     'load', 'load', 'call __acrt_iob_func', 'call _vfprintf_l', 'store', 'call llvm.va_end', 'load', 'ret'], [])]
        graph["calculadora"] = [create_bb(119, '', 0, 1, [
                                          'alloca', 'call printf', 'getelementptr', 'call scanf', 'getelementptr', 'load', 'sext', 'sdiv', 'ret'], [])]
        graph["soma_prefixa"] = [create_bb(193, '', 0, 0, ['alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'load', 'icmp', 'br'], [1, 10]),
                                 create_bb(208, '12', 0, 0, [
                                           'store', 'br'], [2]),
                                 create_bb(212, '13', 0, 0, [
                                           'store', 'store', 'load', 'load', 'icmp', 'br'], [3, 7]),
                                 create_bb(220, '17', 0, 0, ['br'], [4]),
                                 create_bb(223, '18', 0, 0, [
                                           'load', 'load', 'sext', 'getelementptr', 'load', 'load', 'add', 'store', 'load', 'add', 'store', 'br'], [5]),
                                 create_bb(237, '28', 0, 50, [
                                           'load', 'load', 'icmp', 'br'], [4, 6]),
                                 create_bb(243, '32', 0, 0, [
                                           'load', 'load', 'load', 'sext', 'getelementptr', 'store', 'br'], [7]),
                                 create_bb(252, '38', 0, 0, [
                                           'load', 'add', 'store', 'br'], [8]),
                                 create_bb(258, '41', 0, 10, [
                                           'load', 'load', 'icmp', 'br'], [2, 9]),
                                 create_bb(264, '45', 0, 0, ['br'], [10]),
                                 create_bb(267, '46', 0, 1, ['ret'], [])]
        graph["fatorial"] = [create_bb(166, '', 0, 0, ['alloca', 'alloca', 'store', 'load', 'icmp', 'br'], [1, 2]),
                             create_bb(175, '6', 0, 0, ['store', 'br'], [3]),
                             create_bb(179, '7', 0, 0, [
                                       'load', 'load', 'sub', 'call fatorial', 'mul', 'store', 'br'], [3]),
                             create_bb(188, '13', 0, 1, ['load', 'ret'], [])]
        graph["rand"] = []
        graph["srand"] = []
        graph["_time64"] = []
        graph["time"] = [create_bb(
            345, '', 0, 1, ['alloca', 'store', 'load', 'call _time64', 'ret'], [])]
        graph["main"] = [create_bb(271, '', 0, 0, ['alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'load', 'getelementptr', 'load', 'call printf', 'call time', 'trunc', 'call srand', 'store', 'br'], [1]),
                         create_bb(293, '16', 0, 0, [
                                   'load', 'icmp', 'br'], [2, 4]),
                         create_bb(298, '19', 0, 0, ['call rand', 'srem', 'load', 'sext', 'getelementptr',
                                   'store', 'call rand', 'srem', 'load', 'sext', 'getelementptr', 'store', 'br'], [3]),
                         create_bb(313, '30', 0, 20, [
                                   'load', 'add', 'store', 'br'], [1]),
                         create_bb(319, '33', 0, 0, ['store', 'load', 'getelementptr', 'getelementptr',
                                   'call soma_prefixa', 'call calculadora', 'store', 'load', 'icmp', 'br'], [5, 6]),
                         create_bb(331, '40', 0, 0, [
                                   'load', 'call fatorial', 'store', 'br'], [6]),
                         create_bb(337, '43', 0, 1, ['load', 'call printf', 'ret'], [])]

        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_static(), 32474)

    #VC-120
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_02_void_function(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = []
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_static(), 6)

    #VC-121
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_03_recursive_function(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(10, '', 0, 1, ['call main'], [])]
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_static(), 12)

    #VC-122
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_04_read_instruction(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(5, '', 0, 1, [
                                   'alloca', 'br', 'add', 'fdiv', 'getelementptr', 'fmul', 'store', 'load', 'ret'], [])]
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_static(), 1888)

    #VC-123
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_05_simple_conditional(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(145, 'start', 0, 0, ['select', 'trunc', 'br'], [1, 2]), create_bb(150, 'exit_1', 0, 1, [
            'and', 'and', 'and', 'and', 'and', 'ret'], []), create_bb(170, 'pre_exit_2', 0, 0, ['br'], [3]), create_bb(180, 'exit_2', 0, 1, ['fsub', 'ret'], [])]
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_static(), 1199)

    #VC-124
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_06_infeasible_solve(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(145, 'execute_10_times', 0, 10, ['select', 'trunc', 'br'], [
                                   1]), create_bb(180, 'execute_once', 0, 1, ['fsub', 'ret'], [])]
        ipet = Ipet(graph, project)
        with self.assertRaises(SystemExit):
            ipet.run_ipet_static()

    #VC-125
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_07_without_connections_instructions(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(145, 'start', 0, 0, ['and'], [1, 2]), create_bb(150, 'exit_1', 0, 1, ['and'], [
        ]), create_bb(170, 'pre_exit_2', 0, 0, ['and'], [3]), create_bb(180, 'exit_2', 0, 1, ['and'], [])]
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_static(), 36)

    #VC-126
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_08_loop_with_two_entry_points(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(0, '', 0, 0, ['and'], [1]),
                         create_bb(1, '', 0, 0, ['and'], [2, 8]),
                         create_bb(2, '', 0, 0, ['and'], [3, 4]),
                         create_bb(3, '', 0, 0, ['and'], [9]),
                         create_bb(4, '', 0, 0, ['and'], [5, 6]),
                         create_bb(5, '', 0, 0, ['and'], [7]),
                         create_bb(6, '', 0, 0, ['and'], [7]),
                         create_bb(7, '', 0, 15, ['and'], [1]),
                         create_bb(8, '', 0, 0, ['and'], [9]),
                         create_bb(9, '', 0, 1, ['ret'], [])]
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_static(), 804)

    #VC-127
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_09_default_main(self, project, mock_stdout):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "nonexistingfunction"

        graph = {}
        graph["main"] = [create_bb(57, 'block0', 50, 1, ['ret'], [])]
        ipet = Ipet(graph, project)
        ipet.run_ipet_static()

        self.assertEqual(mock_stdout.getvalue(),
        "Starting Static IPET...\nFunction: main --- Otimization complete!\n\33[42mIPET finished.\33[0m\n\33[43mWarning: The function selected by user wasn't found, so the FioWAT selected 'main function'\33[0m\n")

    #VC-128
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_10_stop_second_function(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "second"

        graph = {}
        graph["first"] = [create_bb(1, 'block0', 50, 1, ['ret'], [])]
        graph["second"] = [create_bb(2, 'block1', 50, 1, ['call first', 'ret'], [])]
        graph["main"] = [create_bb(3, 'block2', 1000, 1, ['call second', 'add', 'fmul', 'add', 'ret'], [])]
        ipet = Ipet(graph, project)

        self.assertEqual(ipet.run_ipet_static(), 28)
        self.assertEqual(project.get_function_target.call_count, 2)











######################################################################################################3








class Test_run_ipet_hybrid(unittest.TestCase):

    #VC-129
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_01_first_program(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["llvm.va_end"] = []
        graph["__stdio_common_vfscanf"] = []
        graph["__local_stdio_scanf_options"] = [
            create_bb(472, '', 14, 1, ['ret'], [])]
        graph["_vfscanf_l"] = [create_bb(450, '', 412, 1, ['alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'store',
                                         'load', 'load', 'load', 'load', 'call __local_stdio_scanf_options', 'load', 'call __stdio_common_vfscanf', 'ret'], [])]
        graph["__acrt_iob_func"] = []
        graph["llvm.va_start"] = []
        graph["scanf"] = [create_bb(149, '', 293, 1, ['alloca', 'alloca', 'alloca', 'store', 'call llvm.va_start',
                                    'load', 'load', 'call __acrt_iob_func', 'call _vfscanf_l', 'store', 'call llvm.va_end', 'load', 'ret'], [])]
        graph["__stdio_common_vfprintf"] = []
        graph["__local_stdio_printf_options"] = [
            create_bb(421, '', 14, 1, ['ret'], [])]
        graph["_vfprintf_l"] = [create_bb(426, '', 412, 1, ['alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'store',
                                          'load', 'load', 'load', 'load', 'call __local_stdio_printf_options', 'load', 'call __stdio_common_vfprintf', 'ret'], [])]
        graph["printf"] = [create_bb(132, '', 293, 1, ['alloca', 'alloca', 'alloca', 'store', 'call llvm.va_start',
                                     'load', 'load', 'call __acrt_iob_func', 'call _vfprintf_l', 'store', 'call llvm.va_end', 'load', 'ret'], [])]
        graph["calculadora"] = [create_bb(119, '', 188, 1, [
                                          'alloca', 'call printf', 'getelementptr', 'call scanf', 'getelementptr', 'load', 'sext', 'sdiv', 'ret'], [])]
        graph["soma_prefixa"] = [create_bb(193, '', 451, 0, ['alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'load', 'icmp', 'br'], [1, 10]),
                                 create_bb(208, '12', 41, 0, [
                                           'store', 'br'], [2]),
                                 create_bb(212, '13', 123, 0, [
                                           'store', 'store', 'load', 'load', 'icmp', 'br'], [3, 7]),
                                 create_bb(220, '17', 23, 0, ['br'], [4]),
                                 create_bb(223, '18', 203, 0, [
                                           'load', 'load', 'sext', 'getelementptr', 'load', 'load', 'add', 'store', 'load', 'add', 'store', 'br'], [5]),
                                 create_bb(237, '28', 87, 50, [
                                           'load', 'load', 'icmp', 'br'], [4, 6]),
                                 create_bb(243, '32', 117, 0, [
                                           'load', 'load', 'load', 'sext', 'getelementptr', 'store', 'br'], [7]),
                                 create_bb(252, '38', 75, 0, [
                                           'load', 'add', 'store', 'br'], [8]),
                                 create_bb(258, '41', 87, 10, [
                                           'load', 'load', 'icmp', 'br'], [2, 9]),
                                 create_bb(264, '45', 23, 0, ['br'], [10]),
                                 create_bb(267, '46', 8, 1, ['ret'], [])]
        graph["fatorial"] = [create_bb(166, '', 195, 0, ['alloca', 'alloca', 'store', 'load', 'icmp', 'br'], [1, 2]),
                             create_bb(175, '6', 41, 0, ['store', 'br'], [3]),
                             create_bb(179, '7', 120, 0, [
                                       'load', 'load', 'sub', 'call fatorial', 'mul', 'store', 'br'], [3]),
                             create_bb(188, '13', 28, 1, ['load', 'ret'], [])]
        graph["rand"] = []
        graph["srand"] = []
        graph["_time64"] = []
        graph["time"] = [create_bb(
            345, '', 113, 1, ['alloca', 'store', 'load', 'call _time64', 'ret'], [])]
        graph["main"] = [create_bb(271, '', 542, 0, ['alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'load', 'getelementptr', 'load', 'call printf', 'call time', 'trunc', 'call srand', 'store', 'br'], [1]),
                         create_bb(293, '16', 67, 0, [
                                   'load', 'icmp', 'br'], [2, 4]),
                         create_bb(298, '19', 299, 0, ['call rand', 'srem', 'load', 'sext', 'getelementptr',
                                   'store', 'call rand', 'srem', 'load', 'sext', 'getelementptr', 'store', 'br'], [3]),
                         create_bb(313, '30', 75, 20, [
                                   'load', 'add', 'store', 'br'], [1]),
                         create_bb(319, '33', 139, 0, ['store', 'load', 'getelementptr', 'getelementptr',
                                   'call soma_prefixa', 'call calculadora', 'store', 'load', 'icmp', 'br'], [5, 6]),
                         create_bb(331, '40', 61, 0, [
                                   'load', 'call fatorial', 'store', 'br'], [6]),
                         create_bb(337, '43', 28, 1, ['load', 'call printf', 'ret'], [])]

        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_hybrid(), 32450)

    #VC-130
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_02_void_function(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = []
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_hybrid(), 0)

    #VC-131
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_03_recursive_function(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(10, '', 50, 1, ['call main'], [])]
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_hybrid(), 50)

    #VC-132
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_04_read_instruction(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(5, '', 155, 1, [
                                   'alloca', 'br', 'add', 'fdiv', 'getelementptr', 'fmul', 'store', 'load', 'ret'], [])]
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_hybrid(), 155)

    #VC-133
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_05_simple_conditional(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(145, 'start', 10, 0, ['select', 'trunc', 'br'], [1, 2]), create_bb(150, 'exit_1', 100, 1, [
            'and', 'and', 'and', 'and', 'and', 'ret'], []), create_bb(170, 'pre_exit_2', 50, 0, ['br'], [3]), create_bb(180, 'exit_2', 200, 1, ['fsub', 'ret'], [])]
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_hybrid(), 260)

    #VC-134
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_06_infeasible_solve(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(145, 'execute_10_times', 50, 10, ['select', 'trunc', 'br'], [
                                   1]), create_bb(180, 'execute_once', 50, 1, ['fsub', 'ret'], [])]
        ipet = Ipet(graph, project)
        with self.assertRaises(SystemExit):
            ipet.run_ipet_hybrid()

    #VC-135
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_07_without_connections_instructions(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(145, 'start', 10, 0, ['and'], [1, 2]), create_bb(150, 'exit_1', 10, 1, ['and'], [
        ]), create_bb(170, 'pre_exit_2', 10, 0, ['and'], [3]), create_bb(180, 'exit_2', 10, 1, ['and'], [])]
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_hybrid(), 30)

    #VC-136
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_08_loop_with_two_entry_points(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(0, '', 10, 0, ['and'], [1]),
                         create_bb(1, '', 10, 0, ['and'], [2, 8]),
                         create_bb(2, '', 10, 0, ['and'], [3, 4]),
                         create_bb(3, '', 10, 0, ['and'], [9]),
                         create_bb(4, '', 10, 0, ['and'], [5, 6]),
                         create_bb(5, '', 10, 0, ['and'], [7]),
                         create_bb(6, '', 10, 0, ['and'], [7]),
                         create_bb(7, '', 10, 15, ['and'], [1]),
                         create_bb(8, '', 10, 0, ['and'], [9]),
                         create_bb(9, '', 8, 1, ['ret'], [])]
        ipet = Ipet(graph, project)
        self.assertEqual(ipet.run_ipet_hybrid(), 798)

    #VC-137
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_09_default_main(self, project, mock_stdout):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "nonexistingfunction"

        graph = {}
        graph["main"] = [create_bb(57, 'block0', 50, 1, ['ret'], [])]
        ipet = Ipet(graph, project)
        ipet.run_ipet_hybrid()

        self.assertEqual(mock_stdout.getvalue(),
        "Starting Hybrid IPET...\nFunction: main --- Otimization complete!\n\33[42mIPET finished.\33[0m\n\33[43mWarning: The function selected by user wasn't found, so the FioWAT selected 'main function'\33[0m\n")
  
    #VC-138
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_10_stop_second_function(self, project):
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "second"

        graph = {}
        graph["first"] = [create_bb(1, 'block0', 50, 1, ['ret'], [])]
        graph["second"] = [create_bb(2, 'block1', 50, 1, ['call first', 'ret'], [])]
        graph["main"] = [create_bb(3, 'block2', 1000, 1, ['call second', 'add', 'fmul', 'add', 'ret'], [])]
        ipet = Ipet(graph, project)

        self.assertEqual(ipet.run_ipet_hybrid(), 100)
        self.assertEqual(project.get_function_target.call_count, 2)
        







######################################################################################################

class Test_run_ipet_constraint_solver(unittest.TestCase):

    #VC-139
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_01_first_program(self, project):
        intermediate_values = IntermediateValues()
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["llvm.va_end"] = []
        graph["__stdio_common_vfscanf"] = []
        graph["__local_stdio_scanf_options"] = [create_bb(472, '#;__local_stdio_scanf_options;block0', 14, 1, ['ret'], [])]
        graph["_vfscanf_l"] = [create_bb(450, '#;_vfscanf_l;block0', 412, 1, ['alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'store','load', 'load', 'load', 'load', 'call __local_stdio_scanf_options', 'load', 'call __stdio_common_vfscanf', 'ret'], [])]
        graph["__acrt_iob_func"] = []
        graph["llvm.va_start"] = []
        graph["scanf"] = [create_bb(149, '#;scanf;block0', 293, 1, ['alloca', 'alloca', 'alloca', 'store', 'call llvm.va_start','load', 'load', 'call __acrt_iob_func', 'call _vfscanf_l', 'store', 'call llvm.va_end', 'load', 'ret'], [])]
        graph["__stdio_common_vfprintf"] = []
        graph["__local_stdio_printf_options"] = [create_bb(421, '#;__local_stdio_printf_options;block0', 14, 1, ['ret'], [])]
        graph["_vfprintf_l"] = [create_bb(426, '#;_vfprintf_l;block0', 412, 1, ['alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'store','load', 'load', 'load', 'load', 'call __local_stdio_printf_options', 'load', 'call __stdio_common_vfprintf', 'ret'], [])]
        graph["printf"] = [create_bb(132, '#;printf;block0', 293, 1, ['alloca', 'alloca', 'alloca', 'store', 'call llvm.va_start','load', 'load', 'call __acrt_iob_func', 'call _vfprintf_l', 'store', 'call llvm.va_end', 'load', 'ret'], [])]
        graph["calculadora"] = [create_bb(119, '#;calculadora;block0', 188, 1, ['alloca', 'call printf', 'getelementptr', 'call scanf', 'getelementptr', 'load', 'sext', 'sdiv', 'ret'], [])]
        graph["soma_prefixa"] = [create_bb(193, '#;soma_prefixa;block0', 451, 0, ['alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'load', 'icmp', 'br'], [1, 10]),
                                 create_bb(208, '#;soma_prefixa;block1', 41, 0, ['store', 'br'], [2]),
                                 create_bb(212, '#;soma_prefixa;block2', 123, 0, ['store', 'store', 'load', 'load', 'icmp', 'br'], [3, 7]),
                                 create_bb(220, '#;soma_prefixa;block3', 23, 0, ['br'], [4]),
                                 create_bb(223, '#;soma_prefixa;block4', 203, 0, ['load', 'load', 'sext', 'getelementptr', 'load', 'load', 'add', 'store', 'load', 'add', 'store', 'br'], [5]),
                                 create_bb(237, '#;soma_prefixa;block5', 87, 50, ['load', 'load', 'icmp', 'br'], [4, 6]),
                                 create_bb(243, '#;soma_prefixa;block6', 117, 0, ['load', 'load', 'load', 'sext', 'getelementptr', 'store', 'br'], [7]),
                                 create_bb(252, '#;soma_prefixa;block7', 75, 0, ['load', 'add', 'store', 'br'], [8]),
                                 create_bb(258, '#;soma_prefixa;block8', 87, 10, ['load', 'load', 'icmp', 'br'], [2, 9]),
                                 create_bb(264, '#;soma_prefixa;block9', 23, 0, ['br'], [10]),
                                 create_bb(267, '#;soma_prefixa;block10', 8, 1, ['ret'], [])]
        graph["fatorial"] = [create_bb(166, '#;fatorial;block0', 195, 0, ['alloca', 'alloca', 'store', 'load', 'icmp', 'br'], [1, 2]),
                             create_bb(175, '#;fatorial;block1', 41, 0, ['store', 'br'], [3]),
                             create_bb(179, '#;fatorial;block2', 120, 0, ['load', 'load', 'sub', 'call fatorial', 'mul', 'store', 'br'], [3]),
                             create_bb(188, '#;fatorial;block3', 28, 1, ['load', 'ret'], [])]
        graph["rand"] = []
        graph["srand"] = []
        graph["_time64"] = []
        graph["time"] = [create_bb(345, '#;time;block0', 113, 1, ['alloca', 'store', 'load', 'call _time64', 'ret'], [])]
        graph["main"] = [create_bb(271, '#;main;block0', 542, 0, ['alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store', 'load', 'getelementptr', 'load', 'call printf', 'call time', 'trunc', 'call srand', 'store', 'br'], [1]),
                         create_bb(293, '#;main;block1', 67, 0, ['load', 'icmp', 'br'], [2, 4]),
                         create_bb(298, '#;main;block2', 299, 0, ['call rand', 'srem', 'load', 'sext', 'getelementptr','store', 'call rand', 'srem', 'load', 'sext', 'getelementptr', 'store', 'br'], [3]),
                         create_bb(313, '#;main;block3', 75, 20, ['load', 'add', 'store', 'br'], [1]),
                         create_bb(319, '#;main;block4', 139, 0, ['store', 'load', 'getelementptr', 'getelementptr','call soma_prefixa', 'call calculadora', 'store', 'load', 'icmp', 'br'], [5, 6]),
                         create_bb(331, '#;main;block5', 61, 0, ['load', 'call fatorial', 'store', 'br'], [6]),
                         create_bb(337, '#;main;block6', 28, 1, ['load', 'call printf', 'ret'], [])]

        result = {'__local_stdio_scanf_options': [('block0', 1)],
                  '_vfscanf_l': [('block0', 1)],
                  'scanf': [('block0', 1)],
                  '__local_stdio_printf_options': [('block0', 1)],
                  '_vfprintf_l': [('block0', 1)],
                  'printf': [('block0', 1)],
                  'calculadora': [('block0', 1)],
                  'soma_prefixa': [('block0', 1), ('block1', 1), ('block2', 10), ('block3', 10), ('block4', 50), ('block5', 50), ('block6', 10), ('block7', 10), ('block8', 10), ('block9', 1), ('block10', 1)],
                  'fatorial': [('block0', 1), ('block2', 1), ('block3', 1)],
                  'time': [('block0', 1)]}

        ipet = Ipet(graph, project, intermediate_values)
        self.assertEqual(ipet.run_ipet_constraint_solver(), 32450)
        self.assertDictEqual(intermediate_values.get_all_worst_path_basic_block(), result)

    #VC-140
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_02_void_function(self, project):
        intermediate_values = IntermediateValues()
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = []

        result = {}

        ipet = Ipet(graph, project, intermediate_values)
        self.assertEqual(ipet.run_ipet_constraint_solver(), 0)
        self.assertDictEqual(intermediate_values.get_all_worst_path_basic_block(), result)

    #VC-141
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_03_recursive_function(self, project):
        intermediate_values = IntermediateValues()
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "fat"

        graph = {}
        graph["fat"] = [create_bb(10, '#;fat;block0', 50, 1, ['call fat'], [])]
        ipet = Ipet(graph, project, intermediate_values)

        result = {'fat': [('block0', 1)]}

        self.assertEqual(ipet.run_ipet_constraint_solver(), 50)
        self.assertDictEqual(intermediate_values.get_all_worst_path_basic_block(), result)

    #VC-142
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_04_read_instruction(self, project):
        intermediate_values = IntermediateValues()
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "fat"

        graph = {}
        graph["fat"] = [create_bb(5, '#;fat;block0', 155, 1, [
                                   'alloca', 'br', 'add', 'fdiv', 'getelementptr', 'fmul', 'store', 'load', 'ret'], [])]
        
        result = {'fat': [('block0', 1)]}
        
        ipet = Ipet(graph, project, intermediate_values)
        self.assertEqual(ipet.run_ipet_constraint_solver(), 155)
        self.assertDictEqual(intermediate_values.get_all_worst_path_basic_block(), result)

    #VC-143
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_05_simple_conditional(self, project):
        intermediate_values = IntermediateValues()
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "fat"

        graph = {}
        graph["fat"] = [create_bb(145, '#;fat;block0', 10, 0, ['select', 'trunc', 'br'], [1, 2]), create_bb(150, '#;fat;block1', 100, 1, [
            'and', 'and', 'and', 'and', 'and', 'ret'], []), create_bb(170, '#;fat;block2', 50, 0, ['br'], [3]), create_bb(180, '#;fat;block3', 200, 1, ['fsub', 'ret'], [])]
        
        result = {'fat': [('block0', 1), ('block2', 1), ('block3', 1)]}
        
        ipet = Ipet(graph, project, intermediate_values)
        self.assertEqual(ipet.run_ipet_constraint_solver(), 260)
        self.assertDictEqual(intermediate_values.get_all_worst_path_basic_block(), result)

    #VC-144
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_06_infeasible_solve(self, project):
        intermediate_values = IntermediateValues()
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "fat"

        graph = {}
        graph["fat"] = [create_bb(145, '#;fat;block0', 50, 10, ['select', 'trunc', 'br'], [
                                   1]), create_bb(180, 'execute_once', 50, 1, ['fsub', 'ret'], [])]
        
        result = {}
        
        ipet = Ipet(graph, project, intermediate_values)
        with self.assertRaises(SystemExit):
            ipet.run_ipet_constraint_solver()
        self.assertDictEqual(intermediate_values.get_all_worst_path_basic_block(), result)

    #VC-145
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_07_worst_path_main_function(self, project):
        intermediate_values = IntermediateValues()
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "main"

        graph = {}
        graph["main"] = [create_bb(145, '#;main;block0', 10, 0, ['and'], [1, 2]), create_bb(150, '#;main;block1', 10, 1, ['and'], [
        ]), create_bb(170, '#;main;block2', 10, 0, ['and'], [3]), create_bb(180, '#;main;block2', 10, 1, ['and'], [])]
        
        result = {}
        
        ipet = Ipet(graph, project, intermediate_values)
        self.assertEqual(ipet.run_ipet_constraint_solver(), 30)
        self.assertDictEqual(intermediate_values.get_all_worst_path_basic_block(), result)

    #VC-146
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_08_loop_with_two_entry_points(self, project):
        intermediate_values = IntermediateValues()
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "fat"

        graph = {}
        graph["fat"] =  [create_bb(0, '#;fat;block0', 10, 0, ['and'], [1]),
                         create_bb(1, '#;fat;block1', 10, 0, ['and'], [2, 8]),
                         create_bb(2, '#;fat;block2', 10, 0, ['and'], [3, 4]),
                         create_bb(3, '#;fat;block3', 10, 0, ['and'], [9]),
                         create_bb(4, '#;fat;block4', 10, 0, ['and'], [5, 6]),
                         create_bb(5, '#;fat;block5', 10, 0, ['and'], [7]),
                         create_bb(6, '#;fat;block6', 10, 0, ['and'], [7]),
                         create_bb(7, '#;fat;block7', 10, 15, ['and'], [1]),
                         create_bb(8, '#;fat;block8', 10, 0, ['and'], [9]),
                         create_bb(9, '#;fat;block9', 8, 1, ['ret'], [])]

        result = {'fat': [('block0', 1), ('block1', 16), ('block2', 16), ('block3', 1), ('block4', 15), ('block5', 15), ('block7', 15), ('block9', 1)]}

        ipet = Ipet(graph, project, intermediate_values)
        self.assertEqual(ipet.run_ipet_constraint_solver(), 798)
        self.assertDictEqual(intermediate_values.get_all_worst_path_basic_block(), result)

    #VC-147
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_09_default_main(self, project, mock_stdout):
        intermediate_values = IntermediateValues()
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "nonexistingfunction"

        graph = {}
        graph["main"] = [create_bb(57, 'block0', 50, 1, ['ret'], [])]

        result = {}

        ipet = Ipet(graph, project, intermediate_values)
        ipet.run_ipet_constraint_solver()

        self.assertEqual(mock_stdout.getvalue(),
        "Starting Constraint Solver...\nFunction: main --- Otimization complete!\n\33[42mIPET finished.\33[0m\n\33[43mWarning: The function selected by user wasn't found, so the FioWAT selected 'main function'\33[0m\n")
        self.assertDictEqual(intermediate_values.get_all_worst_path_basic_block(), result)

    #VC-148
    @patch('src.utils.user_project.UserProject.get_architecture')
    def test_10_stop_second_function(self, project):
        intermediate_values = IntermediateValues()
        project = Mock()
        project.get_architecture.return_value = "avr"
        project.get_function_target.return_value = "second"

        graph = {}
        graph["first"] = [create_bb(1, '#;first;block0', 50, 1, ['ret'], [])]
        graph["second"] = [create_bb(2, '#;second;block1', 50, 1, ['call first', 'ret'], [])]
        graph["main"] = [create_bb(3, '#;main;block2', 1000, 1, ['call second', 'add', 'fmul', 'add', 'ret'], [])]
        
        result = {'first': [('block0', 1)], 'second': [('block1', 1)]}
        
        ipet = Ipet(graph, project, intermediate_values)

        self.assertEqual(ipet.run_ipet_constraint_solver(), 100)
        self.assertEqual(project.get_function_target.call_count, 2)
        self.assertDictEqual(intermediate_values.get_all_worst_path_basic_block(), result)





if __name__ == '__main__':
    unittest.main()