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


class HybridIpetFacade:
    """
    Class for estimating the Worst-Case Execution Time (WCET) of a program.

    This class encapsulates the logic for calculating WCET using the IPET with measurements of basic blocks.


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
        self.inter_values = IntermediateValues()

        self.interface_target = InterfaceTarget(
            project=self.project, inter_values=self.inter_values)

        self.input_manager = InputManager(project=self.project,
                                          inter_values=self.inter_values)
        self.timer = TimeMeter(project=self.project,
                               inter_values=self.inter_values,
                               interface_target=self.interface_target)

    def run(self) -> None:
        '''
        Hybrid IPET pipeline for calculate WCET.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''

        if self.input_manager.generator:
            self.inter_values.test_cases = self.input_manager.generate_inputs()
        else:
            self.inter_values.test_cases = [self.project.chosen_input]

        self.interface_target.compile_io_ports()
        self.interface_target.compile_tick_counter()
        self.interface_target.compile_to_ir()
        self.interface_target.setup_ipet_hybrid()
        self.interface_target.instrument_ipet_hybrid()
        self.interface_target.set_ir()
        self.interface_target.link()
        self.interface_target.compile_to_obj()
        self.interface_target.compile_to_asm()
        self.interface_target.backend_compile()
        self.interface_target.flash()
        self.timer.run_test_cases()
        self.timer.save_times()

        #Pre processor before IPET
        create_call_graph(self.project, self.inter_values)
        loop_mapping(self.inter_values)
        loop_bounding(self.inter_values)
        functions_mapping(self.inter_values)
        create_call_graph_in_post_order(self.inter_values)
        graph = {}
        graph_generator_post_order(self.inter_values, graph)

        #Create weight and calculate using IPET
        ipet = Ipet(graph, self.project)
        update_weight_by_measurements(graph, self.timer, False)
        self.wcet.set_swcet(ipet.run_ipet_hybrid())