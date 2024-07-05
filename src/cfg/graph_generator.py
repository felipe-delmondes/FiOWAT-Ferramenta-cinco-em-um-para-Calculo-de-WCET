from cfg.pre_processor import *
from cfg.basic_block import BasicBlock
import copy


# Constant for name of first function in program
MAIN_FUNCTION = "main"


def mapping_nodes_and_names(
        line: str, node_and_names: dict, node_entry_point: list) -> str:
    '''
    Create a pair between function name and nodes


    Parameters
    ----------
    line : str
        Line contains node code and name function of dot file.

        Example: "	 Node0x1c93e82a2d0 [shape=record,label="{_vsprintf_l}"];"

    node_and_names : dict
        Mapping all code nodes and all functions name of dot file.

        Example: {'Node0x1c93e829a50': 'vsprintf', 'Node0x1c93e829ad0': 'sprintf', 'Node0x1c93e8296d0': '_snprintf', 'Node0x1c93e82ac50': 'llvm.va_end'}

    node_entry_point : list
        Save one code node about program entry point, usually "main function".

        Example: ['Node0x1c93e82a950']


    Returns
    -------
    node : str
        Code node of current node. For example, if this line contain this code: Node0x1c93e82a2d0, so return the same code.
    '''
    # Temporal variables
    node = ""
    name_function = ""

    # Read code node. This always start in second character and its composite by unique word. For example: Node0x1ee7381d140
    position = 1
    while (line[position] != ' '):
        node += line[position]
        position += 1

    # Read function name. This name always between {}. For example: [shape=record,label="{main}"];
    position = line.find('{') + 1
    while (line[position] != '}'):
        name_function += line[position]
        position += 1

    # Add a new pair node-name on dictionary
    node_and_names[node] = name_function

    if (name_function == MAIN_FUNCTION):
        node_entry_point.append(node)

    # For next function, it's necessary know current name
    return node


def create_node_for_callgraph(
        dot: list, line: int, nodes: dict, current_node: str) -> None:
    '''
    Create node, with all connections to child nodes, expect edges about recursion.

    The code node is found in previous function, so only missing child nodes.


    Parameters
    ----------
    dot : list 
        All lines of dot file callgraph

    line : int
        Current position in dot file

    nodes : dict
        Composed by current node and child nodes.

        Example: {'Node0x1c93e829a50': ['Node0x1c93e82a8d0'], 'Node0x1c93e829ad0': ['Node0x1c93e828f50', 'Node0x1c93e82a2d0', 'Node0x1c93e82ac50']}

    current_node : str
        Code of current node.

        Example: Node0x1c93e82ac50


    Returns
    -------
        None
    '''
    child_nodes = []
    node = ""

    # Read all child nodes. Just lines with information about relationship between two nodes has ">" character.
    # Start the readness in first child node.
    # For example: Node0x1ee7381d540 -> Node0x1ee7381d1c0;
    position = dot[line].find('>')
    while (position != -1):
        position += 2
        # Read child code node. This node is unique word and finish in ";" character
        while (dot[line][position] != ';'):
            node += dot[line][position]
            position += 1

        # Save this child node in list and search on the next line. Except recursions situation
        if (node != current_node):
            child_nodes.append(node)
        else:
            print(
                "\n\33[43mFound a recursive function. WCET will be underestimated.\33[0m")
        node = ""
        line += 1
        # Doesn't have "do while" in Python, so this line code corrects this behaviour
        position = dot[line].find('>')

    nodes[current_node] = child_nodes


def post_order(
        node_entry_point: list, nodes: dict, node_and_names: dict,
        intermediate_values) -> None:
    '''
    Traverse graph in post order, this way It's possible to find functions that do not call other uncalculated functions.


    Parameters
    ----------
    node_entry_point : list
        This callgraph doesn't have a entry point clearly defined, so it's necessary define the initial node.
        Usually is "main function".

        Example: ['Node0x1c93e82a950']

    nodes : dict
        All nodes and its child nodes.

        Example: {'Node0x1c93e829a50': ['Node0x1c93e82a8d0'], 'Node0x1c93e829ad0': ['Node0x1c93e828f50', 'Node0x1c93e82a2d0', 'Node0x1c93e82ac50']}

    node_and_names : dict
        Maintain relationship between node codes and functions name.

        Example: {'Node0x1c93e829a50': 'vsprintf', 'Node0x1c93e829ad0': 'sprintf'}

    intermediate_values : IntermediateValues
        All intermediate information obtained by pre processing


    Returns
    -------
        None
    '''
    # Constants to improve readbility
    FINAL_POSITION = -1
    FIRST_POSITION = 0

    # Save the nodes order in graph
    stack = [node_entry_point[FIRST_POSITION]]

    # Traverse all graph
    while (len(stack) > 0):
        # If node is leaf node, so you can insert in final list and remove of "node_and_names"
        if (len(nodes[stack[FINAL_POSITION]]) == 0):
            intermediate_values.set_function_name_post_order(
                node_and_names[stack[FINAL_POSITION]])
            node_and_names.pop(stack[FINAL_POSITION])
            stack.pop()
        # If node already exist in final list, so you cannot insert its. Therefore remove this child node to prevent double insertion
        elif (node_and_names.get(nodes[stack[FINAL_POSITION]][FINAL_POSITION]) == None):
            nodes[stack[FINAL_POSITION]].pop(FINAL_POSITION)
        # Traverse to child node
        else:
            stack.append(nodes[stack[FINAL_POSITION]][FINAL_POSITION])


