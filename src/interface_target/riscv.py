from interface_target.i_target import ITarget
from cfg.timeMeter_aux import system_call
from interface_target.target_means import *
from utils.user_project import UserProject


class Riscv(ITarget):
    """
    Create the same interface and common pipeline to RISC-V architecture


    Parameters
    ----------
    project : UserProject
        All informations about user project


    Attributes
    ----------
    output_path : str
        Directory where report will be generated and its name

    mmcu : str
        Microcontroller of target. Example: atmega328, unknown

    serial_port : str
        Serial port to connect with board
    """
    def __init__(self, project):
        self.output_path = project.output_directory+project.main_file_name
        self.mmcu = project.microcontroller_unit
        self.serial_port = project.serial_port


class RiscvBoard(Board, Riscv):
    """
    Control RISC-V board pipeline


    Parameters
    ----------
    project : UserProject
        All informations about user project


    Attributes
    ----------
    output_path : str
        Directory where report will be generated and its name

    mmcu : str
        Microcontroller of target. Example: atmega328, unknown

    serial_port : str
        Serial port to connect with board
    """
    def __init__(self, project : UserProject) -> None:
        # explicit calls without super
        Board.__init__(self, project.serial_port)
        Riscv.__init__(self, project)


    def compile(self) -> None:
        '''
        Compile object file to RISC-V board executable


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("trying to compile to riscv...")
        pass


    def flash(self) -> None:
        '''
        Load the hex file to board


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("trying to compile to riscv...")
        pass


    def run(self, args : list) -> list:
        '''
        Execute once the program with input set


        Parameters
        ----------
        input : list
            Input values of one execution


        Returns
        -------
        output : list
            Response of board
        '''
        return super().run(args)
