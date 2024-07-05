from setup_test import *
from src.main import main
from freezegun import freeze_time


# ----------------------------------#
#           OBSERVATION             #
# ----------------------------------#
# These tests will fail because it's necessary change config.yaml file to your enviroment
# Example: Operational system, LLVM path, input directory, output directory, and so on


class Test_static_ipet(unittest.TestCase):

    # VC-361
    @freeze_time("2012-01-14")
    def test_01_first_program(self):
        directory_base = os.path.join(CURRENT_DIRECTORY, "system_test")
        directory_config_yaml = os.path.join(directory_base, "config_01.yaml")
        directory_json = os.path.join(os.path.join(os.path.join(
            directory_base, "first"), "2012_01_14-00h_00m_00s_static_ipet"), "WCET Report first - 2012-01-14.json")

        main(["--config", directory_config_yaml])

        # Find the hash of created JSON file
        file = open(directory_json, 'r')
        hash_json = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()

        # Compare is value is correct
        self.assertEqual(
            hash_json,
            "2e25311b37687ca013eca3a8a33fbb32a27d18b6d611550203922fd30a8d080a")

    # VC-362
    @freeze_time("2015-02-02")
    def test_02_error_annotation(self):
        directory_base = os.path.join(CURRENT_DIRECTORY, "system_test")
        directory_config_yaml = os.path.join(directory_base, "config_02.yaml")

        with self.assertRaises(SystemExit):
            main(["--config", directory_config_yaml])


class Test_hybrid_ipet(unittest.TestCase):

    # VC-405
    @freeze_time("2015-03-05")
    def test_01_bsort_program(self):
        directory_base = os.path.join(CURRENT_DIRECTORY, "system_test")
        directory_config_yaml = os.path.join(directory_base, "config_03.yaml")
        directory_json = os.path.join(os.path.join(os.path.join(
            directory_base, "bsort10"), "2015_03_05-00h_00m_00s_hybrid_ipet"), "WCET Report bsort10 - 2015-03-05.json")

        main(["--config", directory_config_yaml])

        # Find the hash of created JSON file
        file = open(directory_json, 'r')
        hash_json = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()

        # Compare is value is correct
        self.assertEqual(
            hash_json,
            "53da9fe2f17264d0e7905e7282a49038fe62dadf1bea4c20bdfddeda91994317")


class Test_wpevt(unittest.TestCase):

    #VC-417
    @freeze_time("2015-03-05")
    def test_01_bsort_program(self):
        directory_base = os.path.join(CURRENT_DIRECTORY, "system_test")
        directory_config_yaml = os.path.join(directory_base, "config_04.yaml")
        directory_json = os.path.join(os.path.join(os.path.join(
            directory_base, "bsort20"), "2015_03_05-00h_00m_00s_wpevt"), "WCET Report bsort20 - 2015-03-05.json")

        main(["--config", directory_config_yaml])

        # Find the hash of created JSON file
        file = open(directory_json, 'r')
        hash_json = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()

        # Compare is value is correct
        self.assertEqual(
            hash_json,
            "53da9fe2f17264d0e7905e7282a49038fe62dadf1bea4c20bdfddeda91994317")
        

class Test_dynamic_ga(unittest.TestCase):

    #VC-418
    @freeze_time("2015-03-05")
    def test_01_bsort_program(self):
        directory_base = os.path.join(CURRENT_DIRECTORY, "system_test")
        directory_config_yaml = os.path.join(directory_base, "config_05.yaml")
        directory_json = os.path.join(os.path.join(os.path.join(
            directory_base, "bsort10"), "2015_03_05-00h_00m_00s_dynamic_ga"), "WCET Report bsort10 - 2015-03-05.json")
    

        main(["--config", directory_config_yaml])

        # Find the hash of created JSON file
        file = open(directory_json, 'r')
        hash_json = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()

        # Compare is value is correct
        self.assertEqual(
            hash_json,
            "53da9fe2f17264d0e7905e7282a49038fe62dadf1bea4c20bdfddeda91994317")

# class Test_evt(unittest.TestCase):

#     #VC-450 - System Test EVT 
#     @freeze_time("2015-03-05")
#     @patch('src.evt.evt_facade.IntermediateValues')
#     @patch('src.evt.evt_facade.InputManager')
#     @patch('src.evt.evt_facade.InterfaceTarget')
#     @patch('src.evt.evt_facade.evt_running')
#     def test_Tool_EVT(self,mock_evt_running, mock_interface_target, mock_manager, mock_inter_values):

#         directory_base = os.path.join(CURRENT_DIRECTORY, "system_test")
#         directory_config_yaml = os.path.join(directory_base, "config_06.yaml")
#         #directory_json = os.path.join(os.path.join(os.path.join(
#         #    directory_base, "bsort10"), "2015_03_05-00h_00m_00s_evt"), "WCET Report bsort10 - 2015-03-05.json")
        
#         mock_manager().generator = False

#         mock_evt_running.return_value = [10, 10, 110, 12 ,12,154,15,15,16,16]

#         main(["--config", directory_config_yaml])


if __name__ == '__main__':
    unittest.main()
