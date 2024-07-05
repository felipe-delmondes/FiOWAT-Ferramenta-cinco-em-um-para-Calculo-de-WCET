from setup_test import *
from src.cfg.graph_generator import mapping_nodes_and_names, create_node_for_callgraph, post_order, create_call_graph_in_post_order, read_instruction, define_basic_block_id, define_next_basic_blocks, update_index_basic_block, define_first_basic_block_id, graph_generator_post_order
from src.utils.intermediate_values import IntermediateValues


class Test_mapping_nodes_and_names(unittest.TestCase):

    # VC-067
    def test_01_find_code_of_main(self):
        line = "	Node0x1c93e82a950 [shape=record,label=\"{main}\"];"
        nodes = {'Node0x1c93e829a50': 'vsprintf',
                 'Node0x1c93e829ad0': 'sprintf',
                 'Node0x1c93e8296d0': '_snprintf',
                 'Node0x1c93e82ac50': 'llvm.va_end',
                 'Node0x1c93e82a2d0': '_vsprintf_l',
                 'Node0x1c93e82a8d0': '_vsnprintf_l',
                 'Node0x1c93e8299d0': '_vsnprintf'}
        main = []

        # Multiples assertions. If the first assertion fail, the test as whole fails. And the NEXT ASSERTION ISN'T tested
        # You can add message to the assertion to help distinguish which assertions fail
        self.assertEqual(mapping_nodes_and_names(line, nodes, main),
                         "Node0x1c93e82a950", msg="Current node not found")
        self.assertEqual(main[0], "Node0x1c93e82a950",
                         msg="Main function not found")

    # VC-068
    def test_02_add_first_code(self):
        line = "	Node0x1c93e829a50 [shape=record,label=\"{vsprintf}\"];"
        nodes = {}
        main = []
        self.assertEqual(mapping_nodes_and_names(line, nodes, main),
                         "Node0x1c93e829a50", msg="Current node not found")
        self.assertEqual(
            nodes, {'Node0x1c93e829a50': 'vsprintf'}, msg="New code not added")

    # VC-069
    def test_03_propagate_main(self):
        line = "	Node0x1c93e8291d0 [shape=record,label=\"{__stdio_common_vsprintf}\"];"
        nodes = {
            'Node0x1c93e829a50': 'vsprintf', 'Node0x1c93e829ad0': 'sprintf',
            'Node0x1c93e8296d0': '_snprintf',
            'Node0x1c93e82ac50': 'llvm.va_end',
            'Node0x1c93e82a2d0': '_vsprintf_l',
            'Node0x1c93e82a8d0': '_vsnprintf_l',
            'Node0x1c93e8299d0': '_vsnprintf', 'Node0x1c93e82a950': 'main',
            'Node0x1c93e828f50': 'llvm.va_start'}
        main = ['Node0x1c93e82a950']
        self.assertEqual(mapping_nodes_and_names(line, nodes, main),
                         "Node0x1c93e8291d0", msg="Current node not found")
        self.assertEqual(main[0], "Node0x1c93e82a950", msg="Main disappeared")

    # VC-070
    def test_04_invalid_line(self):
        line = "	       Node0x1c93e8291d0 [shape=record,label=\"{__stdio_common_vsprintf}\"];"
        nodes = {}
        main = []
        self.assertEqual(mapping_nodes_and_names(
            line, nodes, main), "", msg="Read something wrong")
        self.assertEqual(
            nodes, {'': '__stdio_common_vsprintf'}, msg="New code not added")

    # VC-071
    def test_05_without_braces(self):
        line = "	Node0x1c93e829a50 [shape=record,label=\"{vsprintf\"];"
        nodes = {}
        main = []
        with self.assertRaises(IndexError):
            mapping_nodes_and_names(line, nodes, main)


