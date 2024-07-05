from os.path import split, join, isabs


# If necessary change annotation's standard, just change this "constant"
ANNOTATIONS = "//@"


def read_file_information(count: int, line: str) -> dict:
    '''
    Read all the information about source code developed by programmers.


    Parameters
    ----------
    count : int
        Index number, for example: 13 => !13 in debug table of .ll file

    line: string
        Informations about one file


    Returns
    -------
    all_user_project_files : dict
        Dictionary store all information about information user files indexed.

        Example: {'index_filename': 2, 'filename': 'Desktop\\\\wcet_project\\\\header_file.h', 'directory': 'C:\\Users\\Marcus\\', 'checksum': '7bdd5928b1f3a6c967a6ea18142b9bc3'}
    '''
    # If found empthy directory, It's means that file is standard library
    if (line.find("directory: \"\"") != -1):
        return

    # Read all fields of line
    open_double_quotes = 0
    field = []
    temp = []
    character = 0
    index = 0

    while (line[character] != "\n"):
        # Each field start and finish using ", so It's possible obtain its values just found this character
        if (line[character] == '\"'):
            open_double_quotes = not open_double_quotes
            # If is double quotes closed, so write the content in final list
            if (not open_double_quotes):
                field.append(''.join(temp))
                index += 1
                temp.clear()

        # If the position is between "", so write the content
        if (open_double_quotes):
            # Prevents insertion of double quoted in final content
            if (line[character] != '\"'):
                temp.append(line[character])

        character += 1

    #
    # Correct directory. Because LLVM sometimes join filename and directory, or repeat them
    #
    # Separates the file name from its directory
    # Separate filename and directory. Example: Benchmark/multi-path/gdc.c  ->  Benchmark/multi-path/ ; gdc.c
    pair_directory_filename = split(field[0])

    # CASE 1: Just filename has directory
    if (field[1] == ''):
        directory = pair_directory_filename[0]

    # CASE 2: Just directory field has directory
    elif (pair_directory_filename[0] == ''):
        directory = field[1]

    # CASE 3: filename and directory have directory, but different. So use filename directory
    elif (isabs(pair_directory_filename[0])):
        directory = pair_directory_filename[0]

    # CASE 4: Separeted directory. So it's necessary concatenate both directory
    else:
        directory = join(field[1], '') + join(pair_directory_filename[0], '')

    return {'index_filename': count, 'filename': pair_directory_filename[1], 'directory': join(directory, ''), 'checksum': field[2]}


def find_loop_content(line_content: str) -> int:
    '''
    Find where is loop information in debug table.


    Parameters
    ----------
    line_content : str
        Line under analysis. Example: !184 = distinct !{!184, !177, !185, !186}


    Returns
    -------
    index_loop_information_in_debug_table : int
        Code where find loop information in debug table. Example: 177
    '''
    # The content of loop information is like this: !184 = distinct !{!184, !177, !185, !186}
    # The second value is the number of line contains the line number and file source code of loop
    position = line_content.find(",")
    position += 3
    index_loop_information_in_debug_table = ""
    # Convert string to int
    while (line_content[position].isdigit()):
        index_loop_information_in_debug_table += line_content[position]
        position += 1
    return int(index_loop_information_in_debug_table)


def read_line(line_content: str) -> int:
    '''
    Read line information in debug table and find source code line of loop.


    Parameters
    ----------
    line_content : str
        Line under analysis. Example: !177 = !DILocation(line: 14, scope: !178)


    Returns
    -------
    line_source_code : int
        Line with information about which line in source code has init of loop.
    '''
    # The content of loop information is like this: !177 = !DILocation(line: 14, scope: !178)
    # The first value correspond begin of loop. The second value is a index about other debug line contains the filename
    position = line_content.find("line:")

    # The IR was generated without debug flag, abort the analysis
    if (position == -1):
        # If there are instrumentation in IR file add after this generation, so ignore this information
        if (line_content.find("llvm.loop.mustprogress") != -1):
            print(
                "\33[41mError! The \".ll file\" was generated without debug table!\33[0m")
            print(
                "Please, use this flag in clang compilation process: -gline-tables-only")
            exit(1)
        else:
            return -1

    position += 6
    line_source_code = ""
    # Convert string to int
    while (line_content[position].isdigit()):
        line_source_code += line_content[position]
        position += 1
    return int(line_source_code)


