import subprocess
from ast import literal_eval
import re
import numpy as np
from utils.user_project import UserProject


class RandomInputGenerator():
    """
    Generate random inputs for code coverage


    Parameters
    ----------
    variables : Variables
        Contain all bounds and types of each input variable


    Attributes
    ----------
    rng : Numpy
        Range of pseudorandom values

    variables : Variables
        Contain all bounds and types of each input variable
    """

    def __init__(self, variables, test_cases) -> None:
        self.test_cases = test_cases
        self.rng = np.random.default_rng(seed=42)
        self.variables = variables

    def generate_random_type(
            self, type: str, min: int, max: int, size: int) -> list:
        '''
        Generate the random value for specified type.


        Parameters
        ----------
        type : str
            Type of variable. Example: int, float

        min : int
            Minimum value for the variable

        max : int
            Maximum value for the variable

        size : int
            Number of elements. If is array is > 1, else is == 1


        Returns
        -------
        inputs : list
            Input values for execute in program under analysis
        '''
        if type == "int":
            return self.rng.integers(
                low=min,
                high=max,
                size=size).tolist()
        if type == "float":
            array_in_range = (max - min) * self.rng.random(size=size) + min
            return array_in_range.tolist()

    def generate_random_input(self) -> list:
        '''
        Create pseudorandom values to create an set of input for one execution


        Parameters
        ----------
            None


        Returns
        -------
        random_input : list
            Set of input for one execution
        '''
        random_input = []
        for var in self.variables:
            if var.array:
                value = self.generate_random_type(
                    var.type, var.min_value,
                    var.max_value,
                    var.size)
            else:
                value = self.generate_random_type(
                    var.type, var.min_value,
                    var.max_value,
                    1)[0]

            random_input.append(value)

        return random_input

    def run(self) -> list:
        '''
        Create a list with many set of inputs for multiple executions


        Parameters
        ----------
            None


        Returns
        -------
        test_cases_list : list
            Set of set of input for multiples executions
        '''
        test_cases_list = []
        for _ in range(self.test_cases):
            test_cases_list.append(self.generate_random_input())
        return test_cases_list


class CBMCInputGenerator():
    """
    Generate inputs for code coverage using CBMC tool.

    This tool needs source code with instructions that allow using symbolic execution


    Parameters
    ----------
    project : UserProject
        Contain all information about project


    Attributes
    ----------
    file : str
        Absolute directory to source code file modified for CBMC tool

    cbmc_path : str
        Absolute directory to CBMC tool
    """

    def __init__(self, project: UserProject) -> None:
        self.file = project.input_directory+project.main_file_name+"_cbmc.c"
        self.cbmc_path = project.cbmc_path

    def parse_cbmc_output(self, cmbc_output) -> list:
        '''
        Receive CBMC test cases for code coverage


        Parameters
        ----------
            None


        Returns
        -------
        test_cases_list : list
            Set of set of input for multiples executions
        '''
        tests = cmbc_output[-1]['tests'][0]
        print("CBMC test suite generation: ", cmbc_output[-2]['messageText'])
        print("CBMC test suite coverage: ", cmbc_output[-3]['messageText'])
        match = re.search(r'\(([\d.]+)%\)', cmbc_output[-3]['messageText'])
        percent = float(match.group(1))
        if percent < 95:
            print(cmbc_output)
        inputs = tests['inputs']
        test_cases_list = []
        args_list = []
        n_args = len(self.input_types)
        for var in inputs:
            value = var['value']['data']
            args_list.append(value)
            if len(args_list) == n_args:
                test_cases_list.append(args_list)
                args_list = []
        print(test_cases_list)
        return test_cases_list

    def run(self) -> set:
        '''
        Run the CBMC tool for find input values for code coverage


        Parameters
        ----------
            None


        Returns
        -------
        test_cases_list : set
            Set of set of input for multiples executions
        '''
        # Run the CBMC
        cmd = "{}cbmc {} --cover location --show-test-suite --unwind 10 --json-ui".format(
            self.cbmc_path, self.file)
        print(f"Running {cmd}")
        result = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True)

        # Read the result of CBMC
        if result.returncode != 0:
            print(f"Error executing the cmd {cmd}")
            print(result.stderr, result.stdout)
            exit(-1)
        else:
            cbmc_output = self.parse_cbmc_output(
                literal_eval(result.stdout))
            return set(cbmc_output)
