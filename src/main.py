from argparse import ArgumentParser
from pipeline.director import Director
import sys



def main(terminal_arguments) -> None:
    '''
    Read the system arguments to initialize the system


    Parameters
    ----------
    terminal_arguments : list
        Arguments of terminal (sys.argv[...])


    Returns
    -------
        None
    '''
    # Read this article for more information: https://docs.python.org/3/howto/argparse.html#argparse-tutorial
    # Create the interface program in terminal
    parser = ArgumentParser(
        prog="fiowat",
        usage="%(prog)s [--config <config.yaml> | --printtargets | --version]",
        description="FioWAT (Five in One WCET Analysis Tool) is a tool to calculate WCET of ANSI C program.\nSend a config.yaml file to fiowat with all setup to calculate WCET.",
        epilog="For more questions, check the manual in the folder \"doc\".")

    # Create a mutually exclusive group of flags
    group_run = parser.add_mutually_exclusive_group()

    # Add all possibles arguments to program
    # Optional arguments there are "-" or "--" before name.
    # Required arguments there aren't dash character. The order of declaration of "add_argument" is the same in terminal
    group_run.add_argument(
        "-c", "--config", type=str,
        help="Path to a YAML config file. See README for more informations",
        metavar="<config.yaml>")
    group_run.add_argument(
        "--printtargets", action="store_true",
        help="Print the list of architectures supported by FioWAT tool")
    group_run.add_argument("-v", "--version",
                           action="store_true",
                           help="Show the version of FioWAT program")

    # Read all flags from terminal
    #It's possible using none argument to automatically catch terminal arguments, but it's possible use explictly the "terminal_arguments" variable. It's easier to do tests
    args = parser.parse_args(terminal_arguments)

    # Optional arguments:
    if args.config:
        # Send the config.yaml file to Pipeline of FioWAT
        print("\33[44mStarting FioWAT analysis...\33[0m")
        wcet_run = Director(args.config)
        wcet_run.run_pipeline()

    elif args.printtargets:
        print("Architectures supported:")
        print("\33[1mStatic IPET:\33[0m")
        print("  - AVR")
        print("  - x86_64 (non accurate version)")

        print("\n\33[1mHybrid IPET | WPEVT:\33[0m")
        print("  - AVR")

        print("\n\33[1mGA Dynamic | EVT:\33[0m")
        print("  - Any board connected in serial port")

    elif args.version:
        print("FioWAT version 1.0.0")






if __name__ == "__main__":
    main(sys.argv[1:])