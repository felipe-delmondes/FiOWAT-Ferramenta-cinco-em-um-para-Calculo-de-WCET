from setup_test import *
from src.cfg.pre_processor import read_file_information, find_loop_content, read_line, read_scope, read_file, loop_mapping, loop_analyzer, loop_bounding, find_function_name, functions_mapping
from src.utils.intermediate_values import IntermediateValues


class Test_read_file_information(unittest.TestCase):

    # VC-001
    def test_01_filename_and_directory_correct(self):
        if 'win' in sys.platform:
            line = "!1 = !DIFile(filename: \"smloop.c\", directory: \"C:\\Users\\Peter\\Desktop\\Test\", checksumkind: CSK_MD5, checksum: \"a9b8798997832a9f7b5dcb836ae3c366\")\n"
            result = {'index_filename': 10, 'filename': "smloop.c",
                      'directory': "C:\\Users\\Peter\\Desktop\\Test\\",
                      'checksum': "a9b8798997832a9f7b5dcb836ae3c366"}
            self.assertEqual(read_file_information(10, line), result)
        else:
            line = "!1 = !DIFile(filename: \"smloop.c\", directory: \"/home/maria/Documents/TCC-PES/experiments/CFG/LLVM\", checksumkind: CSK_MD5, checksum: \"a9b8798997832a9f7b5dcb836ae3c366\")\n"
            result = {
                'index_filename': 10, 'filename': "smloop.c",
                'directory':
                r"/home/maria/Documents/TCC-PES/experiments/CFG/LLVM/",
                'checksum': "a9b8798997832a9f7b5dcb836ae3c366"}
            self.assertEqual(read_file_information(10, line), result)

    # VC-002
    def test_02_directories_splitted(self):
        if 'win' in sys.platform:
            line = "!0 = !DIFile(filename: \"Desktop\\hello\\bsort100.c\", directory: \"C:\\Users\\John\", checksumkind: CSK_MD5, checksum: \"32bef3773e7a36013980e4201249215d\")\n"
            result = {'index_filename': 21, 'filename': "bsort100.c",
                      'directory': "C:\\Users\\John\\Desktop\\hello\\",
                      'checksum': "32bef3773e7a36013980e4201249215d"}
            self.assertEqual(read_file_information(21, line), result)
        else:
            line = "!0 = !DIFile(filename: \"TCC-PES/experiments/CFG/LLVM/bsort100.c\", directory: \"/home/maria/Documents\", checksumkind: CSK_MD5, checksum: \"32bef3773e7a36013980e4201249215d\")\n"
            result = {
                'index_filename': 21, 'filename': "bsort100.c",
                'directory':
                "/home/maria/Documents/TCC-PES/experiments/CFG/LLVM/",
                'checksum': "32bef3773e7a36013980e4201249215d"}
            self.assertEqual(read_file_information(21, line), result)

    # VC-003
    def test_03_two_different_directory(self):
        if 'win' in sys.platform:
            line = "!0 = !DIFile(filename: \"C:\\Users\\Walter\\Desktop\\x\\program.c\", directory: \"C:\\Users\\Walter\\source\\repos\\VS Code\\TCC-PES\", checksumkind: CSK_MD5, checksum: \"15b5e193a217391fa5e1d7bb3d22dc57\")\n"
            result = {'index_filename': 150, 'filename': "program.c",
                      'directory': "C:\\Users\\Walter\\Desktop\\x\\",
                      'checksum': "15b5e193a217391fa5e1d7bb3d22dc57"}
            self.assertEqual(read_file_information(150, line), result)
        else:
            line = "!0 = !DIFile(filename: \"/home/Lucia/Desktop/program.c\", directory: \"/home/Lucia/Documents/MyPrograms/WCET\", checksumkind: CSK_MD5, checksum: \"15b5e193a217391fa5e1d7bb3d22dc57\")\n"
            result = {'index_filename': 150, 'filename': "program.c",
                      'directory': "/home/Lucia/Desktop/",
                      'checksum': "15b5e193a217391fa5e1d7bb3d22dc57"}
            self.assertEqual(read_file_information(150, line), result)

    # VC-004
    def test_04_common_path(self):
        if 'win' in sys.platform:
            line = "!21 = !DIFile(filename: \"C:\\Users\\Walter\\Desktop\\x\\program.c\", directory: \"C:\\Users\\Walter\\source\\repos\\BlockCode\", checksumkind: CSK_MD5, checksum: \"15b5e193a217391fa5e1d7bb3d22dc57\")\n"
            result = {'index_filename': 33, 'filename': "program.c",
                      'directory': "C:\\Users\\Walter\\Desktop\\x\\",
                      'checksum': "15b5e193a217391fa5e1d7bb3d22dc57"}
            self.assertEqual(read_file_information(33, line), result)
        else:
            line = "!21 = !DIFile(filename: \"/home/maria/Documents/TCC-PES/experiments/CFG/LLVM/program.c\", directory: \"/home/maria/Documents/TCC-PES\", checksumkind: CSK_MD5, checksum: \"15b5e193a217391fa5e1d7bb3d22dc57\")\n"
            result = {
                'index_filename': 33, 'filename': "program.c",
                'directory':
                "/home/maria/Documents/TCC-PES/experiments/CFG/LLVM/",
                'checksum': "15b5e193a217391fa5e1d7bb3d22dc57"}
            self.assertEqual(read_file_information(33, line), result)

    # VC-005
    def test_05_standard_header_file(self):
        if 'win' in sys.platform:
            line = "!17 = !DIFile(filename: \"C:\\System\\Windows\\10\\Include\\stdio.h\", directory: \"\", checksumkind: CSK_MD5, checksum: \"15b5e193a217391fa5e1d7bb3d22dc57\")\n"
            self.assertEqual(read_file_information(123, line), None)
        else:
            line = "!17 = !DIFile(filename: \"/home/maria/src/stdio.h\", directory: \"\", checksumkind: CSK_MD5, checksum: \"15b5e193a217391fa5e1d7bb3d22dc57\")\n"
            self.assertEqual(read_file_information(123, line), None)

    # VC-006
    def test_06_blank_space_in_directory(self):
        if 'win' in sys.platform:
            line = "!4 = !DIFile(filename: \"smloop.c\", directory: \"C:\\Users\\Peter Vlad\\Desktop\\Test\", checksumkind: CSK_MD5, checksum: \"a9b8798997832a9f7b5dcb836ae3c366\")\n"
            result = {'index_filename': 15, 'filename': "smloop.c",
                      'directory': "C:\\Users\\Peter Vlad\\Desktop\\Test\\",
                      'checksum': "a9b8798997832a9f7b5dcb836ae3c366"}
            self.assertEqual(read_file_information(15, line), result)
        else:
            line = "!4 = !DIFile(filename: \"smloop.c\", directory: \"/home/maria/Documents/TCC LLVM/Project\", checksumkind: CSK_MD5, checksum: \"a9b8798997832a9f7b5dcb836ae3c366\")\n"
            result = {'index_filename': 15, 'filename': "smloop.c",
                      'directory': "/home/maria/Documents/TCC LLVM/Project/",
                      'checksum': "a9b8798997832a9f7b5dcb836ae3c366"}
            self.assertEqual(read_file_information(15, line), result)

    # VC-007
    def test_07_blank_space_in_filename(self):
        if 'win' in sys.platform:
            line = "!57 = !DIFile(filename: \"C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt\\quantum.h\", directory: \"C:\\Users\\Walter\\source\\repos\\VS Code\", checksumkind: CSK_MD5, checksum: \"15b5e193a217391fa5e1d7bb3d22dc57\")\n"
            result = {
                'index_filename': 666, 'filename': "quantum.h",
                'directory':
                "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt\\",
                'checksum': "15b5e193a217391fa5e1d7bb3d22dc57"}
            self.assertEqual(read_file_information(666, line), result)
        else:
            line = "!57 = !DIFile(filename: \"/home/maria/Documents/TCC LLVM/Project/quantum.h\", directory: \"/home/maria/Desktop\", checksumkind: CSK_MD5, checksum: \"15b5e193a217391fa5e1d7bb3d22dc57\")\n"
            result = {'index_filename': 666, 'filename': "quantum.h",
                      'directory': "/home/maria/Documents/TCC LLVM/Project/",
                      'checksum': "15b5e193a217391fa5e1d7bb3d22dc57"}
            self.assertEqual(read_file_information(666, line), result)

    # VC-008
    def test_08_user_header_file(self):
        if 'win' in sys.platform:
            line = "!57 = !DIFile(filename: \"Desktop\\first.h\", directory: \"C:\\Users\\Jose\", checksumkind: CSK_MD5, checksum: \"15b5e193a217391fa5e1d7bb3d22dc57\")\n"
            result = {'index_filename': 101, 'filename': "first.h",
                      'directory': "C:\\Users\\Jose\\Desktop\\",
                      'checksum': "15b5e193a217391fa5e1d7bb3d22dc57"}
            self.assertEqual(read_file_information(101, line), result)
        else:
            line = "!57 = !DIFile(filename: \"Desktop/WCET/first.h\", directory: \"/home/Joana\", checksumkind: CSK_MD5, checksum: \"15b5e193a217391fa5e1d7bb3d22dc57\")\n"
            result = {'index_filename': 101, 'filename': "first.h",
                      'directory': "/home/Joana/Desktop/WCET/",
                      'checksum': "15b5e193a217391fa5e1d7bb3d22dc57"}
            self.assertEqual(read_file_information(101, line), result)


