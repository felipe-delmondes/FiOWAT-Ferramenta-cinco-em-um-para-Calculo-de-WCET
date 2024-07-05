from setup_test import *

from src.utils.intermediate_values import IntermediateValues


class Test_BasicBlock(unittest.TestCase):

    #VC-232
    def test_01_constructor(self):
        intermediate_values = IntermediateValues()
        
        self.assertEqual(intermediate_values.get_ir(), [])
        self.assertEqual(intermediate_values.get_call_graph(), [])
        self.assertEqual(intermediate_values.get_all_user_project_files(), [])
        self.assertEqual(intermediate_values.get_mapping_loop_lines(), [])
        self.assertEqual(intermediate_values.get_mapping_loop_bound(), {})
        self.assertEqual(intermediate_values.get_mapping_important_functions_lines(), {})
        self.assertEqual(intermediate_values.get_mapping_void_functions_lines(), {})
        self.assertEqual(intermediate_values.get_function_name_post_order(), [])
        self.assertEqual(intermediate_values.get_all_worst_path_basic_block(), {})
        self.assertEqual(intermediate_values.get_init_debug_table(), 0)
        self.assertEqual(intermediate_values.get_number_executions_worst_path(), 0)

    #VC-233
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_02_str_function_default(self, mock_stdout):
        intermediate_values = IntermediateValues()
        
        print(intermediate_values)
        self.assertEqual(mock_stdout.getvalue(),
                         "*** Intermediate Values ***" + \
                         "\nIR: False" + \
                         "\nCall Graph: False" + \
                         "\nNumber execututions Worst Path: 0.0\n")

    #VC-234
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_03_str_function_set(self, mock_stdout):
        intermediate_values = IntermediateValues()
        intermediate_values.set_ir(["add"])
        intermediate_values.set_call_graph(["Node"])
        intermediate_values.increment_number_executions_worst_path(200)

        print(intermediate_values)
        self.assertEqual(mock_stdout.getvalue(),
                         "*** Intermediate Values ***" + \
                         "\nIR: True" + \
                         "\nCall Graph: True" + \
                         "\nNumber execututions Worst Path: 200.0\n")

    #VC-235
    def test_04_setters(self):
        intermediate_values = IntermediateValues()
        
        intermediate_values.set_ir(["add"])
        intermediate_values.set_call_graph(["Node"])
        intermediate_values.set_all_user_project_files({'index_filename': 2, 'filename': 'Desktop\\\\wcet_project\\\\header_file.h', 'directory': 'C:\\Users\\Marcus\\', 'checksum': '7bdd5928b1f3a6c967a6ea18142b9bc3'})
        intermediate_values.set_all_user_project_files({'index_filename': 3, 'filename': 'Desktop\\\\wcet_project\\\\code.c', 'directory': 'C:\\Users\\Peter\\', 'checksum': '7bdd5928b1f3a6c77776ea18142b9bc3'})
        intermediate_values.set_mapping_loop_lines({'index_filename': 14, 'line_source_code': 14, 'index_ir': 185, 'line_ir_code': 273})
        intermediate_values.set_mapping_loop_lines({'index_filename': 50, 'line_source_code': 20, 'index_ir': 4, 'line_ir_code': 111})
        intermediate_values.set_mapping_loop_bound(111, 510)
        intermediate_values.set_mapping_loop_bound(7, 8)
        intermediate_values.set_mapping_important_functions_lines('sprintf', 46)
        intermediate_values.set_mapping_important_functions_lines('scanf', 10)
        intermediate_values.set_mapping_void_functions_lines('llvm.declare', 2)
        intermediate_values.set_mapping_void_functions_lines('iot_arct', 111)
        intermediate_values.set_function_name_post_order('llvm.va_end')
        intermediate_values.set_function_name_post_order('__stdio_common_vfscanf')
        intermediate_values.set_worst_path_basic_block('main', 'block0', 3)
        intermediate_values.set_worst_path_basic_block('fat', 'block2', 78)
        intermediate_values.set_worst_path_basic_block('main', 'block1', 20)
        intermediate_values.set_init_debug_table(50)
        intermediate_values.increment_number_executions_worst_path(7)
        intermediate_values.increment_number_executions_worst_path(15)

        self.assertEqual(intermediate_values.get_ir(), ["add"])
        self.assertEqual(intermediate_values.get_call_graph(), ["Node"])
        self.assertEqual(intermediate_values.get_all_user_project_files(), [{'index_filename': 2, 'filename': 'Desktop\\\\wcet_project\\\\header_file.h', 'directory': 'C:\\Users\\Marcus\\', 'checksum': '7bdd5928b1f3a6c967a6ea18142b9bc3'},
                                                                            {'index_filename': 3, 'filename': 'Desktop\\\\wcet_project\\\\code.c', 'directory': 'C:\\Users\\Peter\\', 'checksum': '7bdd5928b1f3a6c77776ea18142b9bc3'}])
        self.assertEqual(intermediate_values.get_mapping_loop_lines(), [{'index_filename': 14, 'line_source_code': 14, 'index_ir': 185, 'line_ir_code': 273},
                                                                        {'index_filename': 50, 'line_source_code': 20, 'index_ir': 4, 'line_ir_code': 111}])
        self.assertEqual(intermediate_values.get_mapping_loop_bound(), {111: 510, 7: 8})
        self.assertEqual(intermediate_values.get_mapping_important_functions_lines(), {'sprintf': 46, 'scanf': 10})
        self.assertEqual(intermediate_values.get_mapping_void_functions_lines(), {'llvm.declare': 2, 'iot_arct': 111})
        self.assertEqual(intermediate_values.get_function_name_post_order(), ['llvm.va_end', '__stdio_common_vfscanf'])
        self.assertEqual(intermediate_values.get_all_worst_path_basic_block(), {'main': [('block0', 3), ('block1', 20)], 'fat': [('block2', 78)]})
        self.assertEqual(intermediate_values.get_init_debug_table(), 50)
        self.assertEqual(intermediate_values.get_number_executions_worst_path(), 22)


if __name__ == '__main__':
    unittest.main()