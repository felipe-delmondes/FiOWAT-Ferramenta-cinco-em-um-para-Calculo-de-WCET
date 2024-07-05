from setup_test import *
from src.utils.user_project import UserProject
from src.utils.wcet_data import WcetData
from src.report_generator.report import *
from freezegun import freeze_time



# Initialize void Report
def init_void() -> Report:
    # Create Dummy Objects just to fill args
    wcet = Mock()
    project = Mock()
    return Report(project, wcet)


class Test_mm2p(unittest.TestCase):

    #VC-342
    def test_01_positive(self):
        report = init_void()
        self.assertAlmostEqual(report.mm2p(200), 566.9303837835)

    #VC-343
    def test_02_zero(self):
        report = init_void()
        self.assertEqual(report.mm2p(0), 0)

    #VC-344
    def test_03_negative(self):
        report = init_void()
        self.assertAlmostEqual(report.mm2p(-1), -2.8346519)




class Test_compliance_do178(unittest.TestCase):

    #VC-345
    def test_01_exceeded_deadline(self):
        report = init_void()
        report.current_y_position = 200
        report.pdf_file = Mock()

        report.compliance_do178(50, 0.900001)

        report.pdf_file.setFillColorRGB.assert_called_once_with(1, 0, 0)
        report.pdf_file.drawString.assert_called_once_with(141.73259594588083,
                                                           566.9303837835233,
                                                           "90.0% --- Does not comply with the DO-178 standard")

    #VC-346
    def test_02_almost_exceeded_deadline_1(self):
        report = init_void()
        report.current_y_position = 200
        report.pdf_file = Mock()

        report.compliance_do178(50, 0.9)

        report.pdf_file.setFillColorRGB.assert_called_once_with(1, 1, 0)
        report.pdf_file.drawString.assert_called_once_with(141.73259594588083,
                                                           566.9303837835233,
                                                           "90.0% --- The program must be analyzed with caution")

    #VC-347
    def test_03_almost_exceeded_deadline_2(self):
        report = init_void()
        report.current_y_position = 200
        report.pdf_file = Mock()

        report.compliance_do178(50, 0.800001)

        report.pdf_file.setFillColorRGB.assert_called_once_with(1, 1, 0)
        report.pdf_file.drawString.assert_called_once_with(141.73259594588083,
                                                           566.9303837835233,
                                                           "80.0% --- The program must be analyzed with caution")

    #VC-348
    def test_04_compliance_with_deadline(self):
        report = init_void()
        report.current_y_position = 200
        report.pdf_file = Mock()

        report.compliance_do178(50, 0.8)

        report.pdf_file.setFillColorRGB.assert_called_once_with(0, 1, 0)
        report.pdf_file.drawString.assert_called_once_with(141.73259594588083,
                                                           566.9303837835233,
                                                           "80.0% --- The program is safe")






class Test_setup_pdf(unittest.TestCase):

    #VC-349
    @patch('src.report_generator.report.canvas')
    @patch('src.report_generator.report.datetime')
    def test_01_normal_situation(self, mock_date, mock_canvas):
        mock_date = Mock()
        mock_date.date.today.return_value = date(2020, 10, 15)

        mock_canvas = Mock()
        mock_canvas.Canvas.return_value = None

        report = init_void()
        report.center_x = 100

        report.user_project = Mock()
        report.user_project.get_output_directory.return_value = "/directory/"
        report.user_project.get_main_file_name.return_value = "program"

        report.pdf_file = Mock()
        report.pdf_file.setCreator.return_value = None
        report.pdf_file.setFillColorRGB.return_value = None
        report.pdf_file.setFont.return_value = None
        report.pdf_file.drawCentredString.return_value = None

        report.setup_pdf()
        
        report.pdf_file.setCreator.assert_called_once_with("FioWAT")
        report.pdf_file.setFillColorRGB.assert_called_once_with(0, 0, 0)
        report.pdf_file.drawCentredString.assert_called_once_with(100, 771.0253219455917, "program.c program WCET report")
        self.assertEqual(report.pdf_file.setFont.call_count, 2)