def read_scope(line_content: str) -> int:
    '''
    Read line information in debug table and find scope of loop.


    Parameters
    ----------
    line_content : str
        Line under analysis. Example: !177 = !DILocation(line: 14, scope: !178)


    Returns
    -------
    pointer_to_filename : int
        Line with information about scope of loop, to look up in debug table.
    '''
    # The content of loop information is like this: !177 = !DILocation(line: 14, scope: !178)
    # The first value correspond begin of loop. The second value is a index about other debug line contains the filename
    position = line_content.find("scope:")
    position += 8
    pointer_to_filename = ""
    # Convert string to int
    while (line_content[position].isdigit()):
        pointer_to_filename += line_content[position]
        position += 1
    return int(pointer_to_filename)


def read_file(line_content: str) -> int:
    '''
    Read line information in debug table and find file of loop.


    Parameters
    ----------
    line_content : str
        Line under analysis. Example: !178 = distinct !DILexicalBlock(scope: !179, file: !14, line: 13)


    Returns
    -------
    index_filename : int
        Line with information about file of loop.
    '''
    # The content of loop information is like this: !178 = distinct !DILexicalBlock(scope: !179, file: !14, line: 13)
    # The most important value is "file", but in this case, only necessary save this index
    position = line_content.find("file:")
    position += 7
    index_filename = ""
    # Convert string to int
    while (line_content[position].isdigit()):
        index_filename += line_content[position]
        position += 1
    return int(index_filename)


def loop_mapping(intermediate_values) -> None:
    '''
    Search all the correspondences loops in IR with loops in source code.

    Additional function is find which line begin debug table in .ll file.


    Update this attributes of intermediate values:

    - all_user_project_files : dict
        Information about user files and its IR metadata.

        Example: {'index_filename': 2, 'filename': 'Desktop\\\\wcet_project\\\\header_file.h', 'directory': 'C:\\Users\\Marcus\\', 'checksum': '7bdd5928b1f3a6c967a6ea18142b9bc3'}

    - mapping_loop_lines : dict
        Relationship between user file and loop IR line.

        Example: {'index_filename': 14, 'line_source_code': 14, 'index_ir': 185, 'line_ir_code': 273}


    Prerequisites:

    - create_ir()


    Parameters
    ----------
    intermediate_values : IntermediateValues
        All intermediate information obtained by pre processing


    Returns
    -------
        None
    '''
    print("Mapping loops...", end=" ")

    ir = intermediate_values.get_ir()

    # Temporal list
    loop_index_table = []
    loop_line_ir = []
    position_debug_line_table = 0
    line_ir_code_index = 0

    # Search all loops in the IR
    for i, line in enumerate(ir):
        # If found "br", It's means there are possibility end of basic block with loop
        if (line[0:4] == "  br"):
            temp = line.find("!llvm.loop")

            # If have a match with substring "!llvm.loop", so...
            if (temp != -1):
                # Obtain the position of "!llvm.loop" and jump this word, to obtain the index of Debug Line Table about this loop
                loop_index_table.append(int(line[temp + 12:]))
                # Obtain number line of loop in ir
                loop_line_ir.append(i)

        # If start Debug Line Table, stop the search in main table
        elif (line[0:2] == "!0"):
            position_debug_line_table = ir.index(line)
            intermediate_values.set_init_debug_table(position_debug_line_table)
            break

    # If a table is very large, it's slight fast using a new for with different if-else clauses
    count = 0
    for line in range(position_debug_line_table, len(ir)):

        # Found all source codes developed by programmers
        if (ir[line].find("!DIFile") != -1):
            temp = read_file_information(count, ir[line])

            # Prevents values Null to insert in final list, it's occours because standard libraly generates this result
            if (temp != None):
                intermediate_values.set_all_user_project_files(temp)

        # Find all information about loops
        elif (len(loop_index_table) > 0):
            if (count == loop_index_table[0]):
                loop_index_table.pop(0)

                # Find the line content of loop
                line_under_analysis = ir[position_debug_line_table +
                                         find_loop_content(ir[line])]

                # Extract informations about loop
                line_source_code = read_line(line_under_analysis)
                # Prevent add loop bound of instrumentation
                if (line_source_code != -1):
                    pointer_to_filename = read_scope(line_under_analysis)
                    index_filename = read_file(
                        ir[position_debug_line_table + pointer_to_filename])

                    # Store all this metadata in DTO
                    intermediate_values.set_mapping_loop_lines(
                        {'index_filename': index_filename,
                         'line_source_code': line_source_code,
                         'index_ir': count,
                         'line_ir_code': loop_line_ir[line_ir_code_index]})
                line_ir_code_index += 1
        count += 1
    print("\33[42mDone\33[0m")