class Test_create_node_for_callgraph(unittest.TestCase):

    # VC-072
    def test_01_recursion(self):
        file = open(INPUT_DIRECTORY + "first.ll.callgraph.dot", 'r')
        dot = file.readlines()
        file.close()
        line = 16
        nodes = {'Node0x1c93e829a50': ['Node0x1c93e82a8d0']}
        current_node = "Node0x262043ea820"

        create_node_for_callgraph(dot, line, nodes, current_node)
        self.assertEqual(nodes, {'Node0x1c93e829a50': [
                         'Node0x1c93e82a8d0'], 'Node0x262043ea820': []})

    # VC-073
    def test_02_find_all_children(self):
        file = open(INPUT_DIRECTORY + "first.ll.callgraph.dot", 'r')
        dot = file.readlines()
        file.close()
        line = 22
        nodes = {}
        current_node = "Node0x262043ea2a0"

        create_node_for_callgraph(dot, line, nodes, current_node)
        self.assertEqual(nodes, {'Node0x262043ea2a0': [
                         'Node0x262043e9d20', 'Node0x262043ead20', 'Node0x262043eb520', 'Node0x262043eaca0']})

    # VC-074
    def test_03_leaf_node(self):
        file = open(INPUT_DIRECTORY + "first.ll.callgraph.dot", 'r')
        dot = file.readlines()
        file.close()
        line = 20
        nodes = {}
        current_node = "Node0x262043eada0"

        create_node_for_callgraph(dot, line, nodes, current_node)
        self.assertEqual(nodes, {'Node0x262043eada0': []})

    # VC-075
    def test_04_invalid_line(self):
        file = open(INPUT_DIRECTORY + "first.ll.callgraph.dot", 'r')
        dot = file.readlines()
        file.close()
        line = 0
        nodes = {}
        current_node = "Node0x262043eaba0"

        create_node_for_callgraph(dot, line, nodes, current_node)
        self.assertEqual(nodes, {'Node0x262043eaba0': []})

    # VC-118
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_05_warning_message(self, mock_stdout):
        file = open(INPUT_DIRECTORY + "first.ll.callgraph.dot", 'r')
        dot = file.readlines()
        file.close()
        line = 16
        nodes = {'Node0x1c93e829a50': ['Node0x1c93e82a8d0']}
        current_node = "Node0x262043ea820"

        create_node_for_callgraph(dot, line, nodes, current_node)
        self.assertEqual(
            mock_stdout.getvalue(),
            "\n\33[43mFound a recursive function. WCET will be underestimated.\33[0m\n")


class Test_post_order(unittest.TestCase):

    # VC-076
    # To mock object, you need use the template: MODULE.CLASS
    @patch('src.utils.user_project.UserProject')
    def test_01_one_function(self, mocked):
        node_entry_point = ['Node0x1c93e82a950']
        nodes = {
            'Node0x1c93e829a50': ['Node0x1c93e82a8d0'],
            'Node0x1c93e829ad0':
            ['Node0x1c93e828f50', 'Node0x1c93e82a2d0', 'Node0x1c93e82ac50'],
            'Node0x1c93e8296d0':
            ['Node0x1c93e828f50', 'Node0x1c93e8299d0', 'Node0x1c93e82ac50'],
            'Node0x1c93e82ac50': [],
            'Node0x1c93e82a2d0': ['Node0x1c93e82a8d0'],
            'Node0x1c93e82a8d0': ['Node0x1c93e82ad50', 'Node0x1c93e8291d0'],
            'Node0x1c93e8299d0': ['Node0x1c93e82a8d0'],
            'Node0x1c93e82a950': [],
            'Node0x1c93e828f50': [],
            'Node0x1c93e8291d0': [],
            'Node0x1c93e82ad50': []}
        node_and_names = {
            'Node0x1c93e829a50': 'vsprintf', 'Node0x1c93e829ad0': 'sprintf',
            'Node0x1c93e8296d0': '_snprintf',
            'Node0x1c93e82ac50': 'llvm.va_end',
            'Node0x1c93e82a2d0': '_vsprintf_l',
            'Node0x1c93e82a8d0': '_vsnprintf_l',
            'Node0x1c93e8299d0': '_vsnprintf', 'Node0x1c93e82a950': 'main',
            'Node0x1c93e828f50': 'llvm.va_start',
            'Node0x1c93e8291d0': '__stdio_common_vsprintf',
            'Node0x1c93e82ad50': '__local_stdio_printf_options'}
        # Just pass the object in the function
        post_order(node_entry_point, nodes, node_and_names, mocked)
        # Verify if function was called once with specific argument.
        # The template is: mock.method_name.assert_called_once_with(args)
        mocked.set_function_name_post_order.assert_called_once_with('main')

    # VC-077
    @patch('src.utils.user_project.UserProject')
    def test_02_multiple_functions(self, mocked):
        node_entry_point = ['Node0x227c27fad50']
        nodes = {
            'Node0x227c27fad50': ['Node0x227c27fb2d0', 'Node0x227c27fb6d0'],
            'Node0x227c27fb2d0': [],
            'Node0x227c27fb6d0': []}
        node_and_names = {'Node0x227c27fad50': 'main',
                          'Node0x227c27fb2d0': 'Initialize',
                          'Node0x227c27fb6d0': 'BubbleSort'}
        post_order(node_entry_point, nodes, node_and_names, mocked)

        # Each call of same method receive different value. For test this you need create a list of args
        # Template is: VARIABLE = call(args), call(args) ...
        # Observation: call is of unittest module, so declare its there
        calls = call('BubbleSort'), call('Initialize'), call('main')
        # Test if this args were pass in method.
        # Template is: MOCK.METHOD.assert_has_calls(list_args, any_order)
        # any_order -> Verify if called args were called in order
        # You don't need pass all args, it's possible pass the test using some args. But it's possible fail if order is different
        mocked.set_function_name_post_order.assert_has_calls(
            calls, any_order=False)

    #
    #
    # Recursion will generate infinite loop
    #
    #


