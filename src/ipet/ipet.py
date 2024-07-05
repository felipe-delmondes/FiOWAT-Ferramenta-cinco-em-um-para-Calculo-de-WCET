from cfg.graph_generator import *
from cfg.pre_processor import *
from pulp import *
from cfg.graph_weight import *
from utils.user_project import *


class Ipet:
    '''
    Estimate the Static WCET using IPET technique (Implicit Path Enumeration Technique);
    Or/And estimate the worst path using IPET technique.

    The variation depends of run method: <run_ipet_static | run_ipet_hybrid | run_ipet_constraint_solver>


    Parameters
    ----------
    graph : dict
        Graph of all program

    project : UserProject
        All informations about user project, for example triple target

    intermediate_values : IntermediateValues, default = None
        All intermediate information obtained by pre processing.

        By default, calculate WCET, but if there is intermediate_values, so its object register all worst path.


    Attributes
    ----------
    graph : dict
        Relationship between function name and list of basic blocks.
        It's implicit the function names are inserted in post order.

    project : UserProject
        All informations about user project, for example triple target

    intermediate_values : IntermediateValues
        All intermediate information obtained by pre processing. It's used in this context to store worst path  

    instruction_weight : dict
        IR instrucion weight in cycles. Example: 'alloca' = 10

    connections_in : list
        Edges enter in basic block.

        Example: [['start_0'], [], [], [], [], [], [], [], [], [], []]

    connections_out : list
        Edges out of basic block.

        Example: [[], [], [], []]

    mapping_edges_and_leave_blocks : dict
        Relationship between edges and weight.

        Example: {'start_0': 0}

    function : str
        Function name of current function under analysis    

    edges : dict
        Current functions edge. The relationship between its names and calculated weights.

        Example: {'start_0': 1374.0, '0_1': 67, '1_4': 21044.0, '5_6': 747.0}    

    model : LpSolver
        Pulp model, contain all constraints all objective function    

    objective : list
        Tuple with LpVariable and its respective edge.
        This format is need to LpAffineExpression() function convert to objective function format.

    variables : LpVariable
        LpVariable object, with name, weight        

    status : LpStatus
        LpStatus constant, this register the result of solver.
        Some examples are:
            - LpStatusOptimal : It's means the optimization was reached.
            - LpStatusInfeasible : Some problem with model prevent the optimization, for example, if the linear system has two mutually exclusive constraints. Example: "x > 5" and "x == 1".
            - LpStatusUnbounded : Some variable hasn't constraint, so the optimal value diverge to infinite. Example: just "x > 0" -> the value of x for maximize the objective function is infinite.
    '''

    def __init__(self, graph: dict, project: UserProject,
                 intermediate_values=None):
        self.graph = graph
        self.project = project
        self.intermediate_values = intermediate_values
        self.instructions_weight = define_instructions_weight(self.project)

        # Variables to calculate auxiliate the IPET
        self.connections_in = []  # Edges enter in each basic blocks
        self.connections_out = []  # Edges out of each basic blocks
        self.mapping_edges_and_leave_blocks = {}
        self.function = ""  # Current function name under analysis
        self.edges = {}  # Relationship between edges name and its weight

        # Variable of Pulp lib
        self.model = any  # Model that contain all restrictions and variables
        # Objective function (Maximize weight, or in other words, WCET)
        self.objective = any
        self.variables = any  # Variables of Linear Problem (Weight)
        self.status = any  # Result of optmization

    def __weight_statically(self) -> bool:
        '''
        Set weight using static weight (The CPI's sum of every instructions)


        Parameters
        ----------
            None


        Returns
        -------
        jump_next_function : bool
            If True, analyze next function, because the current function is void
        '''
        # If function hasn't basic blocks, so its weight is equal "call" instruction weight
        if (len(self.graph[self.function]) == 0):
            self.instructions_weight["call " +
                                     self.function] = self.instructions_weight['call']
            # Jump for next function
            return True

        # To avoid recursive functions, the start weight for recursive calling is same of call instruction
        self.instructions_weight["call " +
                                 self.function] = self.instructions_weight['call']
        # Calculates weight of each blocks
        update_basic_block_weight_statically(
            self.graph[self.function],
            self.instructions_weight)

        # Edges of basic block connections. Pair between block init and block end - weight. Example: {'5_33': 14}
        self.edges = {'start_0': self.graph[self.function][0].get_weight()}

        # Continue in same function
        return False

    def __update_basic_block_weight_dynamically(self) -> None:
        '''
        If the weight is obtained using measurements, so when there are "call" instruction, it's necessary add the weight of basic block and weight of "call function" calculated using IPET.
        For this reason, this method "update" the weight measured.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        for basic_block in self.graph[self.function]:
            total = basic_block.get_weight()
            for instruction in basic_block.get_instructions():
                if (instruction[0:4] == "call"):
                    total += self.instructions_weight[instruction]
            basic_block.set_weight(total)

    def __weight_hybrid(self) -> bool:
        '''
        Set weight using measurements weight (The CPI has already been measured)


        Parameters
        ----------
            None


        Returns
        -------
        jump_next_function : bool
            If True, analyze next function, because the current function is void
        '''
        # If function hasn't basic blocks, so its weight is zero, because it's cannot possible to measurement
        if (len(self.graph[self.function]) == 0):
            self.instructions_weight["call " + self.function] = 0
            # Jump for next function
            return True

        # To avoid recursive functions, the start weight for recursive calling is zero
        self.instructions_weight["call " + self.function] = 0

        # Propagate already calculated functions
        self.__update_basic_block_weight_dynamically()

        # Edges of basic block connections. Pair between block init and block end - weight. Example: {'5_33': 14}
        self.edges = {'start_0': self.graph[self.function][0].get_weight()}

        # Continue in same function
        return False

    def __setup(self) -> None:
        '''
        Create the initial conditions to analyze current function.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # Register variables in and out of each basic block
        self.connections_in = [[]
                               for i in range(len(self.graph[self.function]))]
        self.connections_out = [[]
                                for i in range(len(self.graph[self.function]))]

        # Relationship between edges and leave blocks
        self.mapping_edges_and_leave_blocks = {'start_0': 0}

        # Variables of problem
        self.variables = {}
        self.objective = []

        # Create model to maximize execution time
        self.model = pulp.LpProblem(name="IPET_WCET", sense=LpMaximize)

        # Create variables for each edge and its restrictions
        self.variables['start_0'] = LpVariable(
            'start_0', lowBound=1, cat='Integer')

        # All functions have entry point to first basic block connection
        self.connections_in[0].append('start_0')

    def __set_edges(self) -> None:
        '''
        Create edges of basic blocks to IPET can analyze.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # Find all edge in function, basic block by basic block
        for bb_index in range(0, len(self.graph[self.function])):
            # Find all directed edges to next blocks
            self.connections = self.graph[self.function][bb_index].get_next_blocks(
            )
            for next_bb_index in range(0, len(self.connections)):
                # Edge is formed by currente bb ID _ next bb ID, and its value is next basic block weight
                code = (str(bb_index) + "_" +
                        str(self.connections[next_bb_index]))
                self.edges[code] = self.graph[self.function][self.connections[
                    next_bb_index]].get_weight()

                # Relationship between edge and leave block
                self.mapping_edges_and_leave_blocks[code] = self.connections[next_bb_index]

                # Define which edges enter and leave the basic block
                self.connections_in[self.connections[next_bb_index]].append(
                    code)
                self.connections_out[bb_index].append(code)

    def __mapping_line_ir_and_number_executions(self) -> None:
        '''
        Mapping IR line and its executions number.


        Update this attributes of intermediate values:

        - worst_path_basic_block : dict
            All functions, and its relationship between basic blocks name of worst path and number of executions.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # Just main function cannot be mapped
        if (self.function == "main"):
            return

        # All basic block init with 0 executions numbers
        basic_block_number_executions = [0
                                         for i in range(
                                             self.model.numVariables())]

        # Count total number executions each basic block
        for v in self.model.variables():
            basic_block_number_executions[self.mapping_edges_and_leave_blocks
                                          [v.name]] += int(v.varValue)

        # Relationship between basic block name and number of executions. Example: ("block0", 1)
        i = 0
        max_bb = len(self.graph[self.function])
        while (i < max_bb):
            # Delete all unused basic block
            if (basic_block_number_executions[i] == 0):
                i += 1
                continue

            # Obtain just basic block name. Example: #;BubbleSort;block1 -> block1
            _, _, block = self.graph[self.function][i].get_name().split(";")

            # Store the worst path in graph, each function has tuples (basic block name, number of executions)
            self.intermediate_values.set_worst_path_basic_block(
                self.function, block,
                basic_block_number_executions[i])

            # Store the total of number of executions
            self.intermediate_values.increment_number_executions_worst_path(
                basic_block_number_executions
                [i])
            i += 1

    def __set_variables_ipet(self) -> None:
        '''
        Create a variable for each edge. This variable is object of Pulp module.

        This variables will be used in LPSolver.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        for edge in self.edges:
            # If find next block ID
            next_block_id = ""
            for i in range(edge.find("_") + 1, len(edge)):
                next_block_id += edge[i]
                self.variables[edge] = LpVariable(
                    edge, lowBound=0, cat='Integer')

        # Create tuples between: variable name - weight
        for edge in self.edges:
            self.objective.append((self.variables[edge], self.edges[edge]))

    def __structural_restriction(self) -> None:
        '''
        Structural restriction are restrictions about CFG rules of program.

        1 - Using "Kirchhoff Law" applied in computation, the sum of entry in a basic block is same of all exits.

        2- All exit points of function can be entry once. 


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # **** Structural constraint ****
        # The sum of all enter edges is same all leave edges
        if (len(self.graph[self.function]) > 1):
            for bb in range(0, len(self.graph[self.function])):
                # If one block hasn't leave edges, it means it's exit point
                if (len(self.connections_out[bb]) == 0):
                    continue
                else:
                    self.model += lpSum(self.variables[self.connections_in[bb][ed]] * 1 for ed in range(0, len(self.connections_in[bb]))) + lpSum(
                        self.variables[self.connections_out[bb][ed]] * -1 for ed in range(0, len(self.connections_out[bb]))) == 0
        # If just have enter edges, so the sum is equal 1, because this basic block is exit point (It's possible enter it once)
        else:
            self.model += lpSum(
                self.variables[self.connections_in[0][ed]] * 1
                for ed in range(0, len(self.connections_in[0]))) == 1

    def __semantic_restrictions(self) -> None:
        '''
        Semantic restrictions are restrictions using loop bound, or value analysis.

        1- All function has one entry point that is executed once

        2- All function has many exit points and just one can be executed once

        3- All loops has maximum executions times, and the edge can be the entry point or exit point (The edge that has one path, to avoid unbounded situation)


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # **** Semantic constraint ****
        # All function have entry point and it's executed once
        self.model += self.variables['start_0'] == 1
        # All function can exit in one point
        exit_points = []
        for bb in range(0, len(self.graph[self.function])):
            # Exit point hasn't next blocks, so you store all "enter connections"
            if (len(self.connections_out[bb]) == 0):
                for ed in range(0, len(self.connections_in[bb])):
                    exit_points.append(self.connections_in[bb][ed])
        self.model += lpSum(self.variables[exit_points[i]]
                            for i in range(0, len(exit_points))) == 1
        # Set loop bounds
        for bb in range(0, len(self.graph[self.function])):
            # Loop by definition need repeat at least twice
            if (self.graph[self.function][bb].get_number_executions() > 1):
                if (len(self.graph[self.function][bb].get_next_blocks()) == 1):
                    # Loop bound has one exit point, so use the next edge
                    self.model += self.variables[self.connections_out[bb][0]
                                                 ] == self.graph[self.function][bb].get_number_executions()
                else:
                    # Loop bound there is one entry point, so use the first enter edge
                    self.model += self.variables[self.connections_in[bb][0]
                                                 ] == self.graph[self.function][bb].get_number_executions()

    def __error_message(self) -> None:
        '''
        Some problem occured when tried optimize the linear system, so raise an error and abort the execution.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Function: " + self.function)
        print(
            "\33[41mError! The model had a defect.\nPlease, contact development team!\33[0m")
        print("Solver status: ", LpStatus[self.status])
        print("Look it up in https://www.coin-or.org/PuLP/constants.html#pulp.constants.LpMaximize")
        exit(1)

    def __reset_variables(self) -> None:
        '''
        Reset all variables after optimize one function.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        self.edges.clear()
        self.mapping_edges_and_leave_blocks.clear()

    def __default_main(self) -> int:
        '''
        If the function target wasn't found, so by default, calculate this .


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # The IPET main objective is know main function WCET, because this is same program WCET
        print("\33[42mIPET finished.\33[0m")
        print("\33[43mWarning: The function selected by user wasn't found, so the FioWAT selected 'main function'\33[0m")
        return self.instructions_weight['call main']

    def __debug(self) -> None:
        '''
        If it happened an error or the develop team wants debug the IPET, just add this method some point of execution to show the major values of linear system.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("\n\n\nFunction: ", self.function)
        print("Objective function: ", self.model.objective)
        print("Constraints: ", self.model.constraints)
        print("Enter edges: ", self.connections_in)
        print("Leave edges: ", self.connections_out)
        print("Number of constraints: ", self.model.numConstraints())
        print("Number of variables: ", self.model.numVariables())
        print("Number of duplicate variables: ",
              self.model.checkDuplicateVars())
        print("WCET of function: ", value(self.model.objective))
        print("Execution number for each variable:")
        for v in self.model.variables():
            if v.varValue > 0:
                print(f'{v.name} = {v.varValue:.1f}')


###########################################################################################

    def run_ipet_static(self) -> float:
        '''
        Calculate the Static WCET of function target, calculating the WCET of every function transverse the graph in post order.

        For this method, use static weight (The CPI's sum of every instrunction for each basic block)


        Parameters
        ----------
            None


        Returns
        -------
        swcet : float
            The WCET of function target. The units usually are in cycles
        '''
        print("Starting Static IPET...")
        # Calculate WCET function by function, in call graph post order
        for self.function in self.graph:
            '''
            Step 01 - Create objective function and variables
            '''
            # Calculate the static weight for this function
            if (self.__weight_statically()):
                continue

            # Initialize the variables and edges for this function
            self.__setup()
            self.__set_edges()
            self.__set_variables_ipet()

            # Convert each pair variable - weight in linear sum. Example: [(x[0],1), (x[1],-3), (x[2],4)]  ->  1*x_0 + -3*x_1 + 4*x_2 + 0
            # This expression is objective function. What we want to optimize (function WCET)
            self.model.setObjective(LpAffineExpression(self.objective))

            '''
            Step 02 - Build the restrictions
            '''
            self.__structural_restriction()
            self.__semantic_restrictions()

            '''
            Step 03 - Optimize the Linear Problem
            '''
            # Solve linear system and disable log in terminal
            self.status = self.model.solve(PULP_CBC_CMD(msg=0))

            '''
            Step 04 - Analyze the result
            '''
            if (self.status == pulp.const.LpStatusOptimal):
                print("Function: " + self.function,
                      "--- Otimization complete!")

                # The function WCET is considered like "instruction weight" for other functions. It's important add call instruction weight (function call cost)
                self.instructions_weight["call " + self.function] = self.instructions_weight['call'] + value(
                    self.model.objective)

                # Stop the IPET and return the function target selected by user
                if (self.project.get_function_target() == self.function):
                    print(
                        "\33[42mIPET finished.\33[0m WCET of function\33[1m \""
                        + self.function + "\" \33[0mcalculated.")
                    return self.instructions_weight["call " + self.function]

            else:
                self.__debug()
                self.__error_message()

        # Return WCET of all program
        return self.__default_main()


###########################################################################################

    def run_ipet_hybrid(self) -> float:
        '''
        Calculate the Static WCET of function target, calculating the WCET of every function transverse the graph in post order.

        For this method, use measured weight (The CPI's sum of measured weight and WCET of all "call function" inside of basic block)


        Parameters
        ----------
            None


        Returns
        -------
        swcet : float
            The WCET of function target. The units usually are in cycles
        '''
        print("Starting Hybrid IPET...")
        # Calculate WCET function by function, in call graph post order
        for self.function in self.graph:
            '''
            Step 01 - Create objective function and variables
            '''
            # Calculate the weight for this function using measurements
            if (self.__weight_hybrid()):
                continue

            # Initialize the variables and edges for this function
            self.__setup()
            self.__set_edges()
            self.__set_variables_ipet()

            # Convert each pair variable - weight in linear sum. Example: [(x[0],1), (x[1],-3), (x[2],4)]  ->  1*x_0 + -3*x_1 + 4*x_2 + 0
            # This expression is objective function. What we want to optimize (function WCET)
            self.model.setObjective(LpAffineExpression(self.objective))

            '''
            Step 02 - Build the restrictions
            '''
            self.__structural_restriction()
            self.__semantic_restrictions()

            '''
            Step 03 - Optimize the Linear Problem
            '''
            # Solve linear system and disable log in terminal
            self.status = self.model.solve(PULP_CBC_CMD(msg=0))

            '''
            Step 04 - Analyze the result
            '''
            if (self.status == pulp.const.LpStatusOptimal):
                print("Function: " + self.function,
                      "--- Otimization complete!")
                # The function WCET is considered like "instruction weight" for other functions
                self.instructions_weight["call " + self.function] = value(
                    self.model.objective)

                # Stop the IPET and return the function target selected by user
                if (self.project.get_function_target() == self.function):
                    print(
                        "\33[42mIPET finished.\33[0m WCET of function\33[1m \""
                        + self.function + "\" \33[0mcalculated.")
                    return self.instructions_weight["call " + self.function]

            else:
                self.__debug()
                self.__error_message()

            # Reset all variables
            self.__reset_variables()

        # Return WCET of all program
        return self.__default_main()


###########################################################################################

    def run_ipet_constraint_solver(self) -> float:
        '''
        Calculate the Static WCET of function target, calculating the WCET of every function transverse the graph in post order.

        For this method, use measured weight (The CPI's sum of measured weight and WCET of all "call function" inside of basic block)

        Also, the worst path for each optimized function is stored in intermediate_values object.


        Update this attributes of intermediate values:

        - worst_path_basic_block : dict
            The worst path calculated (Execution number for each basic block).

            Example: {'scanf': [(149, 1)], 'fatorial': [(166, 1), (179, 1), (188, 1)]}



        Parameters
        ----------
            None


        Returns
        -------
        swcet : float
            The WCET of function target. The units usually are in cycles
        '''
        # Prevent intermediate_values null
        if (self.intermediate_values == None):
            print(
                "\33[41mError! Intermediate Values cannot be null if use constraint solver method\33[0m")
            exit(1)

        print("Starting Constraint Solver...")
        # Calculate WCET function by function, in call graph post order
        for self.function in self.graph:
            '''
            Step 01 - Create objective function and variables
            '''
            # Calculate the weight for this function using measurements
            if (self.__weight_hybrid()):
                continue

            # Initialize the variables and edges for this function
            self.__setup()
            self.__set_edges()
            self.__set_variables_ipet()

            # Convert each pair variable - weight in linear sum. Example: [(x[0],1), (x[1],-3), (x[2],4)]  ->  1*x_0 + -3*x_1 + 4*x_2 + 0
            # This expression is objective function. What we want to optimize (function WCET)
            self.model.setObjective(LpAffineExpression(self.objective))

            '''
            Step 02 - Build the restrictions
            '''
            self.__structural_restriction()
            self.__semantic_restrictions()

            '''
            Step 03 - Optimize the Linear Problem
            '''
            # Solve linear system and disable log in terminal
            self.status = self.model.solve(PULP_CBC_CMD(msg=0))

            '''
            Step 04 - Analyze the result
            '''
            if (self.status == pulp.const.LpStatusOptimal):
                print("Function: " + self.function,
                      "--- Otimization complete!")

                # The function WCET is considered like "instruction weight" for other functions
                self.instructions_weight["call " + self.function] = value(
                    self.model.objective)
                self.__mapping_line_ir_and_number_executions()

                # Stop the IPET and return the function target selected by user
                if (self.project.get_function_target() == self.function):
                    print(
                        "\33[42mIPET finished.\33[0m WCET of function\33[1m \""
                        + self.function + "\" \33[0mcalculated.")
                    # print(self.intermediate_values.get_all_worst_path_basic_block())
                    return self.instructions_weight["call " + self.function]

            else:
                self.__debug()
                self.__error_message()

            # Reset all variables
            self.__reset_variables()

        # Return WCET of all program
        return self.__default_main()