def create_call_graph_in_post_order(intermediate_values) -> None:
    '''
    Read all callgraph functions in dot file to traverse graph using post order algorithm and generate a sequence of functions doesn't depends other functions.


    Update this attributes of intermediate values:

    - function_name_post_order : list
        List functions name in post order.

        Example: ['llvm.va_end', '__stdio_common_vfscanf', ...]


    Prerequisites:

    - create_call_graph()


    Parameters
    ----------
    intermediate_values : IntermediateValues
        All intermediate information obtained by pre processing


    Returns
    -------
        None
    '''
    print("Creating functions name list in post order...", end=" ")
    dot = intermediate_values.get_call_graph()

    # Code of node and list with all nodes it calls
    nodes = {}
    # Allow you to control which functions have already made it to final list. For this just remove the key when you put its in final list
    node_and_names = {}
    # Unique code node of program entry point. To force reference pass, I declare in list form
    node_entry_point = []

    # Find all functions using by program
    for line in range(0, len(dot)):
        # Just the function line has '[' character. For example: Node0x1ee7381d140 [shape=record,label="{main}"];
        if (dot[line].find('[') != -1):
            create_node_for_callgraph(
                dot, line + 1, nodes,
                mapping_nodes_and_names(
                    dot[line],
                    node_and_names, node_entry_point))

    # Find post order access for this callgraph
    post_order(node_entry_point, nodes, node_and_names,
               intermediate_values)
    print("\33[42mDone\33[0m")


def read_instruction(line: str) -> str:
    '''
    Read IR line and identify its instrunction. Example: add, load, call, ret


    Parameters
    ----------
    line : str
        One IR line from within basic block


    Returns
    -------
    command : str
        Final instruction in one word. If is "call instruction", so return two words: call instruction + function name
    '''
    command = ""
    # It's line of atribution. Example: %2 = alloca i32, align 4
    if (line[2] == '%'):
        # In this case, find the real command, is the next word
        column = line.find("=") + 2
    else:
        column = 2

    # Read the command
    while (line[column] != ' '):
        command += line[column]
        column += 1

    # Call instruction needs the funcion name to work
    if (command == "call"):
        command += " "

        column = line.find("@")
        # It means there are assembly inline
        if (column == -1):
            print(
                "\33[43mAssembly inline found! The CPI was not calculated accurately\33[0m")
            command = "asm"
        else:
            column += 1
            # Read the function name
            while (line[column] != '('):
                command += line[column]
                column += 1

    # Return final instruction
    return command


def define_basic_block_id(line: str) -> str:
    '''
    Return formatted basic block ID from IR line.


    Parameters
    ----------
    line : str
        IR line with basic block ID


    Returns
    -------
    bb_id : str
        Character and Basic Block ID. Example: 23 or "main;01"
    '''
    bb_id = ""
    column = 0
    # All Basic Block ID finish ":" character. Example: 102: or "calc;05":
    while (line[column] != ":"):
        bb_id += line[column]
        column += 1
    return bb_id.strip("\"")


def define_next_basic_blocks(line='') -> list:
    '''
    Find basic block ID in terminator of current basic block.

    Examples: br label %16, !dbg !219, !llvm.loop !220  ---  br i1 %18, label %19, label %33, !dbg !212


    Parameters
    ----------
    line : str, default = ''
        Last line of current basic block. If hasn't line, it means this basic block is exit point


    Returns
    -------
    next_blocks : list
        All next basic block IDs connections with current basic block. It includes empty list
    '''
    next_blocks = []
    bb_id = ""

    # Range of characters. First character isn't relevant. Example: "  br label %30, !dbg !218"
    iterator = 4
    lenght_line = len(line)

    # If hasn't content in line
    if (lenght_line == 0):
        return next_blocks

    # Read all lines
    while (iterator < lenght_line):
        # For increase performance, just compare separately each character
        if (line[iterator] == "l"):
            iterator += 1
            if (line[iterator] == "a"):
                iterator += 1
                # If it really substring...
                if (line[iterator: iterator + 3] == "bel"):
                    iterator += 5
                    # Real all next basic block ID. It finish "," character
                    while (line[iterator] != ',' and line[iterator] != '\n'):
                        bb_id += line[iterator]
                        iterator += 1
                    next_blocks.append(bb_id)
                    bb_id = ""
        iterator += 1
    return next_blocks