# It's possible use patch in class, so all inside methods will use the same patch.
# The order is from bottom to top patch (Like stack)
@patch('src.cfg.graph_generator.mapping_nodes_and_names')
@patch('src.cfg.graph_generator.create_node_for_callgraph')
@patch('src.cfg.graph_generator.post_order')
@patch('src.utils.intermediate_values.IntermediateValues')
class Test_create_call_graph_in_post_order(unittest.TestCase):

    # VC-078
    # Pass these patchs like args, using the order: bottom to top. You cannot create Mock() for this parameters
    def test_01_normal_situation(
            self, intermediate_values, post_order, create_node_for_callgraph,
            mapping_nodes_and_names):
        file = open(INPUT_DIRECTORY + "bsort100.ll.callgraph.dot", 'r')
        intermediate_values.get_call_graph.return_value = file.readlines()
        file.close()
        post_order.return_value = ""
        create_node_for_callgraph.return_value = ""
        mapping_nodes_and_names.return_value = ""

        create_call_graph_in_post_order(intermediate_values)

        # Check if the function has been called a certain number of times
        # Template is: MOCK.FUNCTION_NAME.call_count
        self.assertEqual(intermediate_values.get_call_graph.call_count, 1)
        self.assertEqual(mapping_nodes_and_names.call_count, 3)
        self.assertEqual(create_node_for_callgraph.call_count, 3)
        self.assertEqual(post_order.call_count, 1)

    # VC-079
    def test_02_one_function(
            self, intermediate_values, post_order, create_node_for_callgraph,
            mapping_nodes_and_names):
        file = open(INPUT_DIRECTORY + "one.ll.callgraph.dot", 'r')
        intermediate_values.get_call_graph.return_value = file.readlines()
        file.close()
        post_order.return_value = ""
        create_node_for_callgraph.return_value = ""
        mapping_nodes_and_names.return_value = ""

        create_call_graph_in_post_order(intermediate_values)

        self.assertEqual(intermediate_values.get_call_graph.call_count, 1)
        self.assertEqual(mapping_nodes_and_names.call_count, 1)
        self.assertEqual(create_node_for_callgraph.call_count, 1)
        self.assertEqual(post_order.call_count, 1)