class Test_find_loop_content(unittest.TestCase):

    # VC-009
    def test_01_normal_situation(self):
        self.assertEqual(find_loop_content(
            "!105 = distinct !{!105, !1, !104, !87}"), 1)

    # VC-010
    def test_02_less_metadata(self):
        self.assertEqual(find_loop_content("{!105, !5}"), 5)

    # VC-011
    def test_03_more_one_digits(self):
        self.assertEqual(find_loop_content(
            "!105 = distinct !{!105, !101, !104, !87}"), 101)


class Test_read_line(unittest.TestCase):

    # VC-012
    def test_01_normal_situation(self):
        self.assertEqual(
            read_line("!82 = !DILocation(line: 1, scope: !71)"), 1)

    # VC-013
    def test_02_less_metadata(self):
        self.assertEqual(read_line("(line: 77)"), 77)

    # VC-014
    def test_03_more_one_digits(self):
        self.assertEqual(
            read_line("!82 = !DILocation(line: 1475, scope: !71)"),
            1475)

    # VC-015
    def test_04_void_line(self):
        self.assertEqual(read_line(""), -1)

    # VC-016
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_05_loop_mustprogress(self, mock_stdout):
        with self.assertRaises(SystemExit):
            read_line("!4 = !{!\"llvm.loop.mustprogress\"}")
        self.assertEqual(mock_stdout.getvalue(),
                         "\33[41mError! The \".ll file\" was generated without debug table!\33[0m\nPlease, use this flag in clang compilation process: -gline-tables-only\n")


