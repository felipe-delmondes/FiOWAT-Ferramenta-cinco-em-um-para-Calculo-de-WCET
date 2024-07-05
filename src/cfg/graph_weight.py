def define_instructions_weight(project) -> dict:
    '''
    Return instructions weight of selected architecture, without using pipeline, cache or branch predictor effects.

    If there aren't an architecture, so default value is used.

    Architetures supported:

    - avr

    - x86 | x86_64

    - default


    Note: the instructions: "call llvm.dbg.declare"; "call llvm.dbg.value" and "call llvm.dbg.assign" have 0 weight.

    This instruction is used by LLVM to obtain debug information. See more information in this site: https://llvm.org/docs/SourceLevelDebugging.html#llvm-dbg-declare


    Parameters
    ----------
    project : UserProject
        Contain information about architecture, like avr or x86


    Returns
    -------
    instructions_weight : dict
        Pair between instruction name and weights (Cycles per Instruction)
    '''
    # Instructions weight of each architecture
    if (project.get_architecture() == "avr"):
        instructions_weight = {'call llvm.dbg.declare': 0, 'llvm.dbg.value': 0, 'call llvm.dbg.assign': 0, 'asm': 1,
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
    elif (project.get_architecture() == "x86" or project.get_architecture() == "x86_64"):
        instructions_weight = {'call llvm.dbg.declare': 0, 'llvm.dbg.value': 0, 'call llvm.dbg.assign': 0, 'asm': 1,
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
    # Weight obtained by measumerents
    else:
        instructions_weight = {}

    return instructions_weight
    '''
    #Substitute this template in new architecture dictionary
    {'call llvm.dbg.declare': 0, 'llvm.dbg.value': 0, 'call llvm.dbg.assign': 0, 'asm': 1,
    'add': , 'alloca': , 'and': , 'ashr': , 'bitcast': , 'br': ,
    'call': , 'extractelement': , 'extractvalue': , 'fadd': ,
    'fcmp': , 'fdiv': , 'fmul': , 'fpext': , 'fptosi': ,
    'fptoui': , 'fptrunc': , 'frem': , 'fsub': , 'getelementptr': ,
    'icmp': , 'indirectbr': , 'insertelement': , 'insertvalue': ,
    'inttoptr': , 'invoke': , 'load': , 'lshr': , 'mul': , 'or': ,
    'phi': 0, 'ptrtoint': , 'ret': , 'sdiv': , 'select': , 'sext': ,
    'shl': , 'shufflevector': , 'sitofp': , 'srem': , 'store': ,
    'sub': , 'switch': , 'trunc': , 'udiv': , 'uitofp': , 'unreachable': ,
    'unwind': , 'urem': , 'va_arg': , 'xor': , 'zext': }
    '''


def update_basic_block_weight_statically(
        function: list, instructions_weight: dict) -> None:
    '''
    Determine basic block weight by sum of individual instruction weight.

    It's impossible determine all functions weight because "call instructions" has weight undefined at the beginning of the analysis


    Parameters
    ----------
    function : list
        All basic blocks of function

    instructions_weight : dict
        Weight of each instructions (Cycles per Instruction)


    Returns
    -------
        None
    '''
    # Transverse the just one function, and calculate each basic block weight
    for basic_block in function:
        total = 0
        for instruction in basic_block.get_instructions():
            total += instructions_weight[instruction]
        basic_block.set_weight(total)


def update_weight_by_measurements(
        graph: dict, timer, main=True) -> None:
    '''
    Update basic block weight using values obtained by measurements


    Parameters
    ----------
    graph : dict
        All basic blocks of program

    timer : Dict
        Dictonary gerenated by measuring the execution time of basic blocks

    main: Bool, default=True
        Define if the blocks of the main function will have their weight updated or not. If not, the value stays zero.
        True means to consider main.


    Returns
    -------
        None
    '''
    not_covered = []
    covered = []
    for function in graph:
        for bb in range(0, len(graph[function])):
            if graph[function][bb].get_name() != "" and graph[function][bb].get_name()[0] == "#":
                _, func, block = graph[function][bb].get_name().split(";")
                if func == "main" and not main:
                    pass
                elif block not in timer.final_times[func].keys():
                    not_covered.append(block)
                else:
                    graph[function][bb].set_weight(
                        timer.final_times[func][block])
                    covered.append(block)

    if len(not_covered)+len(covered) != 0:
        cov = len(covered)/(len(not_covered)+len(covered))
        if cov < 1:
            print("\n\33[43mWarning! Block coverage achieved by the test cases was {:.2f}\33[0m".format(
                100*cov))
