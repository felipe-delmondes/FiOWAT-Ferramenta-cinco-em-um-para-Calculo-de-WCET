from setup_test import *

from src.utils.create_files import create_ir, create_call_graph


class Test_create_ir(unittest.TestCase):

    # VC-165
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('subprocess.Popen')
    def test_01_non_create_file(self, mock_terminal, mock_stdout):
        intermediate_values = Mock()
        project = Mock()
        project.get_input_directory.return_value = CURRENT_DIRECTORY
        project.get_output_directory.return_value = CURRENT_DIRECTORY
        project.get_main_file_name.return_value = "nonexistfile"
        project.get_llvm_path.return_value = ""
        project.get_triple_target.return_value = ""
        project.get_microcontroller_unit.return_value = ""

        result = "Creating IR file... " + "\33[41mError! Unable to create IR file\33[0m.\n" + "\33[1mCommand entered:\33[0m " + \
            "\"clang\" -emit-llvm -S -gline-tables-only --target= -mmcu= \"" + CURRENT_DIRECTORY + "nonexistfile.c\" -o \"" + CURRENT_DIRECTORY + "nonexistfile.ll\"\n"

        with self.assertRaises(SystemExit):
            create_ir(project, intermediate_values)
        self.assertEqual(mock_stdout.getvalue(), result)

    # VC-166
    @patch('subprocess.Popen')
    def test_02_windows(self, mock_terminal):
        intermediate_values = Mock()
        project = Mock()
        project.get_input_directory.return_value = "C:\\Desktop\\Sort\\Input\\"
        project.get_output_directory.return_value = "C:\\Desktop\\Sort\\Output\\"
        project.get_main_file_name.return_value = "mergesort"
        project.get_llvm_path.return_value = ""
        project.get_triple_target.return_value = "arm-vxworks-none"
        project.get_microcontroller_unit.return_value = "arm7"

        result = "\"clang\" -emit-llvm -S -gline-tables-only --target=arm-vxworks-none -mmcu=arm7 \"C:\\Desktop\\Sort\\Input\\mergesort.c\" -o \"C:\\Desktop\\Sort\\Output\\mergesort.ll\""

        with self.assertRaises(SystemExit):
            create_ir(project, intermediate_values)
        mock_terminal.assert_called_with(result, shell=True)

    # VC-167
    @patch('subprocess.Popen')
    def test_03_linux(self, mock_terminal):
        intermediate_values = Mock()
        project = Mock()
        project.get_input_directory.return_value = "/home/joana/Documents/input program/"
        project.get_output_directory.return_value = "/home/joana/Documents/output program/"
        project.get_main_file_name.return_value = "fflush_all"
        project.get_llvm_path.return_value = "/usr/lib/llvm-16/bin/"
        project.get_triple_target.return_value = "x86_64-pc-linux"
        project.get_microcontroller_unit.return_value = "none"

        result = "\"/usr/lib/llvm-16/bin/clang\" -emit-llvm -S -gline-tables-only --target=x86_64-pc-linux -mmcu=none \"/home/joana/Documents/input program/fflush_all.c\" -o \"/home/joana/Documents/output program/fflush_all.ll\""

        with self.assertRaises(SystemExit):
            create_ir(project, intermediate_values)
        mock_terminal.assert_called_with(result, shell=True)


