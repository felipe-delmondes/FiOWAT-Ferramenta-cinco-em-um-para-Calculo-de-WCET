from setup_test import *

from src.pipeline.director import Director


class Test_Director(unittest.TestCase):

    #VC-340
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.pipeline.director.ConfigParser')
    def test_01_constructor(self, mock_config_parser, mock_stdout):
        mock_config_parser = Mock()
        mock_config_parser.run_config_parser.return_value = None

        wcet_run = Director(CURRENT_DIRECTORY)
        self.assertEqual(mock_stdout.getvalue(),
            "Reading the config.yaml...\n\33[42mDone\33[0m\n")

    #VC-341
    @patch('src.pipeline.director.ConfigParser')
    def test_02_run_pipeline_exit(self, mock_config_parser):
        mock_config_parser = Mock()
        mock_config_parser.run_config_parser.return_value = None

        wcet_run = Director(CURRENT_DIRECTORY)

        with self.assertRaises(SystemExit):
            wcet_run.run_pipeline()



if __name__ == '__main__':
    unittest.main()