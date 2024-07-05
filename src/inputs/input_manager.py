from inputs.generators import *
from utils.user_project import UserProject
from utils.intermediate_values import IntermediateValues


class InputManager():
    """
    Create input variables object and control the pipeline to generate input values


    Parameters
    ----------
    project : UserProject
        Contain all information about project

    inter_values : IntermediateValues
        All intermediate information obtained by pre processing


    Attributes
    ----------
    inter_values : IntermediateValues
        All intermediate information obtained by pre processing

    input_types : list
        List with all types of each input. Example: [int(15), float, int]

    input_bounds_min : list
        List with all minimum values each input can be. Example: [-7, 0]

    input_bounds_max : list
        List with all maximum values each input can be. Example: [-2, 10]

    test_cases : int
        Number of test cases to coverage all code

    cbmc_path : str
        Directory to executable of CBMC
    """

    def __init__(self, project: UserProject, inter_values: IntermediateValues) -> None:
        self.inter_values = inter_values
        self.input_types = project.input_types
        self.input_bounds_min = project.input_bounds_min
        self.input_bounds_max = project.input_bounds_max
        self.test_cases = project.input_n_test_cases
        self.cbmc_path = project.cbmc_path
        self.project = project

        self.set_variables()

        # Select the way to generate inputs for code coverage
        if project.input_gen_method == "random":
            self.generator = RandomInputGenerator(
                self.variables, self.test_cases)
        elif project.input_gen_method == "cbmc":
            self.generator = CBMCInputGenerator(self.project)
        elif project.input_gen_method == "none":
            self.generator = False

    def set_variables(self) -> None:
        '''
        Create variable object to group all attributes about inputs


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        variables = []
        for type, min, max in zip(
                self.input_types, self.input_bounds_min, self.input_bounds_max):
            var = Variable(type)
            var.set_bounds(min, max)
            var.check_type()
            variables.append(var)
        self.variables = variables


    def get_variables(self) -> object:
        '''
        Create variable object to group all attributes about inputs


        Parameters
        ----------
            None


        Returns
        -------
        variable : Variable
            Object with all attributes of variable
        '''
        return self.variables


    def generate_inputs(self) -> set:
        '''
        Create inputs using selected method


        Parameters
        ----------
            None


        Returns
        -------
        test_cases_list : set
            Set of set of input for multiples executions
        '''
        print("Generating test cases for code coverage...", end=" ")
        test_cases_list = self.generator.run()
        print("\33[42mDone\33[0m")
        return test_cases_list


class Variable():
    """
    Organize all attributes of input in one object


    Parameters
    ----------
    string : str
        type information and maybe execution number


    Attributes
    ----------
    array : bool
        If is a array or not

    type : type
        Type of variable. Example: float, int

    size : int
        Number of elements. If is array is > 1, else is == 1
    """

    def __init__(self, string: str) -> None:
        regex = r"(int|float)\((\d+)\)"
        match = re.match(regex, string)

        # Array
        if match:
            self.array = True
            self.type, size = match.groups()
            self.size = int(size)
        # Variable
        else:
            self.array = False
            self.type = string
            self.size = 1


    def set_bounds(self, min: any, max: any) -> None:
        '''
        Set bounds minimum and maximum for each variable


        Parameters
        ----------
        min : int
            Minimum value for the variable

        max : int
            Maximum value for the variable


        Returns
        -------
            None
        '''
        self.min_value = min
        self.max_value = max
        self.check_bounds()


    def check_type(self) -> bool:
        '''
        Check if variable type is numeric, else raises an error


        Parameters
        ----------
            None


        Returns
        -------
        is_valid_type : bool
            Result of check
        '''
        if self.type in ["int", "float"]:
            return True
        else:
            print(f"Erro! Unknonw type \'{self.type}\'")
            exit(-1)


    def check_bounds(self) -> None:
        '''
        Check if types of bounds are the same of input. Raises an error if types are differents


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        if self.type == "int":
            if not isinstance(
                    self.min_value, int) or not isinstance(
                    self.max_value, int):
                print(
                    f"\33[41mError! Bounds min and max for int must be instance of int.\33[0m")
                exit(-1)
        if self.type == "float":
            if not isinstance(
                    self.min_value, float) or not isinstance(
                    self.max_value, float):
                print(
                    f"\33[41mError! Bounds min and max for float must be instance of float.\33[0m")
                exit(-1)