class Test_create_call_graph(unittest.TestCase):

    # VC-168
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('subprocess.Popen')
    def test_01_non_create_file(self, mock_terminal, mock_stdout):
        intermediate_values = Mock()
        project = Mock()
        project.get_output_directory.return_value = CURRENT_DIRECTORY
        project.get_main_file_name.return_value = "nonexistfile"
        project.get_llvm_path.return_value = ""

        result = "Creating call graph file... " + \
                 "\33[41mError! Unable to read dot file\33[0m.\n"
        with self.assertRaises(SystemExit):
            create_call_graph(project, intermediate_values)
        self.assertEqual(mock_stdout.getvalue(), result)

    # VC-169
    @patch('subprocess.Popen')
    def test_02_windows(self, mock_terminal):
        intermediate_values = Mock()
        project = Mock()
        project.get_output_directory.return_value = "C:\\Desktop\\Sort\\Output\\"
        project.get_main_file_name.return_value = "mergesort"
        project.get_llvm_path.return_value = ""

        result = "\"opt\" -f -passes=dot-callgraph --disable-output \"C:\\Desktop\\Sort\\Output\\mergesort.ll\""

        with self.assertRaises(SystemExit):
            create_call_graph(project, intermediate_values)
        mock_terminal.assert_called_with(result, shell=True)

    # VC-170
    @patch('subprocess.Popen')
    def test_03_linux(self, mock_terminal):
        intermediate_values = Mock()
        project = Mock()
        project.get_output_directory.return_value = "/home/joana/Documents/output program/"
        project.get_main_file_name.return_value = "fflush_all"
        project.get_llvm_path.return_value = "/usr/lib/llvm-16/bin/"

        result = "\"/usr/lib/llvm-16/bin/opt\" -f -passes=dot-callgraph --disable-output \"/home/joana/Documents/output program/fflush_all.ll\""

        with self.assertRaises(SystemExit):
            create_call_graph(project, intermediate_values)
        mock_terminal.assert_called_with(result, shell=True)


# ----------------------------------#
#           DEPRECATED              #
# ----------------------------------#
# An opt pass was developed by the team that allows direct mapping


# class Test_create_instrumented_executable(unittest.TestCase):

#     #VC-171
#     @patch('subprocess.Popen')
#     def test_01_windows(self, mock_terminal):
#         project = Mock()
#         project.get_input_directory.return_value = "C:\\Desktop\\Sort\\Input\\"
#         project.get_output_directory.return_value = "C:\\Desktop\\Sort\\Output\\"
#         project.get_main_file_name.return_value = "mergesort"
#         project.get_llvm_path.return_value = ""

#         result = "\"clang\" -fprofile-instr-generate -fcoverage-mapping -mllvm -runtime-counter-relocation \"C:\\Desktop\\Sort\\Input\\mergesort.c\" -o \"C:\\Desktop\\Sort\\Output\\mergesort_instr.exe\""

#         create_instrumented_executable(project)
#         mock_terminal.assert_called_with(result, shell=True)

#     #VC-172
#     @patch('subprocess.Popen')
#     def test_02_linux(self, mock_terminal):
#         project = Mock()
#         project.get_input_directory.return_value = "/home/joana/Documents/input program/"
#         project.get_output_directory.return_value = "/home/joana/Documents/output program/"
#         project.get_main_file_name.return_value = "fflush_all"
#         project.get_llvm_path.return_value = "/usr/lib/llvm-16/bin/"

#         result = "\"/usr/lib/llvm-16/bin/clang\" -fprofile-instr-generate -fcoverage-mapping -mllvm -runtime-counter-relocation \"/home/joana/Documents/input program/fflush_all.c\" -o \"/home/joana/Documents/output program/fflush_all_instr.exe\""

#         create_instrumented_executable(project)
#         mock_terminal.assert_called_with(result, shell=True)


# class Test_create_profdata(unittest.TestCase):

#     #VC-173
#     @patch('subprocess.Popen')
#     def test_01_windows(self, mock_terminal):
#         project = Mock()
#         project.get_output_directory.return_value = "C:\\Desktop\\Sort\\Output\\"
#         project.get_llvm_path.return_value = ""

#         result = "\"llvm-profdata\" merge -sparse \"C:\\Desktop\\Sort\\Output\\default.profraw\" -o \"C:\\Desktop\\Sort\\Output\\default.profdata\""

#         create_profdata(project)
#         mock_terminal.assert_called_with(result, shell=True)

#     #VC-174
#     @patch('subprocess.Popen')
#     def test_02_linux(self, mock_terminal):
#         project = Mock()
#         project.get_output_directory.return_value = "/home/joana/Documents/output program/"
#         project.get_llvm_path.return_value = "/usr/lib/llvm-16/bin/"

