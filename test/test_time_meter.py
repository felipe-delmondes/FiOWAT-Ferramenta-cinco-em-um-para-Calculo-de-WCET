from setup_test import *

from src.cfg.timeMeter import *


class TestTimeMeter(unittest.TestCase):
    def setUp(self):
        self.project = Mock()
        self.inter_values = Mock()
        self.interface_target = Mock()
        self.project.output_directory = os.getcwd()+"/test/input/"
        self.project.main_file_name = "test"

    # LLR-86
    # VC-369
    def test_01_run_test_case_interface_target(self):
        timer = TimeMeter(
            self.project, self.inter_values, self.interface_target)

        test_case1 = [1, 2, 3, 4, 5, 6]
        test_case2 = [6, 5, 4, 3, 2, 1]
        self.inter_values.test_cases = [test_case1, test_case2]
        self.interface_target.run.return_value = [
            "#;main;block0;123", "#;main;block0;54", "#;function;block1;32",
            "#;function;block2;543", "#;function;block3;98"]
        calls_run = [call(test_case1), call(test_case2)]
        calls_extract = [call(), call()]
        calls_integrate = [call(), call()]

        timer.extract_times = Mock()
        timer.integrate_times = Mock()

        timer.run_test_cases()

        self.interface_target.run.assert_has_calls(calls_run, any_order=False)
        timer.extract_times.assert_has_calls(calls_extract)
        timer.integrate_times.assert_has_calls(calls_integrate)

    # LLR-87
    #VC-370
    def test_02_run_test_case_output_attr(self):
        timer = TimeMeter(
            self.project, self.inter_values, self.interface_target)
        test_case1 = [1, 2, 3, 4, 5, 6]
        test_case2 = [6, 5, 4, 3, 2, 1]
        self.inter_values.test_cases = [test_case1, test_case2]
        self.interface_target.run.return_value = [
            "#;main;block0;123", "#;main;block0;54", "#;function;block1;32",
            "#;function;block2;543", "#;function;block3;98"]

        timer.run_test_cases()

        self.assertEqual(timer.output, [
            "#;main;block0;123", "#;main;block0;54", "#;function;block1;32",
            "#;function;block2;543", "#;function;block3;98"])

    # LLR-88
    #VC-371
    def test_03_run_test_case_dict(self):
        timer = TimeMeter(
            self.project, self.inter_values, self.interface_target)
        test_case1 = [1, 2, 3, 4, 5, 6]
        test_case2 = [6, 5, 4, 3, 2, 1]
        self.inter_values.test_cases = [test_case1, test_case2]
        self.interface_target.run.return_value = [
            "#;main;block0;123", "#;main;block0;54", "#;function;block1;32",
            "#;function;block2;543", "#;function;block3;98"]

        timer.run_test_cases()

        self.assertEqual(timer.final_times, {'instrumentation': [54], 'function': {
            '_total': 1022, 'block1': 467, 'block2': 44, 'block3': 0}})

    # LLR-89
    # VC-372
    def test_04_extract_times(self):
        timer = TimeMeter(
            self.project, self.inter_values, self.interface_target)

        timer.output = ["#;main;block0;123", "#;main;block0;54",
                        "#;function;block1;32", "#;function;block2;543",
                        "#;function;block3;98"]

        timer.extract_times()

        self.assertEqual(timer.partial_times, {'instrumentation': [54], 'function': {
            '_total': 511, 'block1': 467, 'block2': 44, 'block3': 0}})

    # LLR-90
    # VC-373
    def test_04_integrate_times(self):
        timer = TimeMeter(
            self.project, self.inter_values, self.interface_target)

        timer.final_times = {'instrumentation': [12], 'function': {
            '_total': 1022, 'block1': 22, 'block2': 44, 'block3': 0}}
        timer.partial_times = {'instrumentation': [54], 'function': {
            '_total': 511, 'block1': 467, 'block2': 44, 'block3': 0}}

        timer.integrate_times()

        self.assertEqual(timer.final_times, {'instrumentation': [12], 'function': {
            '_total': 1022, 'block1': 467, 'block2': 44, 'block3': 0}})

    # LLR-91
    #VC-374
    def test_04_save_times(self):
        timer = TimeMeter(
            self.project, self.inter_values, self.interface_target)

        timer.final_times = {'instrumentation': [12], 'function': {
            '_total': 1022, 'block1': 22, 'block2': 44, 'block3': 0}}

        timer.save_times()

        output_file = self.project.output_directory + \
            self.project.main_file_name+"_block_times.json"
        file = open(output_file, 'r')
        hash_json = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()

        self.assertEqual(
            hash_json,
            "1fabd5d07dd45000ac0a7ff8ef5f0d3fa000a97f80e711e4ca6e63989552bf22")


if __name__ == '__main__':
    unittest.main()
