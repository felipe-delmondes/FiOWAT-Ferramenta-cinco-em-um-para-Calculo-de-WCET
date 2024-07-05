from setup_test import *

from src.cfg.basic_block import BasicBlock


class Test_BasicBlock(unittest.TestCase):

    # VC-064
    def test_01_constructor(self):
        basic_block = BasicBlock()
        self.assertEqual(basic_block.get_id(), -1)
        self.assertEqual(basic_block.get_name(), "")
        self.assertEqual(basic_block.get_weight(), 0)
        self.assertEqual(basic_block.get_number_executions(), 0)
        self.assertEqual(basic_block.get_instructions(), [])
        self.assertEqual(basic_block.get_next_blocks(), [])

    # VC-065
    def test_02_test_set_all(self):
        basic_block = BasicBlock()
        basic_block.set_basic_block(5, "block", 100, 67, ['add', 'ret'], [1, 3])
        self.assertEqual(basic_block.get_id(), 5)
        self.assertEqual(basic_block.get_name(), "block")
        self.assertEqual(basic_block.get_weight(), 100)
        self.assertEqual(basic_block.get_number_executions(), 67)
        self.assertEqual(basic_block.get_instructions(), ['add', 'ret'])
        self.assertEqual(basic_block.get_next_blocks(), [1, 3])

    # VC-064
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_03_print_basic_block(self, mock_stdout):
        basic_block = BasicBlock()
        basic_block.set_id(2)
        basic_block.set_name("main;0")
        basic_block.set_weight(55)
        basic_block.set_number_executions(20)
        basic_block.set_instructions('and')
        basic_block.set_instructions('br')
        basic_block.set_next_blocks([5, 6])
        print(basic_block)
        self.assertEqual(
            mock_stdout.getvalue(),
            "\n\nID: 2\nName: main;0\nWeight: 55\nMax execution times: 20\nInstructions: ['and', 'br']\nNext basic blocks ID: [5, 6]\n")


if __name__ == '__main__':
    unittest.main()