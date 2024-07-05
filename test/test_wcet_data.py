from setup_test import *

from src.utils.wcet_data import WcetData


class Test_WcetData(unittest.TestCase):

    # VC-229
    @patch('src.utils.wcet_data.datetime')
    def test_01_constructor(self, mocked):
        mocked.now = Mock(return_value=date(2023, 9, 23))
        wcet = WcetData("Technique")

        self.assertEqual(wcet.get_technique_name(), "Technique")
        self.assertEqual(wcet.get_swcet(), 0.0)
        self.assertEqual(wcet.get_pwcet(), [])
        self.assertEqual(wcet.get_hwm(), 0)
        self.assertEqual(wcet.get_iid_flag(), "")
        self.assertEqual(wcet.get_histogram(), None)
        self.assertEqual(wcet.get_worst_input(), None)
        self.assertEqual(wcet.get_analysis_start_time(), "2023/09/23 - 00:00:00.000000")

    # VC-230
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.utils.wcet_data.datetime')
    def test_02_str_function(self, mocked, mock_stdout):
        mocked.now = Mock(return_value=date(2020, 11, 7))
        wcet = WcetData("Analysis")

        print(wcet)
        self.assertEqual(mock_stdout.getvalue(),
                         "*** WCET result ***" +
                         "\nTechnique: Analysis" +
                         "\nAnalysis start time: 2020/11/07 - 00:00:00.000000" +
                         "\nStatic WCET: 0.0" +
                         "\nProbabilistic WCET: []" +
                         "\nHigh-Water Mark: 0" +
                         "\nIID flag: " +
                         "\Worst Input: None\n")

    # VC-231
    @patch('src.utils.wcet_data.datetime')
    def test_03_setters(self, mocked):
        mocked.now = Mock(return_value=date(1999, 1, 2))
        wcet = WcetData("WCET")

        wcet.set_swcet(50000.2)
        wcet.set_pwcet([(1E-9, 20000.0)])
        wcet.set_hwm(5700)
        wcet.set_iid_flag("iid")
        wcet.set_histogram([5, 5, 5])
        wcet.set_worst_input([1, 2, 3])

        self.assertEqual(wcet.get_technique_name(), "WCET")
        self.assertEqual(wcet.get_swcet(), 50000.2)
        self.assertEqual(wcet.get_pwcet(), [(1E-9, 20000.0)])
        self.assertEqual(wcet.get_hwm(), 5700)
        self.assertEqual(wcet.get_iid_flag(), "iid")
        self.assertEqual(wcet.get_histogram(), [5, 5, 5])
        self.assertEqual(wcet.get_worst_input(), [1, 2, 3])
        self.assertEqual(wcet.get_analysis_start_time(), "1999/01/02 - 00:00:00.000000")


if __name__ == '__main__':
    unittest.main()
