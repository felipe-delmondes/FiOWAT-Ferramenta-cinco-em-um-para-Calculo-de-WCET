import subprocess


def create_ir(project, intermediate_values):
    '''
    Create file in Intermediate Representation (IR), whose extension is ".ll"

    Its directory is same of main file of project you analyze


    Update this attributes of intermediate values:

    - ir : list
        All lines of ".ll file". Contains information in Intermediate Representation


    Parameters
    ----------
    project : UserProject
        Current user project

    intermediate_values : IntermediateValues
        Store all values to next steps

    Returns
    -------
        None
    '''
    print("Creating IR file...", end=" ")
    directory_c = project.get_input_directory() + project.get_main_file_name()
    directory_ll = project.get_output_directory() + project.get_main_file_name()

    command_raw = "\"" + project.get_llvm_path() + "clang\" -emit-llvm -S -gline-tables-only --target=" + project.get_triple_target(
    ) + " -mmcu=" + project.get_microcontroller_unit() + " \"" + directory_c + ".c\" -o \"" + directory_ll + ".ll\""

    subprocess.Popen(command_raw, shell=True).wait()

    try:
        file = open(directory_ll + ".ll", "r")
        ir = file.readlines()
        intermediate_values.set_ir(ir)
        file.close()
        print("\33[42mDone\33[0m")
    except OSError:
        print("\33[41mError! Unable to create IR file\33[0m.")
        print("\33[1mCommand entered:\33[0m " + command_raw)
        exit(1)


def create_call_graph(project, intermediate_values) -> list:
    '''
    Create call graph from ".ll file". This call graph is in dot format


    Update this attributes of intermediate values:

    - call_graph : list
        Contain all lines about call graph dot file


    Parameters
    ----------
    project : UserProject
        Current user project

    intermediate_values : IntermediateValues
        Store all values to next steps


    Returns
    -------
        None
    '''
    print("Creating call graph file...", end=" ")
    directory = project.get_output_directory() + project.get_main_file_name()
    command_raw = "\"" + project.get_llvm_path(
    ) + "opt\" -f -passes=dot-callgraph --disable-output \"" + directory + ".ll\""

    try:
        subprocess.Popen(command_raw, shell=True).wait()
    except OSError:
        print("\33[41mError! Unable to create dot file\33[0m.")
        print("\33[1mCommand entered:\33[0m " + command_raw)
        exit(1)

    try:
        file = open(directory + ".ll.callgraph.dot", "r")
        call_graph = file.readlines()
        intermediate_values.set_call_graph(call_graph)
        file.close()
        print("\33[42mDone\33[0m")
    except OSError:
        print("\33[41mError! Unable to read dot file\33[0m.")
        exit(1)




# ----------------------------------#
#           DEPRECATED              #
# ----------------------------------#
#An opt pass was developed by the team that allows direct mapping



# def create_instrumented_executable(project) -> None:
#     '''
#     Create instrumented executable of C file. Its name is main project name + "_instr".

#     This instrumentation insert counters in executable file (Coverage Report).

#     Just execute this program to generate "default.profraw" file. This file contain number of executions of each source code basic block.


#     Parameters
#     ----------
#     project : UserProject
#         Current user project


#     Returns
#     -------
#         None
#     '''
#     directory_c = project.get_input_directory() + project.get_main_file_name()
#     directory_exe = project.get_output_directory() + project.get_main_file_name()
#     command_raw = "\"" + project.get_llvm_path() + "clang\" -fprofile-instr-generate -fcoverage-mapping -mllvm -runtime-counter-relocation \"" + \
#         directory_c + ".c\" -o \"" + directory_exe + "_instr.exe\""

#     subprocess.Popen(command_raw, shell=True).wait()

#     print("Instrumented program created!")


# def create_profdata(project) -> None:
#     '''
#     Convert raw data in profile data.

#     Use "default.profraw" and create "default.profdata"


#     Prerequisites:

#     - create_instrumented_executable()

#     - Execute instrumented program


#     Parameters
#     ----------
#     project : UserProject
#         Current user project


#     Returns
#     -------
#         None
#     '''
#     command_raw = "\"" + project.get_llvm_path() + "llvm-profdata\" merge -sparse \"" + project.get_output_directory() + \
#         "default.profraw\" -o \"" + project.get_output_directory() + "default.profdata\""

#     subprocess.Popen(command_raw, shell=True).wait()


# def create_html_coverage_report(project) -> None:
#     '''
#     Generate human-readable coverage report.

#     Use "default.profdata" and create "coverage.html".

#     It's possible see execution number of each line of user source code.


#     Prerequisites:

#     - create_instrumented_executable()

#     - Execute instrumented program

#     - create_profdata()


#     Parameters
#     ----------
#     project : UserProject
#         Current user project


#     Returns
#     -------
#         None
#     '''
#     command_raw = "\"" + project.get_llvm_path() + "llvm-cov\" show -format=html -instr-profile=\"" + project.get_output_directory() + "default.profdata\" \"" + \
#         project.get_output_directory() + project.get_main_file_name() + "_instr.exe\" > \"" + \
#         project.get_output_directory() + "Coverage Report.html\""

#     subprocess.Popen(command_raw, shell=True).wait()

#     print("HTML coverage report created!")


# def create_lcov_coverage(project) -> None:
#     '''
#     Generate machine-readable coverage report.

#     Use "default.profdata" and create "coverage.lcov".

#     Create smaller file, and register branch counters, line counters, file counters, and so one.


#     Prerequisites:

#     - create_instrumented_executable()

#     - Execute instrumented program

#     - create_profdata()


#     Parameters
#     ----------
#     project : UserProject
#         Current user project


#     Returns
#     -------
#         None
#     '''
#     command_raw = "\"" + project.get_llvm_path() + "llvm-cov\" export -format=lcov -instr-profile=\"" + project.get_output_directory() + "default.profdata\" \"" + \
#         project.get_output_directory() + project.get_main_file_name() + \
#         "_instr.exe\" > \"" + project.get_output_directory() + "coverage.lcov\""

#     subprocess.Popen(command_raw, shell=True).wait()