def loop_analyzer(filename: str, line: str, line_number: int) -> int:
    '''
    Try find loop bound of loop in source code

    Parameters
    ----------
    filename : str
        Name of current filename under analysys. Example: quatum.c

    line : str
        Current line under analysis. Example: "    for(i = 0; i < 100; i++){"

    line_number : int
        Number of line in source code file. Example: 12

    Returns
    -------
    bound : int
        The maximum value of loop bound. Example: 30
    '''
    bound = None

    # Remove all blank space and tab of lines
    line = line.replace(' ', '')
    line = line.replace('\t', '')

    # Just look up by "for"
    if (line[0:4] == "for("):
        position = 4

        initial_value = ""
        max_value = ""
        increment = ""
        conditional = ""

        # Read the initial value
        while (line[position] != '='):
            # If find void for. Example: for(;;;), so interrupt the program
            if (line[position] == ')'):
                print("\33[41mError! It is not possible find loop bound!\33[0m")
                print("File: " + filename)
                print("Line " + str(line_number + 1) + ": " + line)
                exit(1)
            position += 1
        position += 1

        # Check if initial value is a constant
        if (line[position].isdigit()):
            while (line[position] != ';'):
                initial_value += line[position]
                position += 1
            initial_value = int(initial_value)
        else:
            initial_value = ''

        # Prevent error by for breaked in 3 parts. Example: for(i=0;
        position += 1
        if (line[position] == '\n'):
            print("\33[41mError! It is not possible find loop bound!\33[0m")
            print("File: " + filename)
            print("Line " + str(line_number + 1) + ": " + line)
            exit(1)

        # Read the conditional and max value
        if (line[position].isdigit()):  # Example: 5>i
            # Read max value
            max_value = line[position]
            position += 1
            while (line[position].isdigit()):
                max_value += line[position]
                position += 1
            max_value = int(max_value)

            # Read the conditional
            while (line[position] == '>' or line[position] == '<' or line[position] == '='):
                conditional += line[position]
                position += 1

        else:  # Example: i<5
            # Jump the iterator
            while (not (line[position] == '>' or line[position] == '<' or line[position] == '=')):
                position += 1

            # Read the conditional
            while (line[position] == '>' or line[position] == '<' or line[position] == '='):
                conditional += line[position]
                position += 1

            # Read the max value
            if (line[position].isdigit()):
                while (line[position].isdigit()):
                    max_value += line[position]
                    position += 1
                max_value = int(max_value)
            # The conditional use constant
            else:
                max_value == ''

        while (line[position] != ';'):
            position += 1
        position += 1

        # Prevent error by for breaked in 2 parts. Example: for(i=0; i<5
        if (line[position] == '\n'):
            print("\33[41mError! It is not possible find loop bound!\33[0m")
            print("File: " + filename)
            print("Line " + str(line_number + 1) + ": " + line)
            exit(1)

        # Read the increment
        while (line[position] != '+' and line[position] != '-' and line[position] != ')'):
            position += 1
        if (line[position] == '+' and line[position + 1] == '+'):
            increment = "++"
        elif (line[position] == '-' and line[position + 1] == '-'):
            increment = "--"

        # Check the pattern of "FOR"
        if (increment != '' and max_value != '' and initial_value != ''):
            if (increment == "++"):
                if (max_value >= initial_value and conditional == "<"):
                    bound = max_value - initial_value
                elif (max_value >= initial_value and conditional == "<="):
                    bound = max_value - initial_value + 1

            elif (increment == "--" and max_value != '' and initial_value != ''):
                if (max_value <= initial_value and conditional == ">"):
                    bound = initial_value - max_value
                elif (max_value <= initial_value and conditional == ">="):
                    bound = initial_value - max_value + 1

    # Advert the user about the calculated loop bound
    if (bound is None):
        # If it is not possible to calculate the loop bound, so interrupt the pipeline
        print("\33[41mError! It is not possible find loop bound!\33[0m")
        print("File: " + filename)
        print("Line " + str(line_number + 1) + ": " + line)
        exit(1)
    else:
        print("\33[43mLoop bound calculated: " + str(bound) + " \33[0m")
        print("File: " + filename)
        print("Line " + str(line_number + 1) + ": " + line)
        return bound


