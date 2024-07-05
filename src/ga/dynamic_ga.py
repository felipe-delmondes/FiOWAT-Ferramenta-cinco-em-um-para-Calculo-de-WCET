import pygad
from constraint_solver.worst_path import worst_path_match
from utils.user_project import UserProject
from utils.intermediate_values import IntermediateValues
from inputs.input_manager import InputManager
from interface_target.interface_target import InterfaceTarget


class GA():
    '''
    Estimate the dynamic WCET 
    Or, given a worst path, search for the input that entails this path
    Using PyGaD as library of a genetic algorithm

    The variation depends of run method: <dynamic_ga | WPEVT>


    Parameters
    ----------
    project : UserProject
        Contain all information about project

    input_manager
        Contain all information about the input vector

    interface_target
        Contain all information about the board / simulator target

    inter_values: IntermediateValues
        Contain all intermediate information obtained by pre processing


    Attributes
    ----------
    csst : string
        Define the crossover selection type to be chosen in GA

    gen_type : list
        Define the type of each variable to be optimized

    gen_space : list
        Define the min and max bound of each variable to be optimized

    interface_target : InterfaceTarget instance
        Contain all information about the board / simulator target

    inter_values : IntermediateValues instance
        Contain all intermediate information obtained by pre processing

    mtt : string
        Define the mutation type to be chosen in GA

    mtpg : list
        Define the percentage of mutation to be used in GA
        If the mutation type is adaptive, then a list containing two values must be passed.
            The first will be used in the beggining, due to major differences
            The second will be used when the fitness values are closer between generations
        Else only one value will be utilized during the whole execution

    num_genes : int
        Define the length of the input to be optimized

    pst : string
        Define the parent selection type to be chosen in GA

    pygad_instance : pygad.GA
        Contain all information about the class GA used in PyGaD.
        For more information: https://pygad.readthedocs.io/en/latest/

    stop_criteria : string
        Define the criteria for previously end the optimization
    '''

    def __init__(self, project: UserProject, input_manager: InputManager, interface_target: InterfaceTarget, inter_values: IntermediateValues) -> None:
        self.pst = project.ga_pst
        self.csst = project.ga_csst
        self.mtt = project.ga_mtt
        if self.mtt == "adaptive":
            self.mtpg = project.ga_mtpg
        else:
            self.mtpg = project.ga_mtpg[0]

        gen_space = []
        gen_type = []
        for var in input_manager.get_variables():
            gen_space += [{'low': var.min_value,
                           'high': var.max_value}] * var.size
            gen_type += [type(var.min_value)] * var.size

        self.gen_type = gen_type
        self.gen_space = gen_space
        self.num_genes = len(gen_space)

        if project.ga_stop_criteria:
            self.stop_criteria = "saturate_"+str(self.num_genes**2)
        else:
            self.stop_criteria = "saturate_"+str(self.num_genes**3)

        self.interface_target = interface_target

        self.inter_values = inter_values


    def fitness_dynamic_ga(self, pygad_instance: pygad.GA, solution: list, solution_idx: list) -> int:
        '''
        Set fitness parameter for methodology Dynamic GA


        Parameters
        ----------
        pygad_instance : pygad.GA
            Instance of object of Genetic Algorithm

        solution : list
            Solution vector of problem

        solution_idx : list
            Parameter not used, but Pygad lib needs it


        Returns
        -------
        fitness : int
            Returns the number of execution cycles for the input given
        '''
        output = self.interface_target.run(solution)
        fitness = int([line.split(" ")[-1]
                       for line in output if line and line[:2] == "#c"][0])
        return fitness

    def instanciate_dynamic_ga(self) -> None:
        '''
        Instanciate the GA for the dynamic methodology


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        self.pygad_instance = pygad.GA(
            num_generations=self.num_genes ** 3, sol_per_pop=self.num_genes*3,
            num_parents_mating=int(self.num_genes),
            fitness_func=self.fitness_dynamic_ga, num_genes=self.num_genes,
            gene_space=self.gen_space, parent_selection_type=self.pst,
            keep_elitism=10, crossover_type=self.csst, mutation_type=self.mtt,
            mutation_percent_genes=self.mtpg, gene_type=self.gen_type,
            stop_criteria=self.stop_criteria, random_seed=4,
            on_generation=self.print_generations)

    def filter_output_wpevt(self, output: list) -> dict:
        '''
        Function to bond the output of path block and create a vector for comparision


        Parameters
        ----------
        output : list
            Response of board/simulator


        Returns
        -------
        path_blocks : dict
            Basic block path
        '''
        path_blocks = {}
        for line in output:
            if line and line[:2] == "#;":
                _, func, block = line.split(";")
                if func not in path_blocks:
                    path_blocks[func] = {}
                if block not in path_blocks[func]:
                    path_blocks[func][block] = 1
                else:
                    path_blocks[func][block] += 1
        return path_blocks

    def fitness_wpevt(self, ga_instance: pygad.GA, solution: list, solution_idx: list) -> float:
        '''
        Set fitness parameter for methodology Dynamic GA


        Parameters
        ----------
        pygad_instance : pygad.GA
            Instance of object of Genetic Algorithm

        solution : list
            Solution vector of problem

        solution_idx : list
            Parameter not used, but Pygad lib needs it


        Returns
        -------
        match : float
            Returns the percentage of match between the worst path and the path for the input given
        '''

        output = self.interface_target.run(solution)
        path_blocks = self.filter_output_wpevt(output)
        match = worst_path_match(self.inter_values, path_blocks)
        return round(match,6)

    def instanciate_wpevt_ga(self) -> None:
        '''
        Instanciate the GA for the WPEVT methodology


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        self.pygad_instance = pygad.GA(
            num_generations=self.num_genes ** 3, sol_per_pop=self.num_genes*3,
            num_parents_mating=int(self.num_genes),
            fitness_func=self.fitness_wpevt, num_genes=self.num_genes,
            gene_space=self.gen_space, parent_selection_type=self.pst,
            keep_elitism=10, crossover_type=self.csst, mutation_type=self.mtt,
            mutation_percent_genes=self.mtpg, gene_type=self.gen_type,
            stop_criteria=["reach_0.9", self.stop_criteria], random_seed=4,
            on_generation=self.print_generations)

    def run(self) -> None:
        '''
        Execute the instanciated GA.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Running GA...")
        self.pygad_instance.run()
        print("\33[42mDone\33[0m")

    def print_generations(self, pygad_instance: pygad.GA) -> None:
        '''
        Print intermediate values in the GA execution.
        Each 10 generations, the generations number, the solution vector and fiteness value obtained until that moment are exhibited.


        Parameters
        ----------
        pygad_instance : pygad.GA
            Instance of object of Genetic Algorithm


        Returns
        -------
            None
        '''
        if pygad_instance.generations_completed % 10 == 0:
            print("Generation Completed: ", pygad_instance.generations_completed)
            print("Solution: ", pygad_instance.best_solution()[0])
            print("Fitness: ", pygad_instance.best_solution()[1])

    def best_solution(self) -> list:
        '''
        After the execution of GA, returns the solution.


        Parameters
        ----------
            None


        Returns
        -------
        solution : list
            The list of optimized outputs after the execution of GA
        '''

        solution, wcet_ga, solution_idx = self.pygad_instance.best_solution()
        return solution
