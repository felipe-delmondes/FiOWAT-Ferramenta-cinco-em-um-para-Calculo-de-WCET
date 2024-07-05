from interface_target.avr import *
from interface_target.riscv import *
from collections.abc import Iterable
from os.path import join
import os
from itertools import chain


class InterfaceTarget():
    """
    Apply adapter pattern, to allow all methodologies using the same point to connect with boards and simulators


    Parameters
    ----------
    project : UserProject
        All informations about user project

    intermediate_values : IntermediateValues
        All intermediate information obtained by pre processing


    Attributes
    ----------
    project : UserProject
        All informations about user project

    intermediate_values : IntermediateValues
        All intermediate information obtained by pre processing

    arch : str
        Architecture of target. Example: arm, avr, riscv

    vendor : str
        Vendor of target. Example: pc, atmel

    os : str
        Operational system of target. Example: none, windows, linux

    mmcu : str
        Microcontroller of target. Example: atmega328, unknown

    llvm_path : str
        Directory where LLVM 16 is installed

    input_file : str
        Directory where main file is located and its name

    output_file : str
        Directory where report will be generated and its name

    bin : str
        Directory of bin folder of this repository

    env : str
        Define it is "board" or "simul"

    communicator : ITarget
        Object of Strategy Pattern, responsible to execute methods of selected board
    """

    def __init__(self, project: object, inter_values: object) -> None:
        self.project = project
        self.inter_values = inter_values
        self.arch = project.architecture
        self.vendor = project.vendor
        self.os = project.operational_system
        self.mmcu = project.microcontroller_unit
        self.llvm_path = project.llvm_path

        self.input_file = os.path.join(
            project.input_directory, project.main_file_name)
        self.output_file = os.path.join(
            project.output_directory, project.main_file_name)

        self.bin = join(os.getcwd(), "bin")
        self.env = project.get_env_name()

        if project.architecture == "avr":
            self.init_avr_communicator()
        elif project.architecture == "riscv32":
            self.init_risc_communicator()
        else:
            print(
                f"\n\33[41mError! Target architecture not supported!\33[0m")
            exit(-1)

    def init_avr_communicator(self) -> None:
        '''
        Initialize communication with AVR board or simulator


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        if self.project.board:
            self.communicator = AvrBoard(self.project)
        else:
            self.communicator = AvrSimulator(self.project)

    def init_risc_communicator(self) -> None:
        '''
        Initialize communication with RISC board or simulator


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        if self.project.board:
            self.communicator = RiscvBoard(self.project)
        else:
            print(
                f"\n\33[41mError! Target architecture does not support a simulator!\33[0m")
            exit(-1)

    def set_ga_filenames(self) -> None:
        '''
        Define file name for GA technique


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        self.input_file = self.input_file + "_inst"
        self.output_file = self.output_file + "_inst"
        self.communicator.output_path = self.output_file

    def backend_compile(self) -> None:
        '''
        Compile IR file to binary file of selected target


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        self.communicator.compile()

    def compile_io_ports(self) -> None:
        '''
        Compile with IO ports


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # self.lib_path = "{}/libs/{}-{}".format(self.bin, self.arch, self.env)
        self.lib_path = os.path.join(os.path.join(
            self.bin, "libs"), self.arch + "-" + self.env)
        print("Compiling to io-ports.c to IR...", end=" ")
        # cmd = "\"{}\"clang -O0 -S -I {} --target={}-{}-{} -mmcu={} -emit-llvm -c {}/io-ports.c -o {}/io-ports.ll".format(
        #     self.llvm_path, self.lib_path, self.arch, self.vendor, self.os, self.mmcu, self.lib_path, self.lib_path)
        cmd = "\"" + self.llvm_path + "clang\" -O0 -S -I \"" + self.lib_path + \
            "\" --target=" + self.arch + "-" + self.vendor + "-" + self.os + \
            " -mmcu=" + self.mmcu + " -emit-llvm -c \"" + \
            os.path.join(self.lib_path, "io-ports.c") + \
            "\" -o \"" + os.path.join(self.lib_path, "io-ports.ll") + "\""
        system_call(cmd)
        print("\33[42mDone\33[0m")
        return

    def compile_tick_counter(self) -> None:
        '''
        Compile with tick counter


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Compiling to tick-counter.c to IR...", end=" ")
        cmd = "\"" + self.llvm_path + "clang\" -O0 -S -I \"" + self.lib_path + \
            "\" --target=" + self.arch + "-" + self.vendor + "-" + self.os + \
            " -mmcu=" + self.mmcu + " -emit-llvm -c \"" + \
            os.path.join(self.lib_path, "tick-counter.c") + \
            "\" -o \"" + os.path.join(self.lib_path,
                                      "tick-counter.ll") + "\""
        system_call(cmd)
        print("\33[42mDone\33[0m")
        return

    def compile_to_ir(self) -> None:
        '''
        Compile to IR file


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Compiling to LLVM IR...", end=" ")
        # cmd = "\"{}\"clang -O0 -S -gline-tables-only -I {}/libs/{}-{} --target={}-{}-{} -mmcu={} -emit-llvm -c {}.c -o {}.ll".format(
        #     self.llvm_path, self.bin, self.arch, self.env, self.arch, self.vendor, self.os, self.mmcu, self.input_file, self.output_file)
        cmd = "\"" + self.llvm_path + "clang\" -O0 -S -gline-tables-only -I \"" + \
            os.path.join(os.path.join(self.bin, "libs"), self.arch + "-" + self.env) + \
            "\" --target=" + self.arch + "-" + self.vendor + "-" + self.os + \
            " -mmcu=" + self.mmcu + " -emit-llvm -c \"" + \
            self.input_file + ".c\" -o \"" + self.output_file + ".ll\""
        system_call(cmd)
        print("\33[42mDone\33[0m")
        return

    def setup_ipet_hybrid(self) -> None:
        '''
        Setup opt pass in IR file


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Inserting initialization in the IR...", end=" ")
        # cmd = "\"{}\"opt -S -load-pass-plugin {}/llvm_plugin/SetUpPass-build/libSetUpPass.so -passes=set-up -o {}.ll {}.ll".format(
        #     self.llvm_path, self.bin, self.output_file, self.output_file)
        cmd = "\"" + self.llvm_path + "opt\" -S -load-pass-plugin \"" + \
            os.path.join(os.path.join(os.path.join(self.bin, "llvm_plugin"), "SetUpPass-build"), "libSetUpPass.so") + \
            "\" -passes=set-up -o \"" + self.output_file + \
            ".ll\" \"" + self.output_file + ".ll\""
        system_call(cmd)
        print("\33[42mDone\33[0m")
        return

    def instrument_ipet_hybrid(self) -> None:
        '''
        Instrument basic blocks using opt pass in the IR file


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Inserting time instrumentation in the IR...", end=" ")
        # cmd = "\"{}\"opt -S -load-pass-plugin {}/llvm_plugin/InstrumentBasicBlocks-build/libInstrumentBasicBlocks.so -passes=inst-basic-blocks -o {}.ll {}.ll".format(
        #     self.llvm_path, self.bin, self.output_file, self.output_file)
        cmd = "\"" + self.llvm_path + "opt\" -S -load-pass-plugin \"" + \
            os.path.join(os.path.join(os.path.join(self.bin, "llvm_plugin"), "InstrumentBasicBlocks-build"), "libInstrumentBasicBlocks.so") + \
            "\" -passes=inst-basic-blocks -o \"" + self.output_file + \
            ".ll\" \"" + self.output_file + ".ll\""
        system_call(cmd)
        print("\33[42mDone\33[0m")
        return

    def instrument_wpevt(self) -> None:
        '''
        Use opt pass in the IR file of WPEVT methodology


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Inserting path instrumentation in the IR...", end=" ")
        # cmd = "\"{}\"opt -S -load-pass-plugin {}/llvm_plugin/WpevtPass-build/libWpevtPass.so -passes=wpevt-pass -o {}.ll {}.ll".format(
        #     self.llvm_path, self.bin, self.output_file, self.output_file)
        cmd = "\"" + self.llvm_path + "opt\" -S -load-pass-plugin \"" + \
            os.path.join(os.path.join(os.path.join(self.bin, "llvm_plugin"), "WpevtPass-build"), "libWpevtPass.so") + \
            "\" -passes=wpevt-pass -o \"" + self.output_file + \
            ".ll\" \"" + self.output_file + ".ll\""

        system_call(cmd)
        print("\33[42mDone\33[0m")
        return

    def set_ir(self) -> None:
        '''
        Read IR file


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        with open(f"{self.output_file}.ll", "r") as ir_file:
            self.inter_values.set_ir(ir_file.readlines())
        return

    def link(self) -> None:
        '''
        Link main IR file with external libs


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print(
            "Linking external libs \'io-ports.ll\' and \'tick-counter.ll\'...",
            end=" ")
        # cmd = "\"{}\"llvm-link -S {}.ll {}/libs/{}-{}/io-ports.ll {}/libs/{}-{}/tick-counter.ll -o {}.ll".format(
        #     self.llvm_path, self.output_file, self.bin, self.arch, self.env, self.bin, self.arch, self.env, self.output_file)
        cmd = "\"" + self.llvm_path + "llvm-link\" -S \"" + self.output_file + ".ll\" \"" + \
            os.path.join(os.path.join(os.path.join(self.bin, "libs"), self.arch + "-" + self.env), "io-ports.ll") + "\" \"" + \
            os.path.join(os.path.join(os.path.join(self.bin, "libs"), self.arch + "-" + self.env), "tick-counter.ll") + "\" -o \"" + \
            self.output_file + ".ll\""

        system_call(cmd)
        print("\33[42mDone\33[0m")
        return

    def compile_to_obj(self) -> None:
        '''
        Compile IR file to object file


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Compiling to object code...", end=" ")
        cmd = "\"{}\"llc -O0 -filetype=obj --mtriple={}-{}-{} -mcpu={} {}.ll -o {}.o".format(
            self.llvm_path, self.arch, self.vendor, self.os, self.mmcu, self.output_file, self.output_file)
        system_call(cmd)
        print("\33[42mDone\33[0m")
        return

    def compile_to_asm(self) -> None:
        '''
        Compile IR file to assembly file


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Compiling to assembly code...", end=" ")
        cmd = "\"{}\"llc -O0 -filetype=asm --mtriple={}-{}-{} -mcpu={} {}.ll -o {}.asm".format(
            self.llvm_path, self.arch, self.vendor, self.os, self.mmcu, self.output_file, self.output_file)
        system_call(cmd)
        print("\33[42mDone\33[0m")
        return

    def run(self, args: list) -> list:
        '''
        Receive the input set and run the board or simulator


        Parameters
        ----------
        args : list
            Input set of one execution, possible with list inside of list.

            Example: [2, 3, [4, 5, 1], 2]


        Returns
        -------
        response : list
            Result of execution
        '''
        flat_args = self.flatten(args)
        return self.communicator.run(flat_args)

    def flash(self) -> None:
        '''
        Load the binary file to board


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        self.communicator.flash()

    # def flatten(self, args : list) -> list:
    #     '''
    #     Convert the input set to a format readable for board or simulator

    #     Parameters
    #     ----------
    #     args : list
    #         Input set of one execution, possible with list inside of list.

    #         Example: [2, 3, [4, 5, 1], 2]

    #     Returns
    #     -------
    #     input : list
    #         Input values of one execution in unique list.

    #         Example: [2, 3, 4, 5, 1, 2]
    #     '''
    #     if isinstance(args, Iterable):
    #         return [a for i in args for a in self.flatten(i)]
    #     else:
    #         return [args]

    def flatten(self, args: list) -> list:
        '''
        Convert the input set to a format readable for board or simulator


        Parameters
        ----------
        args : list
            Input set of one execution, possible with list inside of list.

            Example: [2, 3, [4, 5, 1], 2]


        Returns
        -------
        input : list
            Input values of one execution in unique list.

            Example: [2, 3, 4, 5, 1, 2]
        '''
        if isinstance(args, Iterable):
            return list(chain.from_iterable(i if isinstance(i, list) else [i] for i in args))
        else:
            return [args]
