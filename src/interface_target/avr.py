import subprocess
from interface_target.i_target import ITarget
from cfg.timeMeter_aux import system_call
from interface_target.target_means import *
from utils.user_project import UserProject


class Avr(ITarget):
    """
    Create the same interface and common pipeline to AVR architecture


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
        self.output_path = project.output_directory+project.main_file_name
        self.mmcu = project.microcontroller_unit
        self.serial_port = project.serial_port


    def compile_to_elf(self) -> None:
        '''
        Compile object file to elf file in AVR board


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        cmd = "avr-gcc -O0 -std=c99 -pedantic -mmcu={} {}.o -o {}.elf".format(
            self.mmcu, self.output_path, self.output_path)
        system_call(cmd)
        return


    def compile_to_hex(self) -> None:
        '''
        Compile elf file to hex file in AVR board


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        cmd = "avr-objcopy -O ihex {}.elf {}.hex".format(
            self.output_path, self.output_path)
        system_call(cmd)
        return







class AvrBoard(Board, Avr):
    """
    Control AVR board pipeline


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
        Avr.__init__(self, project)


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
        print("Flashing code to AVR board...")
        cmd = "avrdude -p {}p -c arduino -P {} -U flash:w:{}.hex:i".format(
            self.mmcu, self.serial_port, self.output_path)
        system_call(cmd)
        print("\33[42mDone\33[0m")
        return


    def compile(self) -> None:
        '''
        Compile object file to AVR board executable


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Compiling code to AVR board...", end=" ")
        super().compile_to_elf()
        super().compile_to_hex()
        print("\33[42mDone\33[0m")
        return


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




class AvrSimulator(Simulator, Avr):
    """
    Control AVR simulator pipeline


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
        Simulator.__init__(self)
        Avr.__init__(self, project)


    def flash(self) -> None:
        '''
        Do anything, because it's not necessary load the executable file to simulator.

        It's method allow the class has the same interface


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Flashing code to AVR simulator...", end=" ")
        print("\33[42mDone\33[0m")
        return


    def compile(self) -> None:
        '''
        Compile object file to AVR simulator executable


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Compiling code to AVR simulator...", end=" ")
        super().compile_to_elf()
        print("\33[42mDone\33[0m")
        return


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
            Response of AVR simulator
        '''
        args = "\n".join([str(x) for x in args])
        cmd = "simulavr -d {} -f {}.elf -W 0x20,- -R 0x22,- -T exit".format(
            self.mmcu, self.output_path)
        try:
            process = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, shell=True)

            stdout, stderr = process.communicate(input=str(args).encode())

            if process.returncode != 0:
                print(
                    f"\n\33[41mError while executing the command {cmd}: {stderr.decode()}\33[0m")
                exit(-1)

            return stdout.decode().split("\n")

        except Exception as e:
            print(
                f"\33[41mError trying to execute the command {cmd}: {e}\33[0m")
            exit(-1)