class Test_read_scope(unittest.TestCase):

    # VC-017
    def test_01_normal_situation(self):
        self.assertEqual(read_scope(
            "!78 = !DILocation(line: 3, scope: !1)"), 1)

    # VC-018
    def test_02_less_metadata(self):
        self.assertEqual(read_scope("(scope: !71)"), 71)

    # VC-019
    def test_03_more_one_digits(self):
        self.assertEqual(
            read_scope("!82 = !DILocation(line: 99, scope: !1475)"),
            1475)


class Test_read_file(unittest.TestCase):

    # VC-020
    def test_01_normal_situation(self):
        self.assertEqual(
            read_file(
                "!95 = distinct !DISubprogram(name: \"main\", scope: !72, file: !7, line: 28, type: !96, scopeLine: 28, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)"),
            7)

    # VC-021
    def test_02_less_metadata(self):
        self.assertEqual(read_file("file: !5)"), 5)

    # VC-022
    def test_03_more_one_digits(self):
        self.assertEqual(
            read_file(
                "!95 = distinct !DISubprogram(name: \"main\", scope: !72, file: !72, line: 28, type: !96, scopeLine: 28, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)"),
            72)


class Test_loop_mapping(unittest.TestCase):

    # VC-023
    def test_01_first_program(self):
        if 'win' in sys.platform:
            intermediate_values = IntermediateValues()
            file = open(INPUT_DIRECTORY + "first.ll", 'r')
            intermediate_values.set_ir(file.readlines())
            file.close()

            result_mapping_loops = [
                {'index_filename': 72, 'line_source_code': 14, 'index_ir': 86,
                 'line_ir_code': 240},
                {'index_filename': 72, 'line_source_code': 10, 'index_ir': 92,
                 'line_ir_code': 261},
                {'index_filename': 72, 'line_source_code': 33, 'index_ir': 105,
                 'line_ir_code': 316}]

            loop_mapping(intermediate_values)

            # Test debug table
            self.assertEqual(intermediate_values.get_init_debug_table(
            ), 486, msg="Error! Incorrect line of debug table init")

            # Test user project
            self.assertEqual(intermediate_values.get_all_user_project_files()[
                0]['index_filename'], 1, msg="Error! Incorrect Index Filename")
            self.assertEqual(intermediate_values.get_all_user_project_files()[
                0]['filename'], "first.c", msg="Error! Incorrect Filename")
            self.assertEqual(
                os.path.normcase(
                    intermediate_values.get_all_user_project_files()[0]
                    ['directory']),
                os.path.join(
                    os.path.normcase(
                        os.path.join(
                            os.path.dirname(__file__),
                            "input")).replace('\\', '\\\\'),
                    ''),
                msg="Error! Incorrect directory")
            self.assertEqual(
                intermediate_values.get_all_user_project_files()[
                    0]['checksum'],
                "0f5da55deaae4144daea65e434214000", msg="Error! Incorrect checksum")

            # Test loop mapping
            self.assertEqual(
                intermediate_values.get_mapping_loop_lines(),
                result_mapping_loops)

        else:
            intermediate_values = IntermediateValues()
            file = open(INPUT_DIRECTORY + "first.ll", 'r')
            intermediate_values.set_ir(file.readlines())
            file.close()

            result_mapping_loops = [
                {'index_filename': 72, 'line_source_code': 14, 'index_ir': 86,
                 'line_ir_code': 240},
                {'index_filename': 72, 'line_source_code': 10, 'index_ir': 92,
                 'line_ir_code': 261},
                {'index_filename': 72, 'line_source_code': 33, 'index_ir': 105,
                 'line_ir_code': 316}]

            loop_mapping(intermediate_values)

            # Test debug table
            self.assertEqual(intermediate_values.get_init_debug_table(
            ), 486, msg="Error! Incorrect line of debug table init")

            # Test user project
            self.assertEqual(intermediate_values.get_all_user_project_files()[
                0]['index_filename'], 1, msg="Error! Incorrect Index Filename")
            self.assertEqual(intermediate_values.get_all_user_project_files()[
                0]['filename'], "first.c", msg="Error! Incorrect Filename")
            self.assertEqual(
                os.path.normcase(
                    intermediate_values.get_all_user_project_files()[0]
                    ['directory']),
                os.path.join(
                    os.path.normcase(
                        os.path.join(
                            os.path.dirname(__file__),
                            "input")).replace('\\', '\\\\'),
                    ''),
                msg="Error! Incorrect directory")
            self.assertEqual(
                intermediate_values.get_all_user_project_files()[
                    0]['checksum'],
                "0f5da55deaae4144daea65e434214000", msg="Error! Incorrect checksum")

            # Test loop mapping
            self.assertEqual(
                intermediate_values.get_mapping_loop_lines(),
                result_mapping_loops)

    # VC-024
    def test_02_without_loop(self):
        intermediate_values = IntermediateValues()
        file = open(INPUT_DIRECTORY + "semloop.ll", 'r')
        intermediate_values.set_ir(file.readlines())
        file.close()

        loop_mapping(intermediate_values)

        # Test debug table
        self.assertEqual(intermediate_values.get_init_debug_table(
        ), 189, msg="Error! Incorrect line of debug table init")

        # Test user project
        self.assertEqual(intermediate_values.get_all_user_project_files()[
                         0]['index_filename'], 1, msg="Error! Incorrect Index Filename")
        self.assertEqual(intermediate_values.get_all_user_project_files()[
                         0]['filename'], "semloop.c", msg="Error! Incorrect Filename")
        self.assertEqual(
            os.path.normcase(
                intermediate_values.get_all_user_project_files()[0]
                ['directory']),
            os.path.join(
                os.path.normcase("C:\\Users\\Peter").replace('\\', '\\\\'),
                ''),
            msg="Error! Incorrect directory")
        self.assertEqual(
            intermediate_values.get_all_user_project_files()[0]['checksum'],
            "a9b8798997832a9f7b5dcb836ae3c366", msg="Error! Incorrect checksum")

        # Test loop mapping
        self.assertEqual(intermediate_values.get_mapping_loop_lines(), [])


