import subprocess


class Context():
    """
    Save the current context of communication, to trace the call graph of function and know how cycles spend each basic block


    Parameters
    ----------
    last_mark : str
        Last mark outputted. Example: #;_vfscanf_l;block0

    block_time : int
        Number of cycles in that time


    Attributes
    ----------
    last_mark : str
        Last mark outputted. Example: #;_vfscanf_l;block0

    block_time : int
        Number of cycles in that time
    """
    def __init__(self, last_mark : str, block_time : int) -> None:
        self.last_mark = last_mark
        self.block_time = block_time

    def __str__(self) -> str:
        return f"{self.last_mark.func} {self.last_mark.block} {self.last_mark.time} {self.total_time} {self.partial_block_time}"

    def update_last_mark(self, mark : str) -> None:
        """
        Update the last mark outputted

        
        Parameters
        ----------
        last_mark : str
            Last mark outputted. Example: #;_vfscanf_l;block0

            
        Returns
        -------
            None
        """
        self.last_mark = mark

    def inc_block_time(self, time : int) -> None:
        """
        Update total number of cycles spend at time by the program

        
        Parameters
        ----------
        time : int
            Increment the number of cycles spend at time by the program

            
        Returns
        -------
            None
        """
        self.block_time += time


class Stack():
    """
    Create match between basic blocks, to avoid count call functions


    Parameters
    ----------
        None


    Attributes
    ----------
    stack_frames : list
        Stack of basic blocks called
    """
    def __init__(self) -> None:
        self.stack_frames = []

    def __str__(self) -> str:
        stack_string = "Stack:"
        for item in reversed(self.stack_frames):
            stack_string += f"\n{item}"
        return "\n------\n" + stack_string + "\n------"

    def pop_if_matches(self, name : str) -> list:
        """
        Remove the basic block of stack if match with other basic block

        
        Parameters
        ----------
        name : str
            Basic block name

            
        Returns
        -------
        stack_frames : list
            Stack updated
        """
        if self.stack_frames and self.stack_frames[-1].last_mark.func == name:
            return self.stack_frames.pop()

    def push(self, ctx : str) -> None:
        """
        Push one basic block on stack

        
        Parameters
        ----------
        ctx : str
            Basic block name

            
        Returns
        -------
            None
        """
        self.stack_frames.append(ctx)


class Mark():
    """
    Process the output of board or simulator. Example of output: #;_vfscanf_l;block0


    Parameters
    ----------
    mark : str
        Output of board/simulator. Example of output: #;_vfscanf_l;block0


    Attributes
    ----------
    func : str
        Function name. Example: _vfscanf_l

    block : str
        Basic block. Example: block0

    time : int
        Number of cycles of respective basic block
    """
    def __init__(self, mark : str) -> None:
        fields = mark.split(";")
        self.func = fields[1]
        self.block = fields[2]
        self.time = int(fields[3])

    def __str__(self) -> str:
        return f"{self.func};{self.block};{self.time}"




def insert_in_dict(times : dict, func_name : str, block : str, time : int) -> None:
    """
    Stores the execution time of a block in the dictionary.

    
    Parameters
    ----------
    times : dict
        The dictionary to store block times.

    func_name : str
        Name of the function which the block belong.

    block : str
        Name of the block.

    time : int
        Execution time to be inserted.

    
    Returns
    -------
        None
    """
    if func_name not in times:
        times[func_name] = {}
    if block not in times[func_name]:
        times[func_name][block] = time
    else:
        times[func_name][block] = max(times[func_name][block], time)


def inc_in_dict(times : dict, func_name : str, block : str, time : int) -> None:
    """
    Increment the execution time of a block in the dictionary.

    
    Parameters
    ----------
    times : dict
        The dictionary to store block times.

    func_name : str
        Name of the function which the block belong.

    block : str
        Name of the block.

    time : int
        Execution time to be incremented in block time.

        
    Returns
    -------
        None
    """
    if func_name not in times:
        times[func_name] = {}
    if block not in times[func_name]:
        times[func_name][block] = time
    else:
        times[func_name][block] += time


def system_call(cmd : str) -> None:
    '''
    Execute command like a system call


    Parameters
    ----------
    cmd : str
        Command to run in shell


    Returns
    -------
        None
    '''
    try:
        processo = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        stdout, stderr = processo.communicate()

        if processo.returncode != 0:
            print(
                f"\n\33[41mError while executing the command {cmd}: {stderr.decode()}\33[0m")
            exit(-1)

    except Exception as e:
        print(f"\33[41mError trying to execute the command {cmd}: {e}\33[0m")
        exit(-1)