def update_index_basic_block(
        function: list, mapping_bb_id_and_index: dict) -> None:
    '''
    Convert from "LLVM format Basic Block ID" to "Index Position" in function list.

    Example: '%23' -> 5


    Parameters
    ----------
    function : list
        Function with all basic blocks with attribute "next_blocks" instantied

    mapping_bb_id_and_index : dict
        Pair between "LLVM format Basic Block ID" and "Index Position" of function array


    Returns
    -------
        None
    '''
    temp = []

    # Read all Basic Block of function
    for bb in function:
        temp = bb.get_next_blocks()
        # Convert each Basic Block ID by its respective index number
        for i in range(0, len(temp)):
            temp[i] = mapping_bb_id_and_index[temp[i].strip("\"")]
        # Update connections to next blocks
        bb.set_next_blocks(temp)


def define_first_basic_block_id(function_line: str, next_line: str) -> str:
    '''
    Find the first basic block ID, because it's different of other blocks.

    It hasn't separated line like: "23: ".

    To discover its value, is necessary count number of parameters declarations and plus one.

    One exception is IR file generated by us pass. In this situation there is next line with basic block name.


    Parameters
    ----------
    function_line : str
        One line of function declaration.

        Example: define dso_local i32 @main(i32 noundef %0, ptr noundef %1) #0 !dbg !195 {

    next_line : str
        Content of IR line. Because IR file process by us pass generate extra line with name of first basic block.

        Example of name is Fib_01. In original IR file generate by "canonical" LLVM there aren't this line.


    Returns
    -------
    bb_id : str
        Basic block ID formatted. Example: 3 or Fib_01
    '''
    if (next_line.find(':') != -1):
        # This is a instrumentation code, so there is name in next line
        name = ""
        for character in next_line:
            if (character == ':'):
                # Remove double quotes in first and last character
                return name.strip("\"")
            name += character
    else:
        # All variables in parameters have unique number because of SSA (Single Statement Assignment)
        SSA_index = function_line.count('%')
        return str(SSA_index + 1)


def graph_generator_post_order(intermediate_values: object, graph: dict) -> None:
    '''
    Generate a graph in a list in post order, each list has basic block in same order of ".ll file".


    Prerequisites:

    - create_ir()

    - create_call_graph()

    - loop_mapping()

    - loop_bounding()

    - functions_mapping()

    - create_call_graph_in_post_order()


    Parameters
    ----------
    intermediate_values : IntermediateValues
        All intermediate information obtained by pre processing

    graph : dict
        Basic block graph of all program


    Returns
    -------
        None
    '''
    print("Creating graph in post order...", end=" ")
    ir = intermediate_values.get_ir()

    # Storage all basic blocks about one function
    function = []

    # Mapping basic block ID and index positions
    mapping_bb_id_and_index = {}

    # Temporal variables
    line = 0
    command = ""
    # Calculate WCET per function, until reach in main function WCET
    for function_name in intermediate_values.get_function_name_post_order():
        # Some functions doesn't exist in post order, because it isn't part of the leaf node of main function
        # Or hasn't code, so its weight is 0 too
        if str(function_name) not in intermediate_values.get_mapping_important_functions_lines():
            function = []
            graph[function_name] = copy.deepcopy(function)
            continue

        # Discover where function begins
        line = intermediate_values.get_mapping_important_functions_lines(
            function_name)
        # If there are instructions...
        b = BasicBlock()
        bb_name = define_first_basic_block_id(ir[line - 1], ir[line])
        mapping_bb_id_and_index[bb_name] = 0
        b.set_id(line - 1)
        index_basic_block = 1

        # If .ll file is instrumented, so the instructions begin in next line
        if (bb_name[0].isdigit() == False):
            b.set_name(bb_name)
            line += 1

        while (True):
            # Every Basic block is separated by "br" or "ret"
            while (True):
                command = read_instruction(ir[line])
                b.set_instructions(command)

                # End of basic block and start next basic block
                if (command == "br"):
                    # If find a loop. Example:   br i1 %31, label %18, label %32, !dbg !183, !llvm.loop !184
                    if (ir[line].find("!llvm.loop") != -1):
                        b.set_number_executions(
                            intermediate_values.get_mapping_loop_bound(line))

                    # Finally, add new basic block in respective function
                    b.set_next_blocks(define_next_basic_blocks(ir[line]))
                    function.append(b)
                    b = BasicBlock()
                    line += 1
                    break
                # End of basic block and function
                elif (command == "ret"):
                    # Exit point means once execution
                    b.set_number_executions(1)
                    # Empty list means exit points
                    b.set_next_blocks(define_next_basic_blocks())
                    # Finally, add new basic block in respective function
                    function.append(b)
                    b = BasicBlock()
                    line += 1
                    break
                line += 1

            # All functions with code finish with this character
            if (ir[line][0] == '}'):
                break
            # Else, there is more basic block
            else:
                # Next line has basic block ID. Example: 16:
                line += 1
                name = define_basic_block_id(ir[line])
                mapping_bb_id_and_index[name] = index_basic_block
                b.set_id(line + 1)
                b.set_name(name)
                index_basic_block += 1
                # Next line start basic block instructions
                line += 1

        # Add function on graph
        update_index_basic_block(function, mapping_bb_id_and_index)
        graph[function_name] = copy.deepcopy(function)
        function.clear()
        mapping_bb_id_and_index.clear()
    print("\33[42mDone\33[0m")