class Test_read_instruction(unittest.TestCase):

    # VC-080
    def test_01_instruction_after(self):
        self.assertEqual(read_instruction(
            "  %4 = alloca ptr, align 8"), "alloca")

    # VC-081
    def test_02_instruction_after(self):
        self.assertEqual(read_instruction(
            "  %8 = mul nsw i32 %7, 3, !dbg !50"), "mul")

    # VC-082
    def test_03_line_without_tab(self):
        self.assertEqual(read_instruction("%4 = alloca ptr, align 8"), "")

    # VC-083
    def test_04_instruction_before(self):
        self.assertEqual(read_instruction("  ret i32 %11, !dbg !23"), "ret")

    # VC-084
    def test_05_instruction_before(self):
        self.assertEqual(read_instruction(
            "  store i64 %1, ptr %5, align 8"), "store")

    # VC-085
    def test_06_call_function_after(self):
        self.assertEqual(
            read_instruction(
                "  %10 = call i32 @_vsnprintf_l(ptr noundef %9, i64 noundef -1, ptr noundef %8, ptr noundef null, ptr noundef %7), !dbg !29"),
            "call _vsnprintf_l")

    # VC-086
    def test_07_call_function_before(self):
        self.assertEqual(
            read_instruction(
                "  call void @llvm.va_start(ptr %8), !dbg !37"),
            "call llvm.va_start")

    # VC-087
    def test_08_call_function_multiple_at(self):
        self.assertEqual(
            read_instruction(
                "  %2 = call i32 (ptr, ...) @printf(ptr noundef @\"??_C@_0BI@IKGCHOED@Digite?5um?5frase?5curta?3?5?$AA@\"), !dbg !49"),
            "call printf")

    # VC-088
    def test_09_instruction_double_word(self):
        self.assertEqual(
            read_instruction(
                "  %5 = getelementptr inbounds [10 x i8], ptr %1, i64 0, i64 0, !dbg !51"),
            "getelementptr")

    # VC-089
    def test_10_void_line(self):
        with self.assertRaises(IndexError):
            read_instruction("")

    # VC-090
    def test_11_assembly_inline(self):
        self.assertEqual(
            read_instruction(
                "  call addrspace(0) void asm sideeffect \"nop\", \"\"() #1, !srcloc !3"),
            "asm")

    # VC-091
    def test_12_call_function_addrspace(self):
        self.assertEqual(read_instruction(
            "  call addrspace(1) void @dumy()"), "call dumy")

    # VC-092
    def test_13_function_with_same_name_ir_instruction(self):
        self.assertEqual(read_instruction(
            "  call void @add(), !dbg !2"), "call add")


class Test_define_basic_block_id(unittest.TestCase):

    # VC-093
    def test_01_id_number(self):
        self.assertEqual(define_basic_block_id("33: ; preds = %16"), "33")

    # VC-094
    def test_02_id_string(self):
        self.assertEqual(define_basic_block_id(
            "main;01: ; preds = %16"), "main;01")

    # VC-095
    def test_03_void(self):
        self.assertEqual(define_basic_block_id(": ; preds = %40, %33"), "")

    # VC-096
    def test_04_error(self):
        # You can use general exception (Exception) or specific exception (e.g. OSError, ValueError, etc)
        with self.assertRaises(IndexError):
            define_basic_block_id("25 ; preds = %40, %33")

    # VC-097
    def test_05_remove_double_quotes(self):
        self.assertEqual(define_basic_block_id(
            "\"gdc;02\": ; preds = %\"gdc;05\""), "gdc;02")


class Test_define_next_basic_blocks(unittest.TestCase):

    # VC-098
    def test_01_void_line(self):
        self.assertEqual(define_next_basic_blocks(), [])

    # VC-099
    def test_02_one_next_block(self):
        self.assertEqual(define_next_basic_blocks(
            "  br label %13, !dbg !68"), ["13"])

    # VC-100
    def test_03_two_next_blocks(self):
        self.assertEqual(
            define_next_basic_blocks(
                "  br i1 %5, label %6, label %7, !dbg !67"),
            ["6", "7"])

    # VC-101
    def test_04_return(self):
        self.assertEqual(define_next_basic_blocks(
            "  ret i32 %14, !dbg !70"), [])

    # VC-102
    def test_05_loop(self):
        self.assertEqual(
            define_next_basic_blocks(
                "  br label %16, !dbg !101, !llvm.loop !105"),
            ["16"])