class Test_show_loose(unittest.TestCase):

    #VC-350
    def test_01_value(self):
        report = init_void()
        report.current_y_position = 200
        report.distance_between_lines = 10
        report.paragraph = 50

        report.compliance_do178 = Mock()
        report.compliance_do178.return_value = None
        report.user_project = Mock()
        report.user_project.get_deadline.return_value = 100
        report.pdf_file = Mock()

        report.show_loose("text", 20)

        report.compliance_do178.assert_called_once_with(57, 0.2)
        report.pdf_file.drawString.assert_called_once_with(50,
                                                           566.9303837835233,
                                                           "Loose of text: ")
        report.pdf_file.setFillColorRGB.assert_called_once_with(0, 0, 0)
        self.assertEqual(report.current_y_position, 190)
        self.assertEqual(report.distance_between_lines, 10)

    #VC-351
    def test_02_tuple(self):
        report = init_void()
        report.current_y_position = -50
        report.distance_between_lines = 20
        report.paragraph = 30

        report.compliance_do178 = Mock()
        report.compliance_do178.return_value = None
        report.user_project = Mock()
        report.user_project.get_deadline.return_value = 100
        report.pdf_file = Mock()

        report.show_loose("text", (500, 1100))

        report.compliance_do178.assert_called_once_with(68, 11)
        report.pdf_file.drawString.assert_called_once_with(30,
                                                           -141.73259594588083,
                                                           "Loose of text: ")
        report.pdf_file.setFillColorRGB.assert_called_once_with(0, 0, 0)
        self.assertEqual(report.current_y_position, -70)
        self.assertEqual(report.distance_between_lines, 20)

    #VC-352
    def test_03_result_zero(self):
        report = init_void()
        report.current_y_position = 150
        report.distance_between_lines = 10
        report.paragraph = 40

        report.compliance_do178 = Mock()
        report.compliance_do178.return_value = None
        report.user_project = Mock()
        report.user_project.get_deadline.return_value = 80
        report.pdf_file = Mock()

        report.show_loose("text", 0)

        report.compliance_do178.assert_not_called()
        report.pdf_file.drawString.assert_called_once_with(40,
                                                           425.19778783764247,
                                                           'Loose of text: --- ')
        report.pdf_file.setFillColorRGB.assert_called_once_with(0, 0, 0)
        self.assertEqual(report.current_y_position, 140)
        self.assertEqual(report.distance_between_lines, 10)


class Test_create_line(unittest.TestCase):

    #VC-353
    def test_01_normal_execution(self):
        report = init_void()
        report.current_y_position = 200
        report.distance_between_lines = 10
        report.paragraph = 50

        report.pdf_file = Mock()

        report.create_line("text", 77)

        report.pdf_file.drawString.assert_called_once_with(
            50, 566.9303837835233, "text: 77")
        self.assertEqual(report.current_y_position, 190)
        self.assertEqual(report.distance_between_lines, 10)

    #VC-354
    def test_02_round(self):
        report = init_void()
        report.current_y_position = -100
        report.distance_between_lines = 20
        report.paragraph = 20

        report.pdf_file = Mock()

        report.create_line("message", 55.123456789)

        report.pdf_file.drawString.assert_called_once_with(
            20, -283.46519189176166, "message: 55.123")
        self.assertEqual(report.current_y_position, -120)
        self.assertEqual(report.distance_between_lines, 20)






class Test_error_print_report(unittest.TestCase):

    #VC-355
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_01_message_error(self, mock_stdout):
        report = init_void()
        report.wcet.get_swcet.return_value = 100
        report.wcet.get_pwcet.return_value = 200
        report.wcet.get_hwm.return_value = 50

        with self.assertRaises(SystemExit):
            report.error_print_report()

        self.assertEqual(mock_stdout.getvalue(),
                         "\n\33[41mError! The FioWAT don't has permission to create file.\33[0m\n" + 
                         "Please, if you have the PDF file opened, close it.\n" +
                         "Another reason is if the image file was not created.\n" +
                         "The WCET calculated was:\n" + 
                         "iWCET:  100\n" + 
                         "pWCET:  200\n" +
                         "High Water-Mark:  50\n")
    


def raise_permisson_error():
    raise PermissionError


class Test_save_pdf_file(unittest.TestCase):

    #VC-356
    def test_01_exit(self):
        report = init_void()
        report.pdf_file = Mock()
        report.pdf_file.save.side_effect = raise_permisson_error

        with self.assertRaises(SystemExit):
            report.save_pdf_file()

    #VC-357
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_02_correct(self, mock_stdout):
        report = init_void()
        report.pdf_file = Mock()
        report.pdf_file.save.return_value = None

        report.save_pdf_file()
        self.assertEqual(mock_stdout.getvalue(), "\33[42mDone\33[0m\n")





