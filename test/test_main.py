from setup_test import *

from src.main import main


class Test_main(unittest.TestCase):

    #VC-334
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_01_print_targets(self, mock_stdout):
        main(["--printtargets"])

        self.assertEqual(mock_stdout.getvalue(),
                         "Architectures supported:\n" +
                         "\33[1mStatic IPET:\33[0m\n" +
                         "  - AVR\n" +
                         "  - x86_64 (non accurate version)\n" +
                         "\n\33[1mHybrid IPET | WPEVT:\33[0m\n" +
                         "  - AVR\n" +
                         "\n\33[1mGA Dynamic | EVT:\33[0m\n" +
                         "  - Any board connected in serial port\n")

    #VC-335
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_02_version(self, mock_stdout):
        main(["--version"])

        self.assertEqual(mock_stdout.getvalue(),
                         "FioWAT version 1.0.0\n")
    
    #VC-336
    def test_03_two_flags(self):
        with self.assertRaises(SystemExit):
            main(["--printtargets", "--version"])

    #VC-337
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_04_no_flags(self, mock_stdout):
        main([])
        self.assertEqual(mock_stdout.getvalue(), "")

    #VC-338
    def test_05_help(self):
        with self.assertRaises(SystemExit):        
            main(["--help"])

    #VC-339
    @patch('src.main.Director')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_06_config(self, mock_stdout, mock_director):
        mock_director = Mock()
        mock_director.run_pipeline.return_value = None
   
        main(["--config", CURRENT_DIRECTORY])
            
        self.assertEqual(mock_stdout.getvalue(), "\33[44mStarting FioWAT analysis...\33[0m\n")



if __name__ == '__main__':
    unittest.main()