class Test_loop_analyzer(unittest.TestCase):

    # VC-025
    def test_01_do_while(self):
        # To test exit(1), check the Raise: "SystemExit"
        with self.assertRaises(SystemExit):
            loop_analyzer("quantum.c", "do{", 10)

    # VC-026
    def test_02_while(self):
        with self.assertRaises(SystemExit):
            loop_analyzer("quantum.c", "while(x < 3){", 21)

    # VC-027
    def test_03_for(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for(i=0;i<100;i++){", 3), 100)

    # VC-028
    def test_04_for_with_blank_space(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for (i = 0; i < 100; i++)", 3), 100)

    # VC-029
    def test_04_for_with_parcial_annotation(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for(i = 0; i < 100; i++)\t//@", 3), 100)

    # VC-030
    def test_05_for_less_equal(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for(i = 0; i <= 100; i++)", 3), 101)

    # VC-031
    def test_06_for_greater(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for(i = 100; i > 0; i--)", 3), 100)

    # VC-032
    def test_07_for_greater_equal(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for(i = 100; i >= 0; i--)", 3), 101)

    # VC-033
    def test_08_for_initial_equal_max_value(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for(i = 0; i <= 0; i++)", 3), 1)

    # VC-034
    def test_09_for_initial_equal_max_value(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for(i = 0; i < 0; i++)", 3), 0)

    # VC-035
    def test_10_for_initial_equal_max_value(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for(i = 0; i >= 0; i--)", 3), 1)

    # VC-036
    def test_11_for_initial_equal_max_value(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for(i = 0; i > 0; i--)", 3), 0)

    # VC-037
    def test_12_for_other_increments(self):
        with self.assertRaises(SystemExit):
            loop_analyzer("quantum.c", "for(i = 100; i < 0; i-=1)", 12)

    # VC-038
    def test_13_for_other_increments(self):
        with self.assertRaises(SystemExit):
            loop_analyzer("quantum.c", "for(i = 0; i < 100; i*=2)", 101)

    # VC-039
    def test_14_for_iterator_large_name(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for(iterator=0;iterator<100;iterator++){", 3), 100)

    # VC-040
    def test_15_for_different_names(self):
        self.assertEqual(loop_analyzer(
            "quantum.c", "for(i=0;j<100;k++){", 3), 100)

    # VC-041
    def test_16_for_void(self):
        with self.assertRaises(SystemExit):
            loop_analyzer("quantum.c", "for(;;)", 666)

    # VC-042
    def test_17_for_constant_in_condition(self):
        with self.assertRaises(SystemExit):
            loop_analyzer(
                "quantum.c", "for(Index = 0;Index < NUMLENS;Index++)", 123)

    # VC-043
    def test_18_for_constant_in_condition(self):
        with self.assertRaises(SystemExit):
            loop_analyzer(
                "quantum.c", "for(Index = 0; NUMLENS >= Index; Index--){", 123)

    # VC-044
    def test_19_for_constant_in_initial(self):
        with self.assertRaises(SystemExit):
            loop_analyzer(
                "quantum.c", "for(Index = A; Index < 5; Index++){", 123)

    # VC-045
    def test_20_for_constant_in_initial(self):
        with self.assertRaises(SystemExit):
            loop_analyzer(
                "quantum.c", "for(Index = A; Index <= 5; Index--){", 123)

    # VC-046
    def test_21_no_increment(self):
        with self.assertRaises(SystemExit):
            loop_analyzer(
                "quantum.c", "for(Index = 0; NUMLENS >= Index; Index){", 123)

    # VC-047
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_22_message_loop_calculated(self, mock_stdout):
        loop_analyzer("quantum.c", "for(i=0;i<100;i++){", 3)
        self.assertEqual(
            mock_stdout.getvalue(),
            "\33[43mLoop bound calculated: 100 \33[0m\nFile: quantum.c\nLine 4: for(i=0;i<100;i++){\n")

    # VC-048
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_23_message_error(self, mock_stdout):
        with self.assertRaises(SystemExit):
            loop_analyzer("quantum.c", "for(i=0;i<100;i*=2){", 5)
        self.assertEqual(
            mock_stdout.getvalue(),
            "\33[41mError! It is not possible find loop bound!\33[0m\nFile: quantum.c\nLine 6: for(i=0;i<100;i*=2){\n")

    # VC-049
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_24_message_error_for_void(self, mock_stdout):
        with self.assertRaises(SystemExit):
            loop_analyzer("void.c", "for(;;)", 666)
        self.assertEqual(
            mock_stdout.getvalue(),
            "\33[41mError! It is not possible find loop bound!\33[0m\nFile: void.c\nLine 667: for(;;)\n")

    # VC-050
    def test_25_for_there_first_part(self):
        with self.assertRaises(SystemExit):
            loop_analyzer("incomplete.c", "for(i=0;\n", 74)

    # VC-051
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_26_message_error_for_there_first_part(self, mock_stdout):
        with self.assertRaises(SystemExit):
            loop_analyzer("incomplete.c", "\tfor(i=0; \t\n", 74)
        self.assertEqual(
            mock_stdout.getvalue(),
            "\33[41mError! It is not possible find loop bound!\33[0m\nFile: incomplete.c\nLine 75: for(i=0;\n\n")

    # VC-052
    def test_27_for_there_second_part(self):
        with self.assertRaises(SystemExit):
            loop_analyzer("incomplete2.c", "for(i=0;i<4;\n", 74)

    # VC-053
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_28_message_errorfor_there_second_part(self, mock_stdout):
        with self.assertRaises(SystemExit):
            loop_analyzer("incomplete2.c", "\tfor(i=0; i<4; \t\n", 74)
        self.assertEqual(
            mock_stdout.getvalue(),
            "\33[41mError! It is not possible find loop bound!\33[0m\nFile: incomplete2.c\nLine 75: for(i=0;i<4;\n\n")


class Test_loop_bounding(unittest.TestCase):

    # VC-054
    @patch('utils.intermediate_values.IntermediateValues')
    def test_01_first_program(self, intermediate_values):
        intermediate_values = Mock()
        intermediate_values.get_all_user_project_files.return_value = [
            {'index_filename': 1, 'filename': 'first.c',
             'directory': INPUT_DIRECTORY,
             'checksum': '2b89d349dba345bd3427ef2e63ac9aa1'},
            {'index_filename': 46, 'filename': 'first.h',
             'directory': INPUT_DIRECTORY,
             'checksum': '7bdd5928b1f3a6c967a6ea18142b9bc3'},
            {'index_filename': 72, 'filename': 'first.c',
             'directory': INPUT_DIRECTORY,
             'checksum': '2b89d349dba345bd3427ef2e63ac9aa1'}]
        intermediate_values.get_mapping_loop_lines.return_value = [
            {'index_filename': 72, 'line_source_code': 10, 'index_ir': 86,
             'line_ir_code': 240},
            {'index_filename': 72, 'line_source_code': 14, 'index_ir': 92,
             'line_ir_code': 261},
            {'index_filename': 72, 'line_source_code': 33, 'index_ir': 105,
             'line_ir_code': 316}]

        loop_bounding(intermediate_values)
        calls = call(240, 10), call(261, 50), call(316, 20)
        intermediate_values.set_mapping_loop_bound.assert_has_calls(
            calls, any_order=False)

    # VC-055
    @patch('src.utils.intermediate_values.IntermediateValues')
    def test_02_without_loop(self, intermediate_values):
        intermediate_values = Mock()
        intermediate_values.get_all_user_project_files.return_value = [
            {'index_filename': 37, 'filename': 'semloop.c',
             'directory': INPUT_DIRECTORY,
             'checksum': 'a4b8f96637d0704c82f39ecb6bde2ab4'}]
        intermediate_values.get_mapping_loop_lines.return_value = []

        loop_bounding(intermediate_values)
        intermediate_values.set_mapping_loop_bound.assert_not_called()

    # VC-056
    @patch('src.utils.intermediate_values.IntermediateValues')
    def test_03_without_file(self, intermediate_values):
        intermediate_values = Mock()
        intermediate_values.get_all_user_project_files.return_value = []
        intermediate_values.get_mapping_loop_lines.return_value = []

        loop_bounding(intermediate_values)
        intermediate_values.set_mapping_loop_bound.assert_not_called()


class Test_find_function_name(unittest.TestCase):

    # VC-059
    def test_01_define_function(self):
        self.assertEqual(find_function_name(
            "define dso_local i32 @calculadora() #0 !dbg !45 {"), "calculadora")

    # VC-060
    def test_02_declare_function(self):
        self.assertEqual(find_function_name(
            "declare dso_local void @srand(i32 noundef) #1"), "srand")

    # VC-061
    def test_03_define_function_with_parameters(self):
        self.assertEqual(find_function_name(
            "define linkonce_odr dso_local i32 @_vsprintf_l(ptr noundef %0, ptr noundef %1, ptr noundef %2, ptr noundef %3) #0 comdat !dbg !125 {"), "_vsprintf_l")

    # VC-062
    def test_04_declare_funtion_with_dot(self):
        self.assertEqual(find_function_name(
            "declare void @llvm.va_start(ptr) #2"), "llvm.va_start")

    # VC-063
    def test_05_less_information(self):
        self.assertEqual(find_function_name("@fatorial()"), "fatorial")


class Test_functions_mapping(unittest.TestCase):

    # VC-057
    def test_01_first_program(self):
        intermediate_values = Mock()

        file = open(INPUT_DIRECTORY + "first.ll", 'r')
        intermediate_values.get_ir.return_value = file.readlines()
        file.close()

        functions_mapping(intermediate_values)

        calls_important = call(
            'sprintf', 46), call(
            'vsprintf', 65), call(
            '_snprintf', 80), call(
            '_vsnprintf', 102), call(
            'calculadora', 120), call(
            'printf', 133), call(
            'scanf', 150), call(
            'fatorial', 167), call(
            'soma_prefixa', 194), call(
            'main', 272), call(
            'time', 346), call(
            '_vsprintf_l', 360), call(
            '_vsnprintf_l', 381), call(
            '__local_stdio_printf_options', 422), call(
            '_vfprintf_l', 427), call(
            '_vfscanf_l', 451), call(
            '__local_stdio_scanf_options', 473)
        intermediate_values.set_mapping_important_functions_lines.assert_has_calls(
            calls_important, any_order=False)

        calls_void = call(
            'srand', 343), call(
            'rand', 354), call(
            'llvm.va_start', 357), call(
            'llvm.va_end', 378), call(
            '__stdio_common_vsprintf', 419), call(
            '__acrt_iob_func', 446), call(
            '__stdio_common_vfprintf', 448), call(
            '__stdio_common_vfscanf', 470), call(
            '_time64', 477)
        intermediate_values.set_mapping_void_functions_lines.assert_has_calls(
            calls_void,
            any_order=False)

    # VC-058
    def test_02_without_loop(self):
        intermediate_values = Mock()

        file = open(INPUT_DIRECTORY + "semloop.ll", 'r')
        intermediate_values.get_ir.return_value = file.readlines()
        file.close()

        functions_mapping(intermediate_values)

        calls_important = call(
            'sprintf', 23), call(
            'vsprintf', 42), call(
            '_snprintf', 57), call(
            '_vsnprintf', 79), call(
            'main', 97), call(
            '_vsprintf_l', 116), call(
            '_vsnprintf_l', 137), call(
            '__local_stdio_printf_options', 178)
        intermediate_values.set_mapping_important_functions_lines.assert_has_calls(
            calls_important, any_order=False)

        calls_void = call(
            'llvm.va_start', 113), call(
            'llvm.va_end', 134), call(
            '__stdio_common_vsprintf', 175)
        intermediate_values.set_mapping_void_functions_lines.assert_has_calls(
            calls_void,
            any_order=False)


if __name__ == '__main__':
    unittest.main()