class Test_create_pdf_report(unittest.TestCase):

    #VC-358
    @freeze_time("2016-07-03")
    def test_01_create_pdf(self):
        project = UserProject(sys._getframe(0).f_code.co_name,
                            "",
                            OUTPUT_DIRECTORY,
                            "x86_64",
                            "pc",
                            "windows",
                            "unknown",
                            "main",
                            deadline=500000)
        wcet = WcetData("Static IPET")

        histogram_data = pd.read_csv(os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv"),
            header=0, usecols=[0],
            names=["valuesx"])
        histogram_data.valuesx = histogram_data.valuesx*1000000
        wcet.set_histogram(histogram_data)

        wcet.set_swcet(400000)
        wcet.set_pwcet(
            [(1E-9, 10000),
            (1E-10, 250000),
            (1E-11, 450000),
            (1E-27, 570000),
            (1E-33, 660000)])
        wcet.set_hwm(histogram_data.valuesx.max())
        wcet.set_iid_flag("Failed - Review data set. (LJung-box not passed)")

        report = Report(project, wcet)
        report.create_pdf_report()

        
        file = open(OUTPUT_DIRECTORY + "WCET Report " + \
                    sys._getframe(0).f_code.co_name + \
                    " - 2016-07-03.pdf", 'r')
        hash_json = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()

        # Compare is value is correct
        self.assertEqual(hash_json,
                         "cea9b1636e6b880b3fd7c70012f90f894f106870f6dd98ef2c62109b78d1ee00")

    #VC-359
    @freeze_time("2000-04-12")
    def test_02_minimum_information(self):
        project = UserProject(sys._getframe(0).f_code.co_name,
                            "",
                            OUTPUT_DIRECTORY,
                            "x86_64",
                            "pc",
                            "windows",
                            "unknown",
                            "main",
                            deadline=0)
        wcet = WcetData("Static IPET")

        histogram_data = None
        wcet.set_histogram(histogram_data)

        wcet.set_swcet(0)
        wcet.set_pwcet([])
        wcet.set_hwm(0)
        wcet.set_iid_flag("")

        report = Report(project, wcet)
        report.create_pdf_report()

        
        file = open(OUTPUT_DIRECTORY + "WCET Report " + \
                    sys._getframe(0).f_code.co_name + \
                    " - 2000-04-12.pdf", 'r')
        hash_json = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()

        # Compare is value is correct
        self.assertEqual(hash_json,
                         "ea766bee2ac5df832b6984b6220227e34afeae14b4dfce245a38a7c174451f25")






class Test_create_json_report(unittest.TestCase):

    #VC-360
    @freeze_time("2023-09-23")
    def test_01_normal_input(self):
        # Create intermediate objects (One mock and one real object)
        wcet = Mock()
        # Using current method to main file; Current directory to obtain and produces intermediate files
        project = UserProject(
            sys._getframe(0).f_code.co_name, CURRENT_DIRECTORY,
            OUTPUT_DIRECTORY, "x86_64", "pc", "windows", "unknown",
            deadline=500)
        report = Report(project, wcet)

        # Simulating methods of WCET (Always use this template: mock_name.method_name.return_value)
        # Simulate attributes is: mock_name.attribute_name
        wcet.get_swcet.return_value = 700.0
        wcet.get_pwcet.return_value = 550.3
        wcet.get_hwm.return_value = 400.0
        wcet.get_technique_name.return_value = "Static IPET"
        wcet.get_analysis_start_time.return_value = "2019/04/01 - 20:10:00"
        wcet.get_iid_flag.return_value = "Ok - Passed"
        wcet.get_worst_input.return_value = None

        # Method to test
        report.create_json_report()

        # Find the hash of created JSON file
        file = open(OUTPUT_DIRECTORY + "WCET Report " + \
                    sys._getframe(0).f_code.co_name + \
                    " - 2023-09-23.json", 'r')
        hash_json = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()

        # Compare is value is correct
        self.assertEqual(hash_json,
                         "7884b531c8f8153de509542cf305873ebb64cbed43aae5a639f169e95e053dcb")


if __name__ == '__main__':
    unittest.main()