class Test_update_index_basic_block(unittest.TestCase):

    # VC-103
    def test_01_zero_connections(self):
        basic_block = Mock()
        basic_block.get_next_blocks.return_value = []

        function = [basic_block]
        mapping_bb_id_and_index = {'3': 0}

        update_index_basic_block(function, mapping_bb_id_and_index)

        basic_block.set_next_blocks.assert_called_once_with([])

    # VC-104
    def test_02_one_connections(self):
        basic_block = Mock()
        basic_block.get_next_blocks.return_value = ['16']
        mapping_bb_id_and_index = {'3': 0, '16': 1,
                                   '19': 2, '30': 3, '33': 4, '40': 5, '43': 6}

        calls = [call([1])]
        function = [basic_block]

        update_index_basic_block(function, mapping_bb_id_and_index)

        basic_block.set_next_blocks.assert_has_calls(calls, any_order=False)

    # VC-105
    def test_03_two_connections(self):
        basic_block = Mock()
        basic_block.get_next_blocks.return_value = ['12', '46']
        mapping_bb_id_and_index = {'4': 0, '12': 1, '13': 2, '17': 3,
                                   '18': 4, '28': 5, '32': 6, '38': 7, '41': 8, '45': 9, '46': 10}

        calls = [call([1, 10])]
        function = [basic_block]

        update_index_basic_block(function, mapping_bb_id_and_index)

        basic_block.set_next_blocks.assert_has_calls(calls, any_order=False)

    # VC-106
    def test_04_repeated_connections(self):
        basic_block1 = Mock()
        basic_block2 = Mock()
        basic_block3 = Mock()
        basic_block4 = Mock()
        basic_block1.get_next_blocks.return_value = ['6', '7']
        basic_block2.get_next_blocks.return_value = ['13']
        basic_block3.get_next_blocks.return_value = ['13']
        basic_block4.get_next_blocks.return_value = []
        mapping_bb_id_and_index = {'2': 0, '6': 1, '7': 2, '13': 3}

        calls1 = [call([1, 2])]
        calls2 = [call([3])]
        calls3 = [call([3])]
        calls4 = [call([])]
        function = [basic_block1, basic_block2, basic_block3, basic_block4]

        update_index_basic_block(function, mapping_bb_id_and_index)

        basic_block1.set_next_blocks.assert_has_calls(calls1, any_order=False)
        basic_block2.set_next_blocks.assert_has_calls(calls2, any_order=False)
        basic_block3.set_next_blocks.assert_has_calls(calls3, any_order=False)
        basic_block4.set_next_blocks.assert_has_calls(calls4, any_order=False)

    # VC-107
    def test_05_complex_graph(self):
        basic_block1 = Mock()
        basic_block2 = Mock()
        basic_block3 = Mock()
        basic_block4 = Mock()
        basic_block5 = Mock()
        basic_block6 = Mock()
        basic_block7 = Mock()
        basic_block1.get_next_blocks.return_value = ['16']
        basic_block2.get_next_blocks.return_value = ['19', '33']
        basic_block3.get_next_blocks.return_value = ['30']
        basic_block4.get_next_blocks.return_value = ['16']
        basic_block5.get_next_blocks.return_value = ['40', '43']
        basic_block6.get_next_blocks.return_value = ['43']
        basic_block7.get_next_blocks.return_value = []
        mapping_bb_id_and_index = {'3': 0, '16': 1,
                                   '19': 2, '30': 3, '33': 4, '40': 5, '43': 6}

        calls1 = [call([1])]
        calls2 = [call([2, 4])]
        calls3 = [call([3])]
        calls4 = [call([1])]
        calls5 = [call([5, 6])]
        calls6 = [call([6])]
        calls7 = [call([])]
        function = [basic_block1, basic_block2, basic_block3,
                    basic_block4, basic_block5, basic_block6, basic_block7]

        update_index_basic_block(function, mapping_bb_id_and_index)

        basic_block1.set_next_blocks.assert_has_calls(calls1, any_order=False)
        basic_block2.set_next_blocks.assert_has_calls(calls2, any_order=False)
        basic_block3.set_next_blocks.assert_has_calls(calls3, any_order=False)
        basic_block4.set_next_blocks.assert_has_calls(calls4, any_order=False)
        basic_block5.set_next_blocks.assert_has_calls(calls5, any_order=False)
        basic_block6.set_next_blocks.assert_has_calls(calls6, any_order=False)
        basic_block7.set_next_blocks.assert_has_calls(calls7, any_order=False)


