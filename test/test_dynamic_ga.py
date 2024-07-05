from setup_test import *
from io import *
from src.ga.dynamic_ga import *

project = Mock()
interface_target = Mock()
input_manager = Mock()
inter_values = Mock()
var1 = Mock()

var1.min_value = 0
var1.max_value = 10
var1.size = 10
project.ga_pst = "sss"
project.ga_csst = "two_points"
project.ga_mtt = "adaptive"
project.ga_mtpg = [70,15]
project.ga_stop_criteria = True

def ga_constructor():

    var = [var1]
    input_manager.get_variables.return_value = var
    inter_values.get_number_executions_worst_path.return_value = 419.0
    inter_values.get_all_worst_path_basic_block.return_value = {'BubbleSort': [('block0', 1), 
                                                                                ('block1', 11),('block2', 11), 
                                                                                ('block3', 66),('block4', 66), 
                                                                                ('block5', 11),('block6', 55), 
                                                                                ('block7', 55),('block8', 55), 
                                                                                ('block9', 55),('block10', 11), 
                                                                                ('block11', 1),('block12', 10), 
                                                                                ('block13', 10),('block14', 1)]}
    return GA(project=project, input_manager=input_manager,
            interface_target=interface_target, inter_values=inter_values)
    

class Test_Dynamic_ga(unittest.TestCase):
    interface_target.run.return_value = ["Dynamic_ga", "BubbleSort", "Function", "#cycles 7560", "Bye Bye"]
    
    # VC-406
    def test_01_InputsTypeLengthMinMax(self):
        gs = [{'low': 0,'high': 10}] * 10
        gt = [int]*10
        ga = ga_constructor()

        self.assertEqual(ga.gen_space,gs)
        self.assertEqual(ga.gen_type,gt)
        self.assertEqual(ga.num_genes,10)

    # VC-407
    def test_02_HyperParameters_mttAdaptive(self):
        ga = ga_constructor()
        
        self.assertEqual(ga.pst,"sss")
        self.assertEqual(ga.csst,"two_points")
        self.assertEqual(ga.mtt,"adaptive")
        self.assertEqual(ga.mtpg,[70,15])
        self.assertEqual(ga.stop_criteria,"saturate_100")

    # VC-408
    def test_03_HyperParameters_mttNotAdaptive(self):
        # Modifica o project para branch coverage
        project.ga_mtt = "scramble"
        project.ga_stop_criteria = False
        ga = ga_constructor()
        
        ga.instanciate_dynamic_ga()

        self.assertEqual(ga.mtt,"scramble")
        self.assertEqual(ga.mtpg,70)
        self.assertEqual(ga.stop_criteria,"saturate_1000")
        self.assertEqual(ga.pygad_instance.mutation_type,"scramble")
        self.assertEqual(ga.pygad_instance.mutation_percent_genes,70)
        self.assertEqual(ga.pygad_instance.stop_criteria,[['saturate',1000]])

        # Retorna o project para o padrão
        project.ga_mtt = "adaptive"
        project.ga_stop_criteria = True
    
    # VC-409
    def test_04_GAPygadInstanciate(self):
        ga = ga_constructor()
        
        ga.instanciate_dynamic_ga()
        
        gs = [{'low': 0,'high': 10}] * 10
        gt = [[int,None]]*10
        self.assertEqual(ga.pygad_instance.num_generations,1000)
        self.assertEqual(ga.pygad_instance.sol_per_pop,30)
        self.assertEqual(ga.pygad_instance.num_parents_mating,10)
        self.assertEqual(ga.pygad_instance.num_genes,10)
        self.assertEqual(ga.pygad_instance.gene_space,gs)
        self.assertEqual(ga.pygad_instance.parent_selection_type,"sss")
        self.assertEqual(ga.pygad_instance.keep_elitism,10)
        self.assertEqual(ga.pygad_instance.crossover_type,"two_points")
        self.assertEqual(ga.pygad_instance.mutation_type,"adaptive")
        self.assertEqual(ga.pygad_instance.mutation_percent_genes,[70,15])
        self.assertEqual(ga.pygad_instance.stop_criteria,[['saturate',100]])
        self.assertEqual(ga.pygad_instance.gene_type,gt)
        self.assertEqual(ga.pygad_instance.random_seed,4)

    # VC-410
    def test_05_GAFitness(self):
        ga = ga_constructor()
        ga.instanciate_dynamic_ga()
        self.assertEqual(ga.fitness_dynamic_ga(ga.pygad_instance,[9,8,7,6,5,4,3,2,1,0],[120]),7560)

    # VC-411
    @patch('sys.stdout', new_callable=io.StringIO) 
    def test_06_OnGenerations(self,mock_stdout):
        ga = ga_constructor()
        ga.instanciate_dynamic_ga()
        ga.pygad_instance.generations_completed = 120
        pop_fitness = (7560,)*30
        ga.pygad_instance.population[:,:] = [[9,8,7,6,5,4,3,2,1,0]]*30
        ga.pygad_instance.best_solution(pop_fitness)
        ga.print_generations(ga.pygad_instance)
        self.assertEqual(mock_stdout.getvalue(),"Generation Completed:  120\nSolution:  [9 8 7 6 5 4 3 2 1 0]\nFitness:  7560\n")

    # VC-412
    @patch('sys.stdout', new_callable=io.StringIO) 
    def test_07_NoneOnGenerations(self,mock_stdout):
        ga = ga_constructor()
        ga.instanciate_dynamic_ga()
        ga.pygad_instance.generations_completed = 119
        pop_fitness = (7560,)*30
        ga.pygad_instance.population[:,:] = [[9,8,7,6,5,4,3,2,1,0]]*30
        ga.pygad_instance.best_solution(pop_fitness)
        ga.print_generations(ga.pygad_instance)
        self.assertEqual(mock_stdout.getvalue(),'')

