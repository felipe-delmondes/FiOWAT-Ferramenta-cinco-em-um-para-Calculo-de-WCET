from utils.wcet_data import WcetData
from utils.intermediate_values import IntermediateValues
from utils.user_project import UserProject

from inputs.input_manager import InputManager
from interface_target.interface_target import InterfaceTarget

from utils.create_files import *
from cfg.graph_generator import *
from cfg.pre_processor import *
from cfg.graph_weight import *
from cfg.timeMeter import *
from ipet.ipet import *
from constraint_solver.worst_path import *
from ga.dynamic_ga import GA
from evt.evt_method import Evt, evt_running
import pandas as pd


class WpevtFacade():
    """
    Class for estimating the Worst-Case Execution Time (WCET) of a program using Worst Path EVT.


    Parameters
    ----------
    project : UserProject
        Contain all information about project


    Attributes
    ----------
    project : UserProject
        Contain all information about project

    wcet : WcetData
        Contain all information about wcet
    """

    def __init__(self, project: UserProject, wcet: WcetData) -> None:
        self.project = project
        self.wcet = wcet

    def run(self) -> None:
        '''
        Run Worst Path EVT for find pWCET and sWCET.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # Create DTO, and auxiliary objects
        inter_values = IntermediateValues()
        interface_target = InterfaceTarget(project=self.project,
                                           inter_values=inter_values)
        input_manager = InputManager(project=self.project,
                                     inter_values=inter_values)
        timer = TimeMeter(project=self.project,
                          inter_values=inter_values,
                          interface_target=interface_target)
        ga = GA(project=self.project, input_manager=input_manager,
                interface_target=interface_target, inter_values=inter_values)

        # Generate code coverage to obtain weights of each basic block
        if input_manager.generator:
            inter_values.test_cases = input_manager.generate_inputs()
        else:
            inter_values.test_cases = [self.project.chosen_input]

        interface_target.compile_io_ports()
        interface_target.compile_tick_counter()
        interface_target.compile_to_ir()
        interface_target.setup_ipet_hybrid()
        interface_target.instrument_ipet_hybrid()
        interface_target.set_ir()
        interface_target.link()
        interface_target.compile_to_obj()
        interface_target.compile_to_asm()
        interface_target.backend_compile()
        interface_target.flash()

        timer.run_test_cases()
        timer.save_times()

        # Create graph to calculate worst path using IPET
        create_call_graph(self.project, inter_values)
        loop_mapping(inter_values)
        loop_bounding(inter_values)
        functions_mapping(inter_values)
        create_call_graph_in_post_order(inter_values)
        graph = {}
        graph_generator_post_order(inter_values, graph)

        # Calculate the worst path and sWCET
        ipet = Ipet(graph, self.project, inter_values)
        update_weight_by_measurements(graph, timer, False)
        self.wcet.set_swcet(ipet.run_ipet_constraint_solver())

        # # Find the input that transverse the worst path
        interface_target.set_ga_filenames()
        interface_target.compile_to_ir()
        interface_target.instrument_wpevt()
        interface_target.link()
        interface_target.compile_to_obj()
        interface_target.compile_to_asm()
        interface_target.backend_compile()
        interface_target.flash()

        ga.instanciate_wpevt_ga()
        ga.run()
        solution = ga.best_solution()

        interface_target.compile_to_ir()
        interface_target.link()
        interface_target.compile_to_obj()
        interface_target.compile_to_asm()
        interface_target.backend_compile()
        interface_target.flash()

        results_exec = evt_running(self.project, self.wcet, interface_target, solution)
        if results_exec is None:
            return
        
        # Save the list with all runs results to a csv file.
        csv_filename = os.path.join(
            self.project.output_directory,
            f"{self.project.main_file_name}_{self.project.number_exec}.csv")


        results_exec = pd.DataFrame(results_exec)
        results_exec.to_csv(csv_filename, index=False, header=False)

        # EVT Method Instantiation and call
        evt = Evt(self.project, csv_filename)

        try:
            pwcet_list, iid_flag, rawdata_df = Evt.run(evt)
        except Exception as e:
            print(
                f"\n\33[41mError running EVT! {e}\33[0m")
            exit(-1)

        # Transmits the results to the report
        self.wcet.set_pwcet(pwcet_list)
        self.wcet.set_hwm(rawdata_df.valuesx.max())
        self.wcet.set_iid_flag(iid_flag)
        self.wcet.set_histogram(rawdata_df)