class Test_define_first_basic_block_id(unittest.TestCase):

    # VC-108
    def test_01_numeric_id_function_without_parameters(self):
        self.assertEqual(
            define_first_basic_block_id(
                "define dso_local i32 @calculadora() #0 !dbg !45 {",
                "  %1 = alloca [10 x i8], align 1"),
            "1")

    # VC-109
    def test_02_numeric_id_function_with_parameters(self):
        self.assertEqual(
            define_first_basic_block_id(
                "define linkonce_odr dso_local i32 @_vsnprintf(ptr noundef %0, i64 noundef %1, ptr noundef %2, ptr noundef %3) #0 comdat !dbg !41 {",
                "  %5 = alloca ptr, align 8"),
            "5")

    # VC-110
    def test_03_numeric_id_next_line_different_value(self):
        self.assertEqual(
            define_first_basic_block_id(
                "define dso_local i32 @fatorial(i32 noundef %0) #0 !dbg !64 {",
                "  %11 = call i32 @fatorial(i32 noundef %10), !dbg !69"),
            "2")

    # VC-111
    def test_04_void_function(self):
        self.assertEqual(define_first_basic_block_id(
            "declare dso_local void @srand(i32 noundef) #1", "\n"), "1")

    # VC-112
    def test_05_string_id_function_without_parameters(self):
        self.assertEqual(
            define_first_basic_block_id(
                "define dso_local i16 @main() addrspace(1) #0 !dbg !7 {",
                "main_block0:"),
            "main_block0")

    # VC-113
    def test_06_string_id_function_with_parameters(self):
        self.assertEqual(
            define_first_basic_block_id(
                "define dso_local void @Initialize(ptr noundef %0) addrspace(1) #0 !dbg !13 {",
                "Initialize_block0:"),
            "Initialize_block0")

    # VC-114
    def test_07_string_id_semicolon(self):
        self.assertEqual(
            define_first_basic_block_id(
                "define dso_local void @BubbleSort(ptr noundef %0) addrspace(1) #0 !dbg !33 {",
                "BubbleSort;block0:"),
            "BubbleSort;block0")

    # VC-115
    def test_08_remove_double_quotes(self):
        self.assertEqual(
            define_first_basic_block_id(
                "define dso_local i16 @gdc(i16 noundef %0, i16 noundef %1) addrspace(1) #0 !dbg !24 {",
                "\"gdc;block0:\""),
            "gdc;block0")