#         result = "\"/usr/lib/llvm-16/bin/llvm-profdata\" merge -sparse \"/home/joana/Documents/output program/default.profraw\" -o \"/home/joana/Documents/output program/default.profdata\""

#         create_profdata(project)
#         mock_terminal.assert_called_with(result, shell=True)


# class Test_create_html_coverage_report(unittest.TestCase):

#     #VC-175
#     @patch('subprocess.Popen')
#     def test_01_windows(self, mock_terminal):
#         project = Mock()
#         project.get_output_directory.return_value = "C:\\Desktop\\Sort\\Output\\"
#         project.get_main_file_name.return_value = "mergesort"
#         project.get_llvm_path.return_value = ""

#         result = "\"llvm-cov\" show -format=html -instr-profile=\"C:\\Desktop\\Sort\\Output\\default.profdata\" \"C:\\Desktop\\Sort\\Output\\mergesort_instr.exe\" > \"C:\\Desktop\\Sort\\Output\\Coverage Report.html\""

#         create_html_coverage_report(project)
#         mock_terminal.assert_called_with(result, shell=True)

#     #VC-176
#     @patch('subprocess.Popen')
#     def test_02_linux(self, mock_terminal):
#         project = Mock()
#         project.get_output_directory.return_value = "/home/joana/Documents/output program/"
#         project.get_main_file_name.return_value = "fflush_all"
#         project.get_llvm_path.return_value = "/usr/lib/llvm-16/bin/"

#         result = "\"/usr/lib/llvm-16/bin/llvm-cov\" show -format=html -instr-profile=\"/home/joana/Documents/output program/default.profdata\" \"/home/joana/Documents/output program/fflush_all_instr.exe\" > \"/home/joana/Documents/output program/Coverage Report.html\""

#         create_html_coverage_report(project)
#         mock_terminal.assert_called_with(result, shell=True)


# class Test_create_lcov_coverage(unittest.TestCase):

#     #VC-177
#     @patch('subprocess.Popen')
#     def test_01_windows(self, mock_terminal):
#         project = Mock()
#         project.get_output_directory.return_value = "C:\\Desktop\\Sort\\Output\\"
#         project.get_main_file_name.return_value = "mergesort"
#         project.get_llvm_path.return_value = ""

#         result = "\"llvm-cov\" export -format=lcov -instr-profile=\"C:\\Desktop\\Sort\\Output\\default.profdata\" \"C:\\Desktop\\Sort\\Output\\mergesort_instr.exe\" > \"C:\\Desktop\\Sort\\Output\\coverage.lcov\""

#         create_lcov_coverage(project)
#         mock_terminal.assert_called_with(result, shell=True)

#     #VC-178
#     @patch('subprocess.Popen')
#     def test_02_linux(self, mock_terminal):
#         project = Mock()
#         project.get_output_directory.return_value = "/home/joana/Documents/output program/"
#         project.get_main_file_name.return_value = "fflush_all"
#         project.get_llvm_path.return_value = "/usr/lib/llvm-16/bin/"

#         result = "\"/usr/lib/llvm-16/bin/llvm-cov\" export -format=lcov -instr-profile=\"/home/joana/Documents/output program/default.profdata\" \"/home/joana/Documents/output program/fflush_all_instr.exe\" > \"/home/joana/Documents/output program/coverage.lcov\""

#         create_lcov_coverage(project)
#         mock_terminal.assert_called_with(result, shell=True)

#     #VC-179
#     @patch('sys.stdout', new_callable=io.StringIO)
#     @patch('subprocess.Popen')
#     def test_03_without_print(self, mock_terminal, mock_stdout):
#         project = Mock()
#         project.get_output_directory.return_value = ""
#         project.get_main_file_name.return_value = "nonexistingprogram"
#         project.get_llvm_path.return_value = ""

#         create_lcov_coverage(project)
#         self.assertEqual(mock_stdout.getvalue(), "")
if __name__ == '__main__':
    unittest.main()