class Test_WPEVT(unittest.TestCase):
    
    # VC-413
    def test_01_WPEVTPygadInstanciate(self):
        ga = ga_constructor()
        
        ga.instanciate_wpevt_ga()
        
        gs = [{'low': 0,'high': 10}] * 10
        gt = [[int,None]]*10
        self.assertEqual(ga.pygad_instance.num_generations,1000)
        self.assertEqual(ga.pygad_instance.sol_per_pop,30)
        self.assertEqual(ga.pygad_instance.num_parents_mating,10)
        self.assertEqual(ga.pygad_instance.num_genes,10)
        self.assertEqual(ga.pygad_instance.gene_space,gs)
        self.assertEqual(ga.pygad_instance.parent_selection_type,"sss")
        self.assertEqual(ga.pygad_instance.keep_elitism,10)
        self.assertEqual(ga.pygad_instance.crossover_type,"two_points")
        self.assertEqual(ga.pygad_instance.mutation_type,"adaptive")
        self.assertEqual(ga.pygad_instance.mutation_percent_genes,[70,15])
        self.assertCountEqual(ga.pygad_instance.stop_criteria,[['reach',0.9],['saturate',100]])
        self.assertEqual(ga.pygad_instance.gene_type,gt)
        self.assertEqual(ga.pygad_instance.random_seed,4)

    # VC-414
    def test_02_WPEVTFitness(self):
        pb = {'BubbleSort': {'block0': 1, 'block1': 10, 'block2': 10, 'block3': 55, 'block4': 55, 'block6': 45, 'block7': 45, 'block8': 45, 'block9': 45, 'block5': 10, 'block10': 10, 'block12': 9, 'block13': 9, 'block11': 1, 'block14': 1}}
        interface_target.run.return_value = ['Input', 'Input', 'Input', 'Input', 'Input', 'Input', 'Input', 'Input', 'Input', 'Input', '#;BubbleSort;block0', '#;BubbleSort;block1', '#;BubbleSort;block2', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block5', '#;BubbleSort;block10', '#;BubbleSort;block12', '#;BubbleSort;block13', '#;BubbleSort;block1', '#;BubbleSort;block2', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block5', '#;BubbleSort;block10', '#;BubbleSort;block12', '#;BubbleSort;block13', '#;BubbleSort;block1', '#;BubbleSort;block2', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block5', '#;BubbleSort;block10', '#;BubbleSort;block12', '#;BubbleSort;block13', '#;BubbleSort;block1', '#;BubbleSort;block2', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block5', '#;BubbleSort;block10', '#;BubbleSort;block12', '#;BubbleSort;block13', '#;BubbleSort;block1', '#;BubbleSort;block2', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block5', '#;BubbleSort;block10', '#;BubbleSort;block12', '#;BubbleSort;block13', '#;BubbleSort;block1', '#;BubbleSort;block2', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block5', '#;BubbleSort;block10', '#;BubbleSort;block12', '#;BubbleSort;block13', '#;BubbleSort;block1', '#;BubbleSort;block2', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block5', '#;BubbleSort;block10', '#;BubbleSort;block12', '#;BubbleSort;block13', '#;BubbleSort;block1', '#;BubbleSort;block2', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block5', '#;BubbleSort;block10', '#;BubbleSort;block12', '#;BubbleSort;block13', '#;BubbleSort;block1', '#;BubbleSort;block2', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block6', '#;BubbleSort;block7', '#;BubbleSort;block8', '#;BubbleSort;block9', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block5', '#;BubbleSort;block10', '#;BubbleSort;block12', '#;BubbleSort;block13', '#;BubbleSort;block1', '#;BubbleSort;block2', '#;BubbleSort;block3', '#;BubbleSort;block4', '#;BubbleSort;block5', '#;BubbleSort;block10', '#;BubbleSort;block11', '#;BubbleSort;block14', '#cycles 1043271', 'Bye Bye!', 'SystemClock::Endless stopped', 'number of cpu cycles simulated: 1072142', '']
        ga = ga_constructor()
        ga.instanciate_wpevt_ga()
        self.assertEqual(ga.filter_output_wpevt(interface_target.run.return_value),pb)
        self.assertEqual(ga.fitness_wpevt(ga.pygad_instance,[9,8,7,6,5,4,3,2,1,0],[120]),0.837709)

if __name__ == '__main__':
    unittest.main()