class Test_graph_generator_post_order(unittest.TestCase):

    # VC-116
    def test_01_main_function_separated_from_the_rest(self):
        intermediate_values = IntermediateValues()

        file = open(INPUT_DIRECTORY + "semloop.ll", 'r')
        intermediate_values.set_ir(file.readlines())
        file.close()

        list_function = ['main']
        for f in list_function:
            intermediate_values.set_function_name_post_order(f)

        list_map = {'sprintf': 23, 'vsprintf': 42, '_snprintf': 57,
                    '_vsnprintf': 79, 'main': 97, '_vsprintf_l': 116,
                    '_vsnprintf_l': 137, '__local_stdio_printf_options': 178}
        for key, value in list_map.items():
            intermediate_values.set_mapping_important_functions_lines(
                key, value)

        list_bound = {}
        for key, value in list_bound.items():
            intermediate_values.set_mapping_loop_bound(key, value)

        graph = {}
        graph_generator_post_order(intermediate_values, graph)

        self.assertEqual(len(graph), 1)  # There are one function
        # The main function has one basic block
        self.assertEqual(len(graph['main']), 1)
        self.assertEqual(graph['main'][0].get_id(), 96)
        self.assertEqual(graph['main'][0].get_name(), '')
        self.assertEqual(graph['main'][0].get_weight(), 0)
        self.assertEqual(graph['main'][0].get_number_executions(), 1)
        self.assertEqual(
            graph['main'][0].get_instructions(),
            ['alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store',
             'store', 'load', 'mul', 'store', 'ret'])
        self.assertEqual(graph['main'][0].get_next_blocks(), [])

    # VC-117
    def test_02_loop_recursion_if_calls(self):
        intermediate_values = IntermediateValues()

        # Create new file, because it's necessary save in .ll file the directory about dependecys of user project
        # The triple target is host target
        command_raw = "clang -emit-llvm -S -w -gline-tables-only \"" + \
            INPUT_DIRECTORY + "first.c\" -o \"" + INPUT_DIRECTORY + "first.ll\""

        command_split = shlex.split(command_raw)
        subprocess.Popen(command_split, shell=True).wait()

        file = open(INPUT_DIRECTORY + "first.ll", 'r')
        intermediate_values.set_ir(file.readlines())
        file.close()

        list_function = [
            'llvm.va_end', '__stdio_common_vfscanf',
            '__local_stdio_scanf_options', '_vfscanf_l', '__acrt_iob_func',
            'llvm.va_start', 'scanf', '__stdio_common_vfprintf',
            '__local_stdio_printf_options', '_vfprintf_l', 'printf',
            'calculadora', 'soma_prefixa', 'fatorial', 'rand', 'srand',
            '_time64', 'time', 'main']
        for f in list_function:
            intermediate_values.set_function_name_post_order(f)

        list_map = {
            'sprintf': 46, 'vsprintf': 65, '_snprintf': 80, '_vsnprintf': 102,
            'calculadora': 120, 'printf': 133, 'scanf': 150, 'fatorial': 167,
            'soma_prefixa': 194, 'main': 272, 'time': 346, '_vsprintf_l': 360,
            '_vsnprintf_l': 381, '__local_stdio_printf_options': 422,
            '_vfprintf_l': 427, '_vfscanf_l': 451,
            '__local_stdio_scanf_options': 473}
        for key, value in list_map.items():
            intermediate_values.set_mapping_important_functions_lines(
                key, value)

        list_bound = {240: 50, 261: 10, 316: 20}
        for key, value in list_bound.items():
            intermediate_values.set_mapping_loop_bound(key, value)

        graph = {}
        graph_generator_post_order(intermediate_values, graph)

        self.assertEqual(len(graph), 19)

        # Test answer
        id = {
            "__local_stdio_scanf_options": [472],
            "_vfscanf_l": [450],
            "scanf": [149],
            "__local_stdio_printf_options": [421],
            "_vfprintf_l": [426],
            "printf": [132],
            "calculadora": [119],
            "soma_prefixa":
            [193, 208, 212, 220, 223, 237, 243, 252, 258, 264, 267],
            "fatorial": [166, 175, 179, 188],
            "time": [345],
            "main": [271, 293, 298, 313, 319, 331, 337]}
        name = {
            "__local_stdio_scanf_options": [''],
            "_vfscanf_l": [''],
            "scanf": [''],
            "__local_stdio_printf_options": [''],
            "_vfprintf_l": [''],
            "printf": [''],
            "calculadora": [''],
            "soma_prefixa":
            ['', '12', '13', '17', '18', '28', '32', '38', '41', '45', '46'],
            "fatorial": ['', '6', '7', '13'],
            "time": [''],
            "main": ['', '16', '19', '30', '33', '40', '43']}
        weight = {
            "__local_stdio_scanf_options": [0],
            "_vfscanf_l": [0],
            "scanf": [0],
            "__local_stdio_printf_options": [0],
            "_vfprintf_l": [0],
            "printf": [0],
            "calculadora": [0],
            "soma_prefixa": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "fatorial": [0, 0, 0, 0],
            "time": [0],
            "main": [0, 0, 0, 0, 0, 0, 0]}
        executions = {
            "__local_stdio_scanf_options": [1],
            "_vfscanf_l": [1],
            "scanf": [1],
            "__local_stdio_printf_options": [1],
            "_vfprintf_l": [1],
            "printf": [1],
            "calculadora": [1],
            "soma_prefixa": [0, 0, 0, 0, 0, 50, 0, 0, 10, 0, 1],
            "fatorial": [0, 0, 0, 1],
            "time": [1],
            "main": [0, 0, 0, 20, 0, 0, 1]}
        instructions = {
            "__local_stdio_scanf_options": [['ret']],
            "_vfscanf_l":
            [['alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store',
              'store', 'load', 'load', 'load', 'load',
              'call __local_stdio_scanf_options', 'load',
              'call __stdio_common_vfscanf', 'ret']],
            "scanf":
            [['alloca', 'alloca', 'alloca', 'store', 'call llvm.va_start',
              'load', 'load', 'call __acrt_iob_func', 'call _vfscanf_l',
              'store', 'call llvm.va_end', 'load', 'ret']],
            "__local_stdio_printf_options": [['ret']],
            "_vfprintf_l":
            [['alloca', 'alloca', 'alloca', 'alloca', 'store', 'store', 'store',
              'store', 'load', 'load', 'load', 'load',
              'call __local_stdio_printf_options', 'load',
              'call __stdio_common_vfprintf', 'ret']],
            "printf":
            [['alloca', 'alloca', 'alloca', 'store', 'call llvm.va_start',
              'load', 'load', 'call __acrt_iob_func', 'call _vfprintf_l',
              'store', 'call llvm.va_end', 'load', 'ret']],
            "calculadora":
            [['alloca', 'call printf', 'getelementptr', 'call scanf',
              'getelementptr', 'load', 'sext', 'sdiv', 'ret']],
            "soma_prefixa":
            [['alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'alloca',
              'store', 'store', 'store', 'load', 'icmp', 'br'],
             ['store', 'br'],
             ['store', 'store', 'load', 'load', 'icmp', 'br'],
             ['br'],
             ['load', 'load', 'sext', 'getelementptr', 'load', 'load', 'add',
              'store', 'load', 'add', 'store', 'br'],
             ['load', 'load', 'icmp', 'br'],
             ['load', 'load', 'load', 'sext', 'getelementptr', 'store', 'br'],
             ['load', 'add', 'store', 'br'],
             ['load', 'load', 'icmp', 'br'],
             ['br'],
             ['ret']],
            "fatorial":
            [['alloca', 'alloca', 'store', 'load', 'icmp', 'br'],
             ['store', 'br'],
             ['load', 'load', 'sub', 'call fatorial', 'mul', 'store', 'br'],
             ['load', 'ret']],
            "time": [['alloca', 'store', 'load', 'call _time64', 'ret']],
            "main":
            [['alloca', 'alloca', 'alloca', 'alloca', 'alloca', 'alloca',
              'alloca', 'store', 'store', 'store', 'load', 'getelementptr',
              'load', 'call printf', 'call time', 'trunc', 'call srand',
              'store', 'br'],
             ['load', 'icmp', 'br'],
             ['call rand', 'srem', 'load', 'sext', 'getelementptr', 'store',
              'call rand', 'srem', 'load', 'sext', 'getelementptr', 'store',
              'br'],
             ['load', 'add', 'store', 'br'],
             ['store', 'load', 'getelementptr', 'getelementptr',
              'call soma_prefixa', 'call calculadora', 'store', 'load', 'icmp',
              'br'],
             ['load', 'call fatorial', 'store', 'br'],
             ['load', 'call printf', 'ret']]}
        next_blocks = {
            "__local_stdio_scanf_options": [[]],
            "_vfscanf_l": [[]],
            "scanf": [[]],
            "__local_stdio_printf_options": [[]],
            "_vfprintf_l": [[]],
            "printf": [[]],
            "calculadora": [[]],
            "soma_prefixa":
            [[1, 10],
             [2],
             [3, 7],
             [4],
             [5],
             [4, 6],
             [7],
             [8],
             [2, 9],
             [10],
             []],
            "fatorial": [[1, 2],
                         [3],
                         [3],
                         []],
            "time": [[]],
            "main": [[1],
                     [2, 4],
                     [3],
                     [1],
                     [5, 6],
                     [6],
                     []]}

        # Create sub tests inside main test
        # You can see specifically which test fails, and the message help you which function/basic block fails
        for function in graph:
            for basic_block in enumerate(graph[function]):
                with self.subTest(msg="ID - Error in function: " + str(function) + ". Basic block: " + str(basic_block[0])):
                    self.assertEqual(
                        basic_block[1].get_id(),
                        id[function][basic_block[0]])

                with self.subTest(msg="Name - Error in function: " + str(function) + ". Basic block: " + str(basic_block[0])):
                    self.assertEqual(
                        basic_block[1].get_name(),
                        name[function][basic_block[0]])

                with self.subTest(msg="Weight - Error in function: " + str(function) + ". Basic block: " + str(basic_block[0])):
                    self.assertEqual(
                        basic_block[1].get_weight(),
                        weight[function][basic_block[0]])

                with self.subTest(msg="Number executions - Error in function: " + str(function) + ". Basic block: " + str(basic_block[0])):
                    self.assertEqual(
                        basic_block[1].get_number_executions(),
                        executions[function][basic_block[0]])

                with self.subTest(msg="Instructions - Error in function: " + str(function) + ". Basic block: " + str(basic_block[0])):
                    self.assertEqual(
                        basic_block[1].get_instructions(),
                        instructions[function][basic_block[0]])

                with self.subTest(msg="Next blocks - Error in function: " + str(function) + ". Basic block: " + str(basic_block[0])):
                    self.assertEqual(
                        basic_block[1].get_next_blocks(),
                        next_blocks[function][basic_block[0]])


if __name__ == '__main__':
    unittest.main()
