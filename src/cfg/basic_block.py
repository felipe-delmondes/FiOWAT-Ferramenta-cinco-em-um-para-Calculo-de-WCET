class BasicBlock:
    """
    Basic block of Intermediate Representation (IR) Control Flow Graph (CFG).


    Parameters
    ----------
        None


    Attributes
    ----------
    id : int
        Basic block ID, using IR line as indexer

    name : str, default = ""
        Name used by instrumentation pass of opt developed by us

    weight : int
        Number of cycles or time for CPU execute this basic block

    number_executions : int, default = 0
        Maximum number of times that block is executed in program.

        Some blocks has 0 value by default, this means the exactly number of executions is undefined.

    instructions : list, default = []
        List of all instructions in order. These instructions just have the instructions. Example: ret, add, load

    next_blocks : list, default = []
        List of all connections to next basic blocks. If list is empty, so it's a exit block.

        The connections is made using index of same list. Example [1, 5, 12]
    """
    # By default, a basic block has these values. Usually it's use by void functions

    def __init__(self) -> None:
        self.id = -1
        self.name = ""
        self.weight = 0
        self.number_executions = 0
        self.instructions = []
        self.next_blocks = []

    # What return if class instance is printed
    def __str__(self) -> str:
        return "\n\nID: " + str(
            self.id) + "\nName: " + self.name + "\nWeight: " + str(
            self.weight) + "\nMax execution times: " + str(
            self.number_executions) + "\nInstructions: " + str(
            self.instructions) + "\nNext basic blocks ID: " + str(
            self.next_blocks)

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_weight(self) -> int:
        return self.weight

    def get_number_executions(self) -> int:
        return self.number_executions

    def get_instructions(self) -> list:
        return self.instructions

    def get_next_blocks(self) -> list:
        return self.next_blocks

    def set_id(self, id: int) -> None:
        self.id = id

    def set_name(self, name: str) -> None:
        self.name = name

    def set_weight(self, weight: int) -> None:
        self.weight = weight

    def set_number_executions(self, number_executions: int) -> None:
        self.number_executions = number_executions

    def set_instructions(self, line: str) -> None:
        self.instructions.append(line)

    def set_next_blocks(self, next_blocks: list) -> None:
        self.next_blocks = next_blocks

    def set_basic_block(self, id: int, name: str, weight: int,
                        number_executions: int, instructions: list,
                        next_blocks: list) -> None:
        self.id = id
        self.name = name
        self.weight = weight
        self.number_executions = number_executions
        self.instructions = instructions
        self.next_blocks = next_blocks