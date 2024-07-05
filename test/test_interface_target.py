from setup_test import *

from src.interface_target.interface_target import *


class TestInterfaceTarget(unittest.TestCase):
    def setUp(self):
        self.project = Mock()
        self.inter_values = Mock()
        self.project.output_directory = os.getcwd()+"/test/input/"
        self.project.input_directory = os.getcwd()+"/test/input/"
        self.project.main_file_name = "test"

    # LLR-100
    # VC-384
    def test_01_init_communicator(self):
        self.project.architecture = "avr"
        interface = InterfaceTarget(
            self.project, self.inter_values)

        self.assertIsInstance(interface.communicator, ITarget)

    # LLR-100
    # VC-385
    def test_02_init_communicator(self):
        self.project.architecture = "riscv32"
        interface = InterfaceTarget(
            self.project, self.inter_values)

        self.assertIsInstance(interface.communicator, ITarget)

    # LLR-100
    # VC-386
    @patch('subprocess.Popen')
    def test_03_init_communicator(self, mock_terminal):
        self.project.architecture = "other"
        with self.assertRaises(SystemExit):
            interface = InterfaceTarget(
                self.project, self.inter_values)
            mock_terminal.assert_called_with(
                "\n\33[41mError! Target architecture not supported!\33[0m",
                shell=True)

    # LLR-101
    # VC-387
    def test_04_init_communicator(self):
        self.project.architecture = "avr"
        self.project.board = True
        interface = InterfaceTarget(
            self.project, self.inter_values)
        self.assertIsInstance(interface.communicator, AvrBoard)

    # LLR-101
    # VC-388
    def test_05_init_communicator(self):
        self.project.architecture = "avr"
        self.project.board = False
        interface = InterfaceTarget(
            self.project, self.inter_values)
        self.assertIsInstance(interface.communicator, AvrSimulator)

    # LLR-102
    # VC-389
    def test_06_init_communicator(self):
        self.project.architecture = "riscv32"
        self.project.board = True
        interface = InterfaceTarget(
            self.project, self.inter_values)
        self.assertIsInstance(interface.communicator, RiscvBoard)

    # LLR-102
    # VC-390
    @patch('subprocess.Popen')
    def test_07_init_communicator(self, mock_terminal):
        self.project.architecture = "riscv32"
        self.project.board = False
        with self.assertRaises(SystemExit):
            interface = InterfaceTarget(
                self.project, self.inter_values)
            mock_terminal.assert_called_with(
                "\n\33[41mError! Target architecture does not support a simulator!\33[0m",
                shell=True)

    # LLR-104
    # VC-391
    def test_08_run(self):
        self.project.architecture = "avr"
        self.project.board = False
        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.communicator = Mock()
        result = interface.run([[1, 2, 3, 4, 5], 5])

        interface.communicator.run.assert_called_once_with([1, 2, 3, 4, 5, 5])

    # LLR-104
    # VC-392
    def test_09_run(self):
        self.project.architecture = "avr"
        self.project.board = False
        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.communicator = Mock()
        interface.communicator.run.return_value = [
            "#;main;block0;123", "#;main;block0;54", "#;function;block1;32",
            "#;function;block2;543", "#;function;block3;98"]
        result = interface.run([1, 2, 3, 4, 5])

        self.assertEqual(
            result,
            ["#;main;block0;123", "#;main;block0;54", "#;function;block1;32",
             "#;function;block2;543", "#;function;block3;98"])

    # LLR-105
    # VC-393
    def test_09_flash(self):
        self.project.architecture = "avr"
        self.project.board = False
        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.communicator = Mock()
        interface.flash()

        interface.communicator.flash.assert_called_once()

    # LLR-106
    # VC-394
    def test_10_backend(self):
        self.project.architecture = "avr"
        self.project.board = False
        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.communicator = Mock()
        interface.backend_compile()

        interface.communicator.compile.assert_called_once()

    # LLR-107
    # VC-395
    def test_11_flatten(self):
        self.project.architecture = "avr"
        self.project.board = False
        interface = InterfaceTarget(
            self.project, self.inter_values)

        result = interface.flatten([[1, 2, 3, 4, 5], 5])
        self.assertEqual(result, [1, 2, 3, 4, 5, 5])

    # LLR-107
    # VC-396
    def test_12_flatten(self):
        self.project.architecture = "avr"
        self.project.board = False
        interface = InterfaceTarget(
            self.project, self.inter_values)

        result = interface.flatten([1, 2, 3, 4, 5])
        self.assertEqual(result, [1, 2, 3, 4, 5])

    # LLR-108
    # VC-397
    def test_14_compile_ir(self):
        self.project.architecture = "avr"
        self.project.board = False

        self.project.vendor = 'atmel'
        self.project.operational_system = 'none'
        self.project.microcontroller_unit = 'atmega328'
        self.project.llvm_path = '/usr/lib/llvm-16/bin/'

        self.project.get_env_name.return_value = "board"

        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.compile_to_ir()

        output_file = self.project.output_directory+self.project.main_file_name+".ll"
        file = open(output_file, 'r')
        hash = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()
        self.assertEqual(
            hash,
            "684f953fba8d0e0436b79a13e4ef6e7036eaf1acc61cfca1c9e173696f1bddd3")

    # LLR-109
    # VC-398
    def test_15_instrument_ipet_hybrid(self):
        self.project.architecture = "avr"
        self.project.board = False

        self.project.vendor = 'atmel'
        self.project.operational_system = 'none'
        self.project.microcontroller_unit = 'atmega328'
        self.project.llvm_path = '/usr/lib/llvm-16/bin/'

        self.project.get_env_name.return_value = "board"

        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.compile_to_ir()
        interface.instrument_ipet_hybrid()

        output_file = self.project.output_directory+self.project.main_file_name+".ll"
        file = open(output_file, 'r')
        hash = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()
        self.assertEqual(
            hash,
            "3ccab4f6e425ab2e6e5c14d8b8dc67845cadebc892381ee2e30c94eef490423c")

    # LLR-118
    # VC-399
    def test_16_instrument_wpevt(self):
        self.project.architecture = "avr"
        self.project.board = False

        self.project.vendor = 'atmel'
        self.project.operational_system = 'none'
        self.project.microcontroller_unit = 'atmega328'
        self.project.llvm_path = '/usr/lib/llvm-16/bin/'

        self.project.get_env_name.return_value = "board"

        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.set_ga_filenames()
        interface.compile_to_ir()
        interface.instrument_wpevt()

        output_file = self.project.output_directory + \
            self.project.main_file_name+"_inst.ll"
        file = open(output_file, 'r')
        hash = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()
        self.assertEqual(
            hash,
            "afb59408183fd1e3edf876cb8e3e8fdced1f6dd1872a02d24d77bc2c4cc72ec5")

    # LLR-121
    # VC-400
    def test_16_setup_ipet_hybrid(self):
        self.project.architecture = "avr"
        self.project.board = False

        self.project.vendor = 'atmel'
        self.project.operational_system = 'none'
        self.project.microcontroller_unit = 'atmega328'
        self.project.llvm_path = '/usr/lib/llvm-16/bin/'

        self.project.get_env_name.return_value = "board"

        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.compile_to_ir()
        interface.setup_ipet_hybrid()

        output_file = self.project.output_directory+self.project.main_file_name+".ll"
        file = open(output_file, 'r')
        hash = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()
        self.assertEqual(
            hash,
            "357fd29227b3cc473f5ea0ebb122497c6b523184bbbeb148e78bd8483301e574")

    # LLR-124
    # VC-401
    def test_17_link(self):
        self.project.architecture = "avr"
        self.project.board = False

        self.project.vendor = 'atmel'
        self.project.operational_system = 'none'
        self.project.microcontroller_unit = 'atmega328'
        self.project.llvm_path = '/usr/lib/llvm-16/bin/'

        self.project.get_env_name.return_value = "board"

        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.compile_to_ir()
        interface.link()

        output_file = self.project.output_directory+self.project.main_file_name+".ll"
        file = open(output_file, 'r')
        hash = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()
        self.assertEqual(
            hash,
            "bdfe45f590f06929eb51ebaca1c97d0df81831b3e41a6c67a915f4e3d43c08b4")

    # LLR-125
    # VC-402
    def test_18_set_ir(self):
        self.project.architecture = "avr"
        self.project.board = False

        self.project.vendor = 'atmel'
        self.project.operational_system = 'none'
        self.project.microcontroller_unit = 'atmega328'
        self.project.llvm_path = '/usr/lib/llvm-16/bin/'

        self.project.get_env_name.return_value = "board"

        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.compile_to_ir()
        interface.set_ir()

        output_file = self.project.output_directory+self.project.main_file_name+".ll"
        file = open(output_file, 'r')
        content = file.readlines()
        file.close()

        interface.inter_values.set_ir.assert_called_once_with(content)

    # LLR-126
    # VC-403
    def test_19_compile_to_obj(self):
        self.project.architecture = "avr"
        self.project.board = False

        self.project.vendor = 'atmel'
        self.project.operational_system = 'none'
        self.project.microcontroller_unit = 'atmega328'
        self.project.llvm_path = '/usr/lib/llvm-16/bin/'

        self.project.get_env_name.return_value = "board"

        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.compile_to_ir()
        interface.compile_to_obj()

        output_file = self.project.output_directory+self.project.main_file_name+".o"
        file = open(output_file, 'rb')
        hash = hashlib.sha256(file.read()).hexdigest()
        file.close()
        self.assertEqual(
            hash,
            "3f775cd98a94b93ee81a5685867e6943409a108ff017f13475fab6292d7485fb")

    # LLR-127
    # VC-404
    def test_20_compile_to_asm(self):
        self.project.architecture = "avr"
        self.project.board = False

        self.project.vendor = 'atmel'
        self.project.operational_system = 'none'
        self.project.microcontroller_unit = 'atmega328'
        self.project.llvm_path = '/usr/lib/llvm-16/bin/'

        self.project.get_env_name.return_value = "board"

        interface = InterfaceTarget(
            self.project, self.inter_values)

        interface.compile_to_ir()
        interface.compile_to_asm()

        output_file = self.project.output_directory+self.project.main_file_name+".asm"
        file = open(output_file, 'rb')
        hash = hashlib.sha256(file.read()).hexdigest()
        file.close()
        self.assertEqual(
            hash,
            "980bda474cdce07604b389a5a53f376ae5e957c75f93d2317f1cd83184048a36")


if __name__ == '__main__':
    unittest.main()