def loop_bounding(intermediate_values) -> None:
    '''
    Read source code and obtain the loop bound in annotation and correlate with IR line of .ll file.


    Update this attributes of intermediate values:

    - mapping_loop_bound : dict 
        Relationship between line in IR code and loop bound.

        Example: {273: 50, 294: 10, 354: 20}


    Prerequisites:

    - create_ir()

    - loop_mapping()


    Parameters
    ----------
    intermediate_values : IntermediateValues
        All intermediate information obtained by pre processing


    Returns
    -------
        None
    '''
    # Open file by file, to find all annotations
    print("Looking for loop bounds...", end=" ")
    last_position = 0
    for filename in intermediate_values.get_all_user_project_files():
        if (filename['filename'].find(":") == -1):
            file = open(filename['directory'] + filename['filename'], "r")
        else:
            # Some filename are complete directory
            file = open(filename['filename'], "r")
        source_code = file.readlines()

        # Find all loops in that file
        for i in range(last_position,
                       len(intermediate_values.get_mapping_loop_lines())):
            # Retrieve the value of loop bound in code
            if (intermediate_values.get_mapping_loop_lines()[i]['index_filename'] == filename['index_filename']):
                temp = intermediate_values.get_mapping_loop_lines()[
                    i]['line_source_code'] - 1
                position = source_code[temp].find(ANNOTATIONS)
                position += 3
                temp2 = ""
                # Convert string to int
                while (source_code[temp][position].isdigit()):
                    temp2 += source_code[temp][position]
                    position += 1

                # Prevent erro if user forget put the annotation in source code
                if (temp2 == ''):
                    # Try find loop bound
                    temp2 = loop_analyzer(
                        filename['filename'],
                        source_code[temp],
                        temp)

                temp2 = int(temp2)
                intermediate_values.set_mapping_loop_bound(
                    intermediate_values.get_mapping_loop_lines()[i]['line_ir_code'], temp2)
            # If find all loops, jumps to next file
            else:
                last_position = i
                break

        file.close()
    print("\33[42mDone\33[0m")


def find_function_name(line_content: str) -> str:
    '''
    Find function name.


    Parameters
    ----------
    line_content : str
        Line under analysis. Example: define dso_local i32 @calculadora() #0 !dbg !45 {


    Returns
    -------
    function_name : str
        Name of function. Example: printf
    '''
    function_name = ""
    # The function name start with "@" character. This means something global
    column = line_content.find("@") + 1
    # Read all content of function name. Example of line: define linkonce_odr dso_local i32 @sprintf(ptr noundef %0, ptr noundef %1, ...) #0 comdat !dbg !46 {
    while (line_content[column] != "("):
        function_name += line_content[column]
        column += 1
    return function_name


def functions_mapping(intermediate_values) -> None:
    '''
    Find all lines about functions name in ".ll file" and storage its lines.

    Also, categorize "important functions" -> Functions with instructions.

    And "void functions" -> Function without instructions.


    Update this attributes of intermediate values:

    - mapping_important_functions_lines : dict
        Relationship between functions name and IR line.

        Example: {'sprintf': 46}

    - mapping_void_functions_lines : dict
        Relationship between functions name and IR line.

        Example: {'rand': 112}


    Prerequisites:

    - create_ir()


    Parameters
    ----------
    intermediate_values : IntermediateValues
        All intermediate information obtained by pre processing


    Returns
    -------
        None
    '''
    print("Mapping functions in the IR...", end=" ")
    ir = intermediate_values.get_ir()

    # Read all IR
    for line in range(1, len(ir)):
        # All functions with code starts "define"
        if (ir[line][0:6] == "define"):
            intermediate_values.set_mapping_important_functions_lines(
                find_function_name(ir[line]), line + 1)
        # All functions without code starts "declare"
        elif (ir[line][0:7] == "declare"):
            intermediate_values.set_mapping_void_functions_lines(
                find_function_name(ir[line]), line + 1)
    print("\33[42mDone\33[0m")
