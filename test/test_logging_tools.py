from setup_test import *
from freezegun import freeze_time

from src.utils.logging_tools import log_function_name, config_logger


#Dummy functions to test decorator functions
@log_function_name
def void_function_1(number):
    return number + 1


class Test_log_function_name(unittest.TestCase):

    #VC-415
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_01(self, mock_stdout):
        self.assertEqual(void_function_1(5), 6)

        self.assertEqual(mock_stdout.getvalue(), "void_function_1\n")


class Test_config_logger(unittest.TestCase):

    #VC-416
    @freeze_time("2030-12-12")
    def test_01(self):
        config_logger(OUTPUT_DIRECTORY)

        log_directory = os.path.join(os.path.join(OUTPUT_DIRECTORY, 'logs'), 'project.log')

        file = open(log_directory, 'r')
        hash_json = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()

        self.assertEqual(hash_json,
                         "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")





if __name__ == '__main__':
    unittest.main()