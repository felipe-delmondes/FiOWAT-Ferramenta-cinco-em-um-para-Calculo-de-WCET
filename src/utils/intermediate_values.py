class IntermediateValues:
    """
    DTO used in methodology pipeline to transfer values between functions.


    Parameters
    ----------
        None


    Attributes
    ----------
    ir : list
        Content of IR file (.ll)

    call_graph : list
        Content of call graph file (.dot)

    all_user_project_files : list
        Information about user source code in IR file.

        Example: {'index_filename': 2, 'filename': 'Desktop\\\\wcet_project\\\\header_file.h', 'directory': 'C:\\Users\\Marcus\\', 'checksum': '7bdd5928b1f3a6c967a6ea18142b9bc3'}

    mapping_loop_lines : list
        Relationship between source code loop line and IR loop line.

        Example: {'index_filename': 14, 'line_source_code': 14, 'index_ir': 185, 'line_ir_code': 273}

    mapping_loop_bound : dict
        Relationship between IR line and number of executions.

        Example: {273: 50, 294: 10, 354: 20}

    mapping_important_functions_lines : dict
        Relationship between function name and its line in IR file.

        Example: {'sprintf': 46}

    mapping_void_functions_lines : dict
        Relationship between function name and its line in IR file.

        Example: {'rand': 112}

    function_name_post_order : list
        All function name in post order.

        Example: ['llvm.va_end', '__stdio_common_vfscanf', ...]

    worst_path_basic_block : dict
        All functions, and its relationship between basic blocks name of worst path and number of executions.

    init_debug_table : int
        Initial Position Line of Debug Table in IR file.

        This debug table start with: !0.

    number_executions_worst_path : float
        Number of executions in total worst path.

        This number is the sum of all executions number of basic blocks.

        This attribute is float because avoid in dynamic calculation, realize a lot of conversations of int to float.

        Example: Worst Path -> BB1 + BB3 + BB4 -> 1 + 20 + 1 -> 22
    """

    def __init__(self) -> None:
        # All content of .ll file
        self.ir = []
        # All content of .dot callgraph file
        self.call_graph = []
        # Relationship between IR index and all file information
        # Example with means of values: {'index_filename': 2, 'filename': 'Desktop\\\\wcet_project\\\\header_file.h', 'directory': 'C:\\Users\\Marcus\\', 'checksum': '7bdd5928b1f3a6c967a6ea18142b9bc3'}
        self.all_user_project_files = []
        # Relationship between IR file index and loop index
        # Example with means of values: {'index_filename': 14, 'line_source_code': 14, 'index_ir': 185, 'line_ir_code': 273}
        self.mapping_loop_lines = []
        # Relationship between IR loop index and loop bound
        # Example: {273: 50, 294: 10, 354: 20}
        self.mapping_loop_bound = {}
        # Relationship between function name and line in IR file. Example: {'sprintf': 46}
        self.mapping_important_functions_lines = {}
        self.mapping_void_functions_lines = {}
        # All function name in post order. Example: ['llvm.va_end', '__stdio_common_vfscanf', ...]
        self.function_name_post_order = []
        # All functions, and its relationship between basic blocks name of worst path and number of executions
        self.worst_path_basic_block = {}
        # Initial Position Line of Debug Table in IR file
        self.init_debug_table = 0
        # Number of executions in total worst path.
        self.number_executions_worst_path = 0.0


    def __str__(self) -> str:
        ir_flag = False
        call_graph_flag = False
        
        if(self.ir != []):
             ir_flag = True
        if(self.call_graph != []):
             call_graph_flag = True

        return "*** Intermediate Values ***" + \
               "\nIR: " + str(ir_flag) + \
               "\nCall Graph: " + str(call_graph_flag) + \
               "\nNumber execututions Worst Path: " + str(self.number_executions_worst_path)


    # Getters
    def get_ir(self) -> list:
        return self.ir

    def get_call_graph(self) -> list:
        return self.call_graph

    def get_all_user_project_files(self, index_file: int = -1):
        if (index_file == -1):
            return self.all_user_project_files
        else:
            return self.all_user_project_files[index_file]

    def get_mapping_loop_lines(self, index_loop: int = -1) :
        # By default, if index isn't specified, return all
        if (index_loop == -1):
            return self.mapping_loop_lines
        else:
            return self.mapping_loop_lines[index_loop]

    def get_mapping_loop_bound(self, index_loop: int = -1) :
        # By default, if index isn't specified, return all
        if (index_loop == -1):
            return self.mapping_loop_bound
        else:
            return self.mapping_loop_bound[index_loop]

    def get_mapping_important_functions_lines(self, index_function: str = -1) :
        # By default, if index isn't specified, return all
        if (index_function == -1):
            return self.mapping_important_functions_lines
        else:
            return self.mapping_important_functions_lines[index_function]

    def get_mapping_void_functions_lines(self, index_function: str = -1) :
        # By default, if index isn't specified, return all
        if (index_function == -1):
            return self.mapping_void_functions_lines
        else:
            return self.mapping_void_functions_lines[index_function]

    def get_function_name_post_order(self, index_function: int = -1) :
        # By default, if index isn't specified, return all
        if (index_function == -1):
            return self.function_name_post_order
        else:
            return self.function_name_post_order[index_function]

    def get_worst_path_basic_block(self, function_name: str) -> list:
        return self.worst_path_basic_block[function_name]

    def get_all_worst_path_basic_block(self) -> dict:
        return self.worst_path_basic_block

    def get_init_debug_table(self) -> int:
        return self.init_debug_table

    def get_number_executions_worst_path(self) -> int:
        return self.number_executions_worst_path

    # Setters
    def set_ir(self, ir: list) -> None:
        self.ir = ir

    def set_call_graph(self, call_graph: list) -> None:
        self.call_graph = call_graph

    def set_all_user_project_files(self, all_user_project_files: list) -> None:
        self.all_user_project_files.append(all_user_project_files)

    def set_mapping_loop_lines(self, mapping_loop: dict) -> None:
        self.mapping_loop_lines.append(mapping_loop)

    def set_mapping_loop_bound(self, index_loop: int, loop_bound: int) -> None:
        self.mapping_loop_bound[index_loop] = loop_bound

    def set_mapping_important_functions_lines(self, function_name: str, line: int) -> None:
        self.mapping_important_functions_lines[function_name] = line

    def set_mapping_void_functions_lines(self, function_name: str, line: int) -> None:
        self.mapping_void_functions_lines[function_name] = line

    def set_function_name_post_order(self, function_name: str) -> None:
        self.function_name_post_order.append(function_name)

    def set_worst_path_basic_block(self, function_name: str, name: str, number_executions: int) -> None:
        if function_name in self.worst_path_basic_block:
            self.worst_path_basic_block[function_name].append(
                (name, number_executions))
        else:
            self.worst_path_basic_block[function_name] = [
                (name, number_executions)]

    def set_init_debug_table(self, line: int) -> None:
        self.init_debug_table = line

    def increment_number_executions_worst_path(self, number_executions: int) -> None:
        self.number_executions_worst_path